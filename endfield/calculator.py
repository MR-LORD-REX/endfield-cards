"""
Stat calculator for Arknights: Endfield characters.

All formulas verified against live game data (Laevatain, level 90):
    HP   = hp_by_level[lv-1]  +  5 × total_STR
    ATK  = ((char_atk + wpn_base_atk) × (1 + %ATK) + flat_ATK)
           × (1 + 0.005 × MAIN + 0.002 × SUB)
    DEF  = Σ equip DEF flat (attr_type 3)
    CritRate % = 5.0 + Σ equip bonuses (attr_type 9)  × 100
    CritDMG  % = 50.0 + Σ equip bonuses (attr_type 10) × 100
    HealRecv % = WILL × 0.1 + Σ equip (attr_type 30)  × 100
    UltGain  % = (1 + Σ equip (attr_type 44)) × 100
    ElemDMG  % = (Σ equip elem_prop + wpn passive) × 100
    NormSkDMG% = Σ equip (attr_type 32) × 100
    ArtsIntns  = suit phy_spell_up + Σ equip (attr_type 87)
"""

from __future__ import annotations
from typing import Optional

from .models.character import ComputedStats

# Character element → fire/nat/etc damage increase prop IDs
ELEMENT_TO_PROP: dict[str, int] = {
    "Fire":     51,
    "Natural":  54,
    "Physical": 50,
    "Pulse":    52,
    "Cryst":    53,
    "Ether":    55,
}

# Weapon blackboard key → attribute prop ID
WPN_KEY_TO_PROP: dict[str, int] = {
    "wisd": 41,
    "agi":  40,
    "str":  39,
    "str_val": 39,  # Alternative format
    "will": 42,
    "atk":   2,
}

# Attribute prop ID → primary attr label
PROP_TO_PRIMARY: dict[int, str] = {
    39: "str",
    40: "agi",
    41: "wisd",
    42: "will",
}


class StatCalculator:
    """Pure static methods — no state, no instantiation required."""

    # ------------------------------------------------------------------
    # Weapon skill level resolution
    # ------------------------------------------------------------------

    @staticmethod
    def get_weapon_skill_levels(
        weapon_detail: dict,
        breakthrough_lv: int,
        gem_terms: list[dict],
    ) -> list[int]:
        """
        Resolve actual weapon skill levels from breakthrough level + gem terms.

        gem_terms is the decoded list from attachedGem.terms, ordered by skill index.
        Each term dict has a 'cost' key indicating extra levels above the breakthrough
        minimum for that skill.
        """
        bt_list: list[dict] = (
            weapon_detail
            .get("progression", {})
            .get("breakthrough", {})
            .get("list", [])
        )

        # Find breakthrough entry matching current breakthrough level
        bt_entry: Optional[dict] = None
        for entry in bt_list:
            if entry.get("breakthroughShowLv") == breakthrough_lv:
                bt_entry = entry
                break
        if bt_entry is None and bt_list:
            bt_entry = bt_list[-1]
        if bt_entry is None:
            return [1] * 3

        bounds: list[dict] = bt_entry.get("skillLevelBounds", [])
        skill_levels: list[int] = []

        for i, bound in enumerate(bounds):
            min_lv = bound.get("lowerBound", 1)
            max_lv = bound.get("upperBound", 9)
            cost   = gem_terms[i].get("cost", 0) if i < len(gem_terms) else 0
            skill_levels.append(min(min_lv + cost, max_lv))

        return skill_levels

    # ------------------------------------------------------------------
    # Weapon blackboard lookup
    # ------------------------------------------------------------------

    @staticmethod
    def get_skill_blackboard(
        weapon_detail: dict,
        skill_id: str,
        level: int,
    ) -> list[dict]:
        """Return the blackboard list for a weapon skill at a specific level."""
        bundle: list[dict] = (
            weapon_detail
            .get("skills", {})
            .get(skill_id, {})
            .get("SkillPatchDataBundle", [])
        )
        for entry in bundle:
            if entry.get("level") == level:
                return entry.get("blackboard", [])
        return bundle[-1].get("blackboard", []) if bundle else []

    # ------------------------------------------------------------------
    # Main stat computation
    # ------------------------------------------------------------------

    @staticmethod
    def compute(
        char_meta: dict,
        level: int,
        attr_nodes: list[str],
        equip_pairs: list[tuple[dict, Optional[dict]]],
        weapon_raw: dict,
        weapon_detail: Optional[dict],
        weapon_skill_levels: list[int],
        suit_details: dict[str, dict],
        suit_pieces: dict[str, int],
        element: str,
        main_attr_id: int,
        sub_attr_id: int,
        debug: bool = False,
    ) -> ComputedStats:
        """
        Compute all display stats for a character.

        Parameters
        ----------
        equip_pairs:
            List of (decoded_equip_dict, equip_meta_from_assets) pairs.
            equip_meta may be None if the template ID was not found in assets.
        weapon_raw:
            Fully decoded weapon dict from the API (templateId, weaponLv, ...).
        debug:
            Enable debug logging for stat computation.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        if debug:
            logger.debug(f"=== StatCalculator.compute START ===")
            logger.debug(f"Character level: {level}, element: {element}")
            logger.debug(f"main_attr_id: {main_attr_id}, sub_attr_id: {sub_attr_id}")

        # ── 1. Base primary attributes (level growth curve) ──────────────
        base_attrs = char_meta.get("base_attributes", {})

        def _base_attr(attr_id: int) -> float:
            a = base_attrs.get(str(attr_id), {})
            return a.get("base", 0.0) + a.get("add", 0.0) * (level - 1)

        primary_base = {
            39: _base_attr(39),  # STR
            40: _base_attr(40),  # AGI
            41: _base_attr(41),  # WISD
            42: _base_attr(42),  # WILL
        }

        # ── 2. Attribute node bonuses (talent tree unlocks) ───────────────
        attr_node_map = char_meta.get("attribute_nodes", {})
        node_bonus: dict[int, float] = {39: 0.0, 40: 0.0, 41: 0.0, 42: 0.0}
        for node_id in attr_nodes:
            for attr_id_str, val in attr_node_map.get(node_id, {}).items():
                attr_id = int(attr_id_str)
                if attr_id in node_bonus:
                    node_bonus[attr_id] += float(val)

        # ── 3. Weapon attribute bonuses ────────────────────────────────────
        wpn_attr_bonus: dict[int, float] = {39: 0.0, 40: 0.0, 41: 0.0, 42: 0.0}
        wpn_atk_pct: float = 0.0

        if weapon_detail:
            skill_list: list[str] = weapon_detail.get("weaponSkillList", [])
            skills_data: dict     = weapon_detail.get("skills", {})

            for i, skill_id in enumerate(skill_list):
                bundle = skills_data.get(skill_id, {}).get("SkillPatchDataBundle", [])
                if not bundle:
                    continue
                tag_id: str = bundle[0].get("tagId", "")
                if not tag_id.startswith("attr_"):
                    continue  # passive skill — handled separately

                lv = weapon_skill_levels[i] if i < len(weapon_skill_levels) else 1
                blackboard = StatCalculator.get_skill_blackboard(weapon_detail, skill_id, lv)

                for bb in blackboard:
                    key = bb.get("key", "")
                    val = float(bb.get("value", 0.0))
                    if key == "atk":
                        wpn_atk_pct += val
                    elif key in WPN_KEY_TO_PROP:
                        prop = WPN_KEY_TO_PROP[key]
                        if prop in wpn_attr_bonus:
                            wpn_attr_bonus[prop] += val

        # ── 4. Equipment bonuses ─────────────────────────────────────────
        equip_bonus: dict[int, float] = {}

        for equip_raw, equip_meta in equip_pairs:
            if equip_meta is None:
                continue
            enhance_map = {
                e.get("key", -1): e.get("value", 0)
                for e in equip_raw.get("enhance", [])
                if isinstance(e, dict)
            }
            for i, mod in enumerate(equip_meta.get("attr_modifiers", [])):
                attr_type  = mod["attr_type"]
                enhance_lv = enhance_map.get(i, 0)
                values     = mod.get("values", [0.0])
                value      = float(values[min(enhance_lv, len(values) - 1)])
                equip_bonus[attr_type] = equip_bonus.get(attr_type, 0.0) + value

        # ── 5. Suit set static bonuses (phy_spell_up → arts intensity) ────
        suit_arts_intensity = 0.0

        for suit_id, detail in suit_details.items():
            pieces = suit_pieces.get(suit_id, 0)
            for effect in detail.get("setEffects", []):
                if pieces >= effect.get("equipCnt", 9999):
                    stat_bb = effect.get("statBlackboardValues", {})
                    suit_arts_intensity += float(stat_bb.get("phy_spell_up", 0.0))

        # ── 6. Final primary attributes ────────────────────────────────────
        total: dict[int, float] = {
            attr: primary_base[attr] + node_bonus[attr] + wpn_attr_bonus[attr]
                  + equip_bonus.get(attr, 0.0)
            for attr in (39, 40, 41, 42)
        }

        STR  = int(total[39])
        AGI  = int(total[40])
        WISD = int(total[41])
        WILL = int(total[42])
        
        if debug:
            logger.debug(f"Primary attributes - STR: {STR}, AGI: {AGI}, WISD: {WISD}, WILL: {WILL}")
            logger.debug(f"  STR breakdown - base: {primary_base[39]:.1f}, node: {node_bonus[39]:.1f}, wpn: {wpn_attr_bonus[39]:.1f}, equip: {equip_bonus.get(39, 0.0):.1f}")
            logger.debug(f"  Weapon ATK %: {wpn_atk_pct * 100:.1f}%")
            logger.debug(f"  Equip bonuses: {equip_bonus}")

        MAIN_ATTR = int(total.get(main_attr_id, total[41]))
        SUB_ATTR  = int(total.get(sub_attr_id,  total[39]))

        # ── 7. HP ───────────────────────────────────────────────────────────
        hp_table: list[int] = char_meta.get("hp_by_level", [])
        hp_base = hp_table[level - 1] if len(hp_table) >= level else 0
        hp = hp_base + 5 * STR
        
        if debug:
            logger.debug(f"HP calculation: base={hp_base}, STR×5={5*STR}, total={hp}")

        # ── 8. DEF ──────────────────────────────────────────────────────────
        defense = int(equip_bonus.get(3, 0.0))

        # ── 9. ATK ──────────────────────────────────────────────────────────
        atk_table: list[int] = char_meta.get("atk_by_level", [])
        char_atk_base = atk_table[level - 1] if len(atk_table) >= level else 0

        wpn_base_atk = 0.0
        if weapon_detail:
            wpn_level = weapon_raw.get("weaponLv", 1)
            for entry in (
                weapon_detail
                .get("progression", {})
                .get("upgrade", {})
                .get("list", [])
            ):
                if entry.get("weaponLv") == wpn_level:
                    wpn_base_atk = float(entry.get("baseAtk", 0.0))
                    break

        flat_atk = equip_bonus.get(2, 0.0)  # rare flat ATK from equipment
        atk = int(
            ((char_atk_base + wpn_base_atk) * (1.0 + wpn_atk_pct) + flat_atk)
            * (1.0 + 0.005 * MAIN_ATTR + 0.002 * SUB_ATTR)
        )
        
        if debug:
            main_multiplier = 1.0 + 0.005 * MAIN_ATTR + 0.002 * SUB_ATTR
            logger.debug(f"ATK calculation: char_base={char_atk_base}, wpn_base={wpn_base_atk}, wpn_atk_pct={wpn_atk_pct*100:.1f}%, flat_atk={flat_atk}, main_mult={main_multiplier:.4f}, total={atk}")

        # ── 10. Crit stats ──────────────────────────────────────────────────
        crit_rate = round((0.05 + equip_bonus.get(9, 0.0))  * 100, 1)
        crit_dmg  = round((0.50 + equip_bonus.get(10, 0.0)) * 100, 1)
        
        if debug:
            logger.debug(f"Crit stats - rate: 5% + {equip_bonus.get(9, 0.0)*100:.1f}% = {crit_rate}%, dmg: 50% + {equip_bonus.get(10, 0.0)*100:.1f}% = {crit_dmg}%")

        # ── 11. Arts intensity ──────────────────────────────────────────────
        arts_intensity = suit_arts_intensity + equip_bonus.get(87, 0.0)

        # ── 12. Healing received bonus ──────────────────────────────────────
        #   Base source: WILL × 0.1%  +  equip HealTakenIncrease (propId 30)
        healing_received = round(
            WILL * 0.1 + equip_bonus.get(30, 0.0) * 100, 1
        )
        
        if debug:
            logger.debug(f"Healing received: WILL×0.1={WILL*0.1:.1f}% + equip×100={equip_bonus.get(30, 0.0)*100:.1f}% = {healing_received}%")

        # ── 13. Ultimate gain efficiency ────────────────────────────────────
        ultimate_gain = round((1.0 + equip_bonus.get(44, 0.0)) * 100, 1)
        
        if debug:
            logger.debug(f"Ultimate gain: (1.0 + {equip_bonus.get(44, 0.0):.2f}) × 100 = {ultimate_gain}%")

        # ── 14. Element damage bonus ────────────────────────────────────────
        element_dmg: Optional[float] = None
        element_dmg_type: Optional[str] = None

        elem_prop = ELEMENT_TO_PROP.get(element)
        if elem_prop is not None:
            base_elem = equip_bonus.get(elem_prop, 0.0)

            # Weapon passive skills may contribute elem dmg (e.g. fire_dmg_up)
            wpn_elem_bonus = 0.0
            if weapon_detail:
                skill_list = weapon_detail.get("weaponSkillList", [])
                skills_data = weapon_detail.get("skills", {})
                for i, skill_id in enumerate(skill_list):
                    bundle = skills_data.get(skill_id, {}).get("SkillPatchDataBundle", [])
                    if not bundle or bundle[0].get("tagId", "").startswith("attr_"):
                        continue
                    lv = weapon_skill_levels[i] if i < len(weapon_skill_levels) else 1
                    for bb in StatCalculator.get_skill_blackboard(weapon_detail, skill_id, lv):
                        key = bb.get("key", "")
                        val = float(bb.get("value", 0.0))
                        if key == "fire_dmg_up"    and element == "Fire":
                            wpn_elem_bonus += val
                        elif key == "nature_dmg_up" and element == "Natural":
                            wpn_elem_bonus += val
                        elif key == "pulse_dmg_up"  and element == "Pulse":
                            wpn_elem_bonus += val
                        elif key == "cryst_dmg_up"  and element == "Cryst":
                            wpn_elem_bonus += val
                        elif key == "ether_dmg_up"  and element == "Ether":
                            wpn_elem_bonus += val
                        elif key == "phys_dmg_up"   and element == "Physical":
                            wpn_elem_bonus += val

            total_elem = base_elem + wpn_elem_bonus
            if total_elem > 0:
                element_dmg = round(total_elem * 100, 1)
                element_dmg_type = element

        # ── 15. Normal skill damage bonus ───────────────────────────────────
        ns_raw = equip_bonus.get(32, 0.0)
        normal_skill_dmg = round(ns_raw * 100, 1) if ns_raw > 0 else None

        return ComputedStats(
            str_val=STR,
            agi=AGI,
            wisd=WISD,
            will=WILL,
            hp=hp,
            atk=atk,
            defense=defense,
            crit_rate=crit_rate,
            crit_dmg=crit_dmg,
            arts_intensity=arts_intensity,
            healing_received_bonus=healing_received,
            ultimate_gain_efficiency=ultimate_gain,
            element_dmg_bonus=element_dmg,
            element_dmg_type=element_dmg_type,
            normal_skill_dmg_bonus=normal_skill_dmg,
        )
