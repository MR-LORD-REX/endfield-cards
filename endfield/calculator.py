"""
Stat calculator for Arknights: Endfield characters.

Verified formulas:
    HP   = hp_by_level[lv-1] + 5×STR + flat_HP_bonus (suit/weapon passive)
    ATK  = ((char_atk + wpn_base) × (1 + %ATK) + flat_ATK)
           × (1 + 0.005×MAIN + 0.002×SUB)
    DEF  = Σ equip DEF flat (attr 3)
    CritRate % = 5.0 + Σ bonus (attr 9) × 100
    CritDMG  % = 50.0 + Σ bonus (attr 10) × 100
    HealRecv % = WILL × 0.1 + Σ bonus (attr 30) × 100
    UltGain  % = (1 + Σ bonus (attr 44)) × 100
    ElemDMG  % = Σ elem bonus × 100
    NormSkDMG% = Σ bonus (attr 32) × 100
    ArtsIntns  = Σ bonus (attr 87)

All bonus sources (equip modifiers, suit set effects, weapon passive skills)
are mapped through api_id_map to get prop IDs and accumulated into bonus_pool.
"""

from __future__ import annotations
from typing import Optional

from .models.character import ComputedStats

ELEMENT_TO_PROP: dict[str, int] = {
    "Fire": 51, "Natural": 54, "Physical": 50,
    "Pulse": 52, "Cryst": 53, "Ether": 55,
}

# Weapon "attr_" skill keys → primary attr prop IDs
WPN_ATTR_KEY_TO_PROP: dict[str, int] = {
    "wisd": 41, "agi": 40, "str": 39, "will": 42,
}


class StatCalculator:

    @staticmethod
    def get_weapon_skill_levels(
        weapon_detail: dict,
        breakthrough_lv: int,
        gem_terms: list[dict],
    ) -> list[int]:
        bt_list: list[dict] = (
            weapon_detail.get("progression", {})
            .get("breakthrough", {}).get("list", [])
        )
        bt_entry = next(
            (e for e in bt_list if e.get("breakthroughShowLv") == breakthrough_lv),
            bt_list[-1] if bt_list else None,
        )
        if bt_entry is None:
            return [1] * 3
        bounds = bt_entry.get("skillLevelBounds", [])
        return [
            min(
                b.get("lowerBound", 1) + (gem_terms[i].get("cost", 0) if i < len(gem_terms) else 0),
                b.get("upperBound", 9),
            )
            for i, b in enumerate(bounds)
        ]

    @staticmethod
    def get_skill_blackboard(weapon_detail: dict, skill_id: str, level: int) -> list[dict]:
        bundle = (
            weapon_detail.get("skills", {})
            .get(skill_id, {}).get("SkillPatchDataBundle", [])
        )
        for entry in bundle:
            if entry.get("level") == level:
                return entry.get("blackboard", [])
        return bundle[-1].get("blackboard", []) if bundle else []

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
        api_id_map: dict,
    ) -> ComputedStats:

        # ── 1. Base primary attributes (level growth curve) ───────────────
        base_attrs = char_meta.get("base_attributes", {})

        def _base(attr_id: int) -> float:
            a = base_attrs.get(str(attr_id), {})
            return a.get("base", 0.0) + a.get("add", 0.0) * (level - 1)

        primary_base = {39: _base(39), 40: _base(40), 41: _base(41), 42: _base(42)}

        # ── 2. Attribute node bonuses (talent tree) ───────────────────────
        attr_node_map = char_meta.get("attribute_nodes", {})
        node_bonus: dict[int, float] = {39: 0.0, 40: 0.0, 41: 0.0, 42: 0.0}
        for nid in attr_nodes:
            for k, v in attr_node_map.get(nid, {}).items():
                pid = int(k)
                if pid in node_bonus:
                    node_bonus[pid] += float(v)

        # ── 3. Weapon "attr_" skill bonuses (flat primary attrs + ATK%) ───
        wpn_attr_bonus: dict[int, float] = {39: 0.0, 40: 0.0, 41: 0.0, 42: 0.0}
        wpn_atk_pct: float = 0.0

        if weapon_detail:
            for i, skill_id in enumerate(weapon_detail.get("weaponSkillList", [])):
                bundle = (
                    weapon_detail.get("skills", {})
                    .get(skill_id, {}).get("SkillPatchDataBundle", [])
                )
                if not bundle or not bundle[0].get("tagId", "").startswith("attr_"):
                    continue
                lv = weapon_skill_levels[i] if i < len(weapon_skill_levels) else 1
                for bb in StatCalculator.get_skill_blackboard(weapon_detail, skill_id, lv):
                    key = bb.get("key", "")
                    val = float(bb.get("value", 0.0))
                    if key == "atk":
                        wpn_atk_pct += val
                    elif key in WPN_ATTR_KEY_TO_PROP:
                        wpn_attr_bonus[WPN_ATTR_KEY_TO_PROP[key]] += val

        # ── 4. Bonus pool: equip modifiers ────────────────────────────────
        # All stat bonuses from every source are collected here keyed by prop ID.
        bonus_pool: dict[int, float] = {}

        for equip_raw, equip_meta in equip_pairs:
            if equip_meta is None:
                continue
            enhance_map = {
                e.get("key", -1): e.get("value", 0)
                for e in equip_raw.get("enhance", [])
                if isinstance(e, dict)
            }
            for i, mod in enumerate(equip_meta.get("attr_modifiers", [])):
                attr_type = mod["attr_type"]
                enh_lv    = enhance_map.get(i, 0)
                values    = mod.get("values", [0.0])
                value     = float(values[min(enh_lv, len(values) - 1)])
                bonus_pool[attr_type] = bonus_pool.get(attr_type, 0.0) + value

        # ── 5. Bonus pool: suit set effect stat bonuses ───────────────────
        for suit_id, detail in suit_details.items():
            pieces = suit_pieces.get(suit_id, 0)
            for effect in detail.get("setEffects", []):
                if pieces < effect.get("equipCnt", 9999):
                    continue
                for key, val in effect.get("statBlackboardValues", {}).items():
                    pid = api_id_map.get(key, {}).get("id")
                    if pid is not None:
                        bonus_pool[pid] = bonus_pool.get(pid, 0.0) + float(val)

        # ── 6. Bonus pool: weapon passive skill bonuses ───────────────────
        # Non-"attr_" skills (tagId != "attr_*") carry combat passive bonuses.
        # Keys are mapped through api_id_map; unrecognised keys (duration, etc.) skipped.
        if weapon_detail:
            for i, skill_id in enumerate(weapon_detail.get("weaponSkillList", [])):
                bundle = (
                    weapon_detail.get("skills", {})
                    .get(skill_id, {}).get("SkillPatchDataBundle", [])
                )
                if not bundle or bundle[0].get("tagId", "").startswith("attr_"):
                    continue
                lv = weapon_skill_levels[i] if i < len(weapon_skill_levels) else 1
                for bb in StatCalculator.get_skill_blackboard(weapon_detail, skill_id, lv):
                    pid = api_id_map.get(bb.get("key", ""), {}).get("id")
                    if pid is not None:
                        bonus_pool[pid] = bonus_pool.get(pid, 0.0) + float(bb.get("value", 0.0))

        # ── 7. Final primary attributes ───────────────────────────────────
        total_primary = {
            attr: primary_base[attr] + node_bonus[attr] + wpn_attr_bonus[attr]
                  + bonus_pool.get(attr, 0.0)
            for attr in (39, 40, 41, 42)
        }
        STR  = int(total_primary[39])
        AGI  = int(total_primary[40])
        WISD = int(total_primary[41])
        WILL = int(total_primary[42])
        MAIN_ATTR = int(total_primary.get(main_attr_id, total_primary[41]))
        SUB_ATTR  = int(total_primary.get(sub_attr_id,  total_primary[39]))

        # ── 8. HP ─────────────────────────────────────────────────────────
        hp_table = char_meta.get("hp_by_level", [])
        hp_base  = hp_table[level - 1] if len(hp_table) >= level else 0
        # bonus_pool[1] = flat HP bonus from suit set effects (e.g. hp_up: 1000)
        hp = hp_base + 5 * STR + int(bonus_pool.get(1, 0.0))

        # ── 9. DEF ───────────────────────────────────────────────────────
        defense = int(bonus_pool.get(3, 0.0))

        # ── 10. ATK ──────────────────────────────────────────────────────
        atk_table     = char_meta.get("atk_by_level", [])
        char_atk_base = atk_table[level - 1] if len(atk_table) >= level else 0

        wpn_base_atk = 0.0
        if weapon_detail:
            wpn_lv = weapon_raw.get("weaponLv", 1)
            wpn_base_atk = next(
                (float(e["baseAtk"]) for e in
                 weapon_detail.get("progression", {}).get("upgrade", {}).get("list", [])
                 if e.get("weaponLv") == wpn_lv),
                0.0,
            )

        flat_atk = bonus_pool.get(2, 0.0)
        atk = int(
            ((char_atk_base + wpn_base_atk) * (1.0 + wpn_atk_pct) + flat_atk)
            * (1.0 + 0.005 * MAIN_ATTR + 0.002 * SUB_ATTR)
        )

        # ── 11. Secondary stats ───────────────────────────────────────────
        crit_rate      = round((0.05 + bonus_pool.get(9,  0.0)) * 100, 1)
        crit_dmg       = round((0.50 + bonus_pool.get(10, 0.0)) * 100, 1)
        arts_intensity = bonus_pool.get(87, 0.0)
        healing_received = round(WILL * 0.1 + bonus_pool.get(30, 0.0) * 100, 1)
        ultimate_gain  = round((1.0 + bonus_pool.get(44, 0.0)) * 100, 1)

        # ── 12. Element damage bonus ──────────────────────────────────────
        element_dmg: Optional[float] = None
        element_dmg_type: Optional[str] = None
        elem_prop = ELEMENT_TO_PROP.get(element)
        if elem_prop is not None:
            total_elem = bonus_pool.get(elem_prop, 0.0)
            if total_elem > 0:
                element_dmg = round(total_elem * 100, 1)
                element_dmg_type = element

        # ── 13. Normal skill damage bonus ─────────────────────────────────
        ns_raw = bonus_pool.get(32, 0.0)
        normal_skill_dmg = round(ns_raw * 100, 1) if ns_raw > 0 else None

        return ComputedStats(
            str_val=STR, agi=AGI, wisd=WISD, will=WILL,
            hp=hp, atk=atk, defense=defense,
            crit_rate=crit_rate, crit_dmg=crit_dmg,
            arts_intensity=arts_intensity,
            healing_received_bonus=healing_received,
            ultimate_gain_efficiency=ultimate_gain,
            element_dmg_bonus=element_dmg,
            element_dmg_type=element_dmg_type,
            normal_skill_dmg_bonus=normal_skill_dmg,
        )