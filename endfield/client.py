from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import aiohttp

from .decoder import DataDecoder
from .resolver import AssetResolver, ENKA_BASE
from .calculator import StatCalculator
from .errors import APIError, CharacterNotFoundError, WeaponNotFoundError
from .models import (
    ShowcaseData, PlayerProfile, ProfileCharacter, DomainProgress,
    CharacterData, ComputedStats, SkillInfo, TalentInfo,
    TalentPassiveNode, TalentFactoryNode,
    WeaponData, WeaponStatBonus, WeaponPassiveSkill, BlackboardEntry,
    EquipData, AttrModifier, SuitSet, SuitSetEffect,
)

logger = logging.getLogger(__name__)

_ENKA_API = "https://enka.network/ef/{uid}/__data.json?x-sveltekit-invalidated=01"


class Endfield:
    """
    Main entry point.

    Usage::

        async with Endfield(assets_path="assets", debug=True) as ef:
            data = await ef.get_showcase(4225399080)
    """

    def __init__(
        self,
        assets_path: str | Path = "assets",
        session: Optional[aiohttp.ClientSession] = None,
        debug: bool = False,
    ) -> None:
        self._assets_path = Path(__file__).parent / "assets"
        self._external_session = session
        self._session: Optional[aiohttp.ClientSession] = None
        self._resolver: Optional[AssetResolver] = None

        log_level = logging.DEBUG if debug else logging.WARNING
        logging.basicConfig(
            level=log_level,
            format="%(levelname)s [%(name)s] %(message)s",
        )
        logger.setLevel(log_level)

    async def __aenter__(self) -> "Endfield":
        await self._init_session()
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def _init_session(self) -> None:
        if self._external_session:
            self._session = self._external_session
        else:
            self._session = aiohttp.ClientSession()
        self._resolver = AssetResolver(self._assets_path, self._session)

    async def close(self) -> None:
        if self._session and not self._external_session:
            await self._session.close()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    async def get_showcase(self, uid: int | str) -> ShowcaseData:
        if not self._session:
            await self._init_session()
        raw = await self._fetch_api(str(uid))
        decoded = DataDecoder(raw).decode()
        profile = await self._build_profile(uid, decoded)
        characters = await self._build_characters(decoded)
        return ShowcaseData(profile=profile, characters=characters)

    # ------------------------------------------------------------------
    # API fetch
    # ------------------------------------------------------------------

    async def _fetch_api(self, uid: str) -> dict:
        url = _ENKA_API.format(uid=uid)
        logger.debug("Fetching API: %s", url)
        async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status != 200:
                raise APIError(resp.status, url)
            return await resp.json(content_type=None)

    # ------------------------------------------------------------------
    # Profile builder
    # ------------------------------------------------------------------

    async def _build_profile(self, uid: int | str, decoded: dict) -> PlayerProfile:
        card  = decoded.get("playerInfo", {}).get("businessCard", {})
        stats = card.get("statistic", {})

        domains = [
            DomainProgress(domain_id=d.get("domainId", ""), level=d.get("level", 0))
            for d in card.get("domainDev", {}).get("domains", [])
        ]

        profile_chars: list[ProfileCharacter] = []
        for entry in card.get("charList", []):
            str_id = entry.get("templateId", "")
            meta   = self._resolver.get_character_by_str_id(str_id)
            if meta is None:
                logger.warning("charList str_id '%s' not in characters.json", str_id)
                continue
            profile_chars.append(ProfileCharacter(
                template_id=self._resolver.get_template_id(str_id),
                str_id=str_id,
                name=meta.get("name", ""),
                level=entry.get("level", 1),
                potential_level=entry.get("potentialLevel", 0),
                rarity=meta.get("rarity", 0),
                element=meta.get("element", ""),
                profession=meta.get("profession", ""),
                splash_url=self._resolver.icon_url(meta.get("assets", {}).get("splash", "")),
                round_icon_url=self._resolver.icon_url(meta.get("assets", {}).get("round_icon", "")),
            ))

        return PlayerProfile(
            uid=str(uid),
            name=card.get("name", ""),
            short_id=str(card.get("shortId", "")),
            signature=card.get("signature", ""),
            adventure_level=card.get("adventureLevel", 0),
            world_level=card.get("worldLevel", 0),
            char_count=stats.get("charNum", 0),
            weapon_count=stats.get("weaponNum", 0),
            doc_count=stats.get("docNum", 0),
            domain_progress=domains,
            characters=profile_chars,
            ttl=decoded.get("ttl"),
        )

    # ------------------------------------------------------------------
    # Character builders
    # ------------------------------------------------------------------

    async def _build_characters(self, decoded: dict) -> list[CharacterData]:
        char_data_raw: list[dict] = decoded.get("playerInfo", {}).get("charData", [])
        results = []
        for raw_char in char_data_raw:
            try:
                results.append(await self._build_character(raw_char))
            except Exception as exc:
                logger.error("Failed to build templateId=%s: %s", raw_char.get("templateId", "?"), exc)
        return results

    async def _build_character(self, raw: dict) -> CharacterData:
        tid  = raw.get("templateId")
        meta = self._resolver.get_character(tid)
        if meta is None:
            raise CharacterNotFoundError(tid)

        str_id    = meta.get("str_id", "")
        level     = raw.get("level", 1)
        pot_level = raw.get("potentialLevel", 0)
        element   = meta.get("element", "")
        assets    = meta.get("assets", {})

        talent_raw = raw.get("talent", {})
        attr_nodes = talent_raw.get("attrNodes", [])
        break_node = talent_raw.get("latestBreakNode", "")
        ascension  = self._resolver.get_break_to_ascension().get(break_node, 0)

        equip_raw_list       = raw.get("equip", [])
        equip_pairs, suit_pieces = await self._resolve_equips(equip_raw_list)
        equip_models         = self._build_equip_models(equip_pairs)
        suit_models, suit_details = await self._build_suit_sets(suit_pieces)

        weapon_raw = raw.get("weapon", {})
        weapon_model, weapon_detail, skill_levels = await self._build_weapon(weapon_raw)

        skill_models  = self._build_skills(raw.get("skillInfo", {}), meta)
        talent_model  = self._build_talents(talent_raw, break_node, ascension, meta)

        stats: Optional[ComputedStats] = None
        try:
            stats = StatCalculator.compute(
                char_meta=meta,
                level=level,
                attr_nodes=attr_nodes,
                equip_pairs=equip_pairs,
                weapon_raw=weapon_raw,
                weapon_detail=weapon_detail,
                weapon_skill_levels=skill_levels,
                suit_details=suit_details,
                suit_pieces=suit_pieces,
                element=element,
                main_attr_id=meta.get("main_attr_id", 41),
                sub_attr_id=meta.get("sub_attr_id", 39),
                api_id_map=self._resolver.api_id_map,
            )
        except Exception as exc:
            logger.error("Stat calc failed for %s: %s", str_id, exc)

        return CharacterData(
            template_id=tid,
            str_id=str_id,
            name=meta.get("name", ""),
            rarity=meta.get("rarity", 0),
            element=element,
            profession=meta.get("profession", ""),
            weapon_type=meta.get("weapon_type", ""),
            level=level,
            potential_level=pot_level,
            splash_url=self._resolver.icon_url(assets.get("splash", "")),
            bg_url=self._resolver.icon_url(assets.get("bg", "")),
            round_icon_url=self._resolver.icon_url(assets.get("round_icon", "")),
            weapon=weapon_model,
            equips=equip_models,
            suit_sets=suit_models,
            skills=skill_models,
            talents=talent_model,
            stats=stats,
        )

    # ------------------------------------------------------------------
    # Weapon builder
    # ------------------------------------------------------------------

    async def _build_weapon(
        self, raw: dict
    ) -> tuple[Optional[WeaponData], Optional[dict], list[int]]:
        tid      = raw.get("templateId")
        wpn_meta = self._resolver.weapons.get(str(tid))
        if wpn_meta is None:
            logger.warning("Weapon templateId %s not in weapons.json", tid)
            return None, None, []

        weapon_id     = wpn_meta.get("slug", "")
        weapon_detail = await self._resolver.get_weapon_detail(weapon_id)
        if weapon_detail is None:
            logger.warning("No detail found for weapon %s", weapon_id)
            return None, None, []

        bt_lv     = raw.get("breakthroughLv", 0)
        gem       = raw.get("attachedGem", {})
        gem_terms = [
            {"cost": t.get("cost", 0)}
            for t in (gem.get("terms") or [])
            if isinstance(t, dict)
        ]
        skill_levels = StatCalculator.get_weapon_skill_levels(weapon_detail, bt_lv, gem_terms)

        wpn_lv   = raw.get("weaponLv", 1)
        base_atk = next(
            (float(e["baseAtk"]) for e in
             weapon_detail.get("progression", {}).get("upgrade", {}).get("list", [])
             if e.get("weaponLv") == wpn_lv),
            0.0,
        )

        stat_bonuses   = self._build_weapon_stat_bonuses(weapon_detail, skill_levels)
        passive_skills = self._build_weapon_passives(weapon_detail, skill_levels)

        model = WeaponData(
            template_id=tid,
            weapon_id=weapon_id,
            name=wpn_meta.get("name", ""),
            rarity=wpn_meta.get("rarity", 0),
            weapon_type=wpn_meta.get("weapon_type", ""),
            level=wpn_lv,
            refine_lv=raw.get("refineLv", 0),
            breakthrough_lv=bt_lv,
            base_atk=base_atk,
            skill_levels=skill_levels,
            icon_url=self._resolver.icon_url(f"/ui/ef/itemicon/{weapon_id}.png"),
            stat_bonuses=stat_bonuses,
            passive_skills=passive_skills,
        )
        return model, weapon_detail, skill_levels

    def _build_weapon_stat_bonuses(
        self, detail: dict, skill_levels: list[int]
    ) -> list[WeaponStatBonus]:
        bonuses: list[WeaponStatBonus] = []
        prop_id_map = {"wisd": 41, "agi": 40, "str": 39, "will": 42, "atk": 2}
        name_map    = {41: "Wisd_base", 40: "Agi_base", 39: "Str_base",
                       42: "Will_base",  2: "Atk_base"}

        for i, skill_id in enumerate(detail.get("weaponSkillList", [])):
            bundle = detail.get("skills", {}).get(skill_id, {}).get("SkillPatchDataBundle", [])
            if not bundle or not bundle[0].get("tagId", "").startswith("attr_"):
                continue
            lv = skill_levels[i] if i < len(skill_levels) else 1
            for bb in StatCalculator.get_skill_blackboard(detail, skill_id, lv):
                key = bb.get("key", "")
                val = float(bb.get("value", 0.0))
                prop_id = prop_id_map.get(key)
                if prop_id is None:
                    continue
                is_pct = key == "atk"
                bonuses.append(WeaponStatBonus(
                    prop_id=prop_id,
                    prop_name=name_map.get(prop_id, key),
                    value=val,
                    is_percentage=is_pct,
                    display=f"{val * 100:.1f}%" if is_pct else str(int(val)),
                    icon_url=f"{ENKA_BASE}/ui/ef/attributeicon/{key.capitalize()}.png",
                ))
        return bonuses

    def _build_weapon_passives(
        self, detail: dict, skill_levels: list[int]
    ) -> list[WeaponPassiveSkill]:
        passives: list[WeaponPassiveSkill] = []
        for i, skill_id in enumerate(detail.get("weaponSkillList", [])):
            bundle = detail.get("skills", {}).get(skill_id, {}).get("SkillPatchDataBundle", [])
            if not bundle or bundle[0].get("tagId", "").startswith("attr_"):
                continue
            lv = skill_levels[i] if i < len(skill_levels) else 1
            bb = StatCalculator.get_skill_blackboard(detail, skill_id, lv)
            passives.append(WeaponPassiveSkill(
                skill_id=skill_id,
                level=lv,
                blackboard=[BlackboardEntry(key=e["key"], value=e["value"]) for e in bb],
                tag_id=bundle[0].get("tagId", ""),
            ))
        return passives

    # ------------------------------------------------------------------
    # Equipment builders
    # ------------------------------------------------------------------

    async def _resolve_equips(
        self, equip_list: list[dict]
    ) -> tuple[list[tuple[dict, Optional[dict]]], dict[str, int]]:
        """Raw entries are {key: slot_id, value: {templateid, enhance, ...}}."""
        pairs: list[tuple[dict, Optional[dict]]] = []
        suit_pieces: dict[str, int] = {}
        for entry in equip_list:
            slot_data = entry.get("value", entry)
            tid  = slot_data.get("templateid") or slot_data.get("templateId")
            meta = self._resolver.get_equipment(tid)
            if meta is None:
                logger.warning("Equipment templateId %s not in equipments.json", tid)
            else:
                sid = meta.get("suit_id", "")
                suit_pieces[sid] = suit_pieces.get(sid, 0) + 1
            pairs.append((slot_data, meta))
        return pairs, suit_pieces

    def _build_equip_models(
        self, pairs: list[tuple[dict, Optional[dict]]]
    ) -> list[EquipData]:
        models: list[EquipData] = []
        for slot_raw, meta in pairs:
            if meta is None:
                continue
            tid = slot_raw.get("templateid") or slot_raw.get("templateId")
            enhance_map = {
                e.get("key", -1): e.get("value", 0)
                for e in slot_raw.get("enhance", [])
                if isinstance(e, dict)
            }
            modifiers: list[AttrModifier] = []
            for i, mod in enumerate(meta.get("attr_modifiers", [])):
                attr_type = mod["attr_type"]
                enh_lv    = enhance_map.get(i, 0)
                values    = mod.get("values", [0.0])
                value     = float(values[min(enh_lv, len(values) - 1)])
                modifiers.append(AttrModifier(
                    index=i,
                    attr_type=attr_type,
                    attr_name=self._resolver.get_prop_name(attr_type),
                    formula=mod.get("formula", "BaseAddition"),
                    enhance_level=enh_lv,
                    value=value,
                ))
            models.append(EquipData(
                slot_id=slot_raw.get("key", 0),
                template_id=tid,
                rarity=meta.get("rarity", 0),
                suit_id=meta.get("suit_id", ""),
                icon_url=self._resolver.icon_url(f"/ui/ef/itemicon/{meta.get('slug', '')}.png"),
                attr_modifiers=modifiers,
            ))
        return models

    # ------------------------------------------------------------------
    # Suit set builder
    # ------------------------------------------------------------------

    async def _build_suit_sets(
        self, suit_pieces: dict[str, int]
    ) -> tuple[dict[str, SuitSet], dict[str, dict]]:
        suit_models:  dict[str, SuitSet] = {}
        suit_details: dict[str, dict]    = {}

        for suit_id, count in suit_pieces.items():
            basic  = self._resolver.get_suit_basic(suit_id)
            detail = await self._resolver.get_suit_detail(suit_id)
            if detail:
                suit_details[suit_id] = detail

            icon_path    = basic.get("icon", "") if basic else ""
            is_active    = False
            active_bonus: Optional[SuitSetEffect] = None

            if detail:
                for effect in detail.get("setEffects", []):
                    if count >= effect.get("equipCnt", 9999):
                        is_active = True
                        active_bonus = SuitSetEffect(
                            equip_count=effect["equipCnt"],
                            blackboard=effect.get("blackboardValues", {}),
                            stat_blackboard=effect.get("statBlackboardValues", {}),
                        )

            suit_models[suit_id] = SuitSet(
                suit_id=suit_id,
                name=detail.get("engName") if detail else None,
                icon_url=self._resolver.icon_url(icon_path),
                pieces_equipped=count,
                is_active=is_active,
                active_bonus=active_bonus,
            )

        return suit_models, suit_details

    # ------------------------------------------------------------------
    # Skill builder
    # ------------------------------------------------------------------

    def _build_skills(
        self, skill_info: dict, char_meta: dict
    ) -> dict[str, Optional[SkillInfo]]:
        level_map  = {e.get("skillId"): e for e in skill_info.get("levelInfo", [])}
        icon_map   = char_meta.get("skill_info_map", {})

        mapping = {
            "normal":   skill_info.get("normalSkill"),
            "ultimate": skill_info.get("ultimateSkill"),
            "combo":    skill_info.get("comboSkill"),
            "attack":   skill_info.get("dispNormalAttackSkill"),
        }
        result: dict[str, Optional[SkillInfo]] = {}
        for key, skill_id in mapping.items():
            if skill_id is None:
                result[key] = None
                continue
            entry = level_map.get(skill_id)
            meta  = icon_map.get(str(skill_id), {})
            result[key] = SkillInfo(
                skill_id=skill_id,
                icon_url=self._resolver.icon_url(meta.get("icon", "")),
                element=meta.get("element", ""),
                level=entry.get("skillLevel", 1) if entry else 1,
                max_level=entry.get("skillMaxLevel", 1) if entry else 1,
                enhanced_level=entry.get("skillEnhancedLevel", 1) if entry else 1,
            ) if entry else None
        return result

    # ------------------------------------------------------------------
    # Talent builder
    # ------------------------------------------------------------------

    def _build_talents(
        self,
        talent_raw: dict,
        break_node: str,
        ascension: int,
        char_meta: dict,
    ) -> Optional[TalentInfo]:
        if not talent_raw:
            return None
        node_map = char_meta.get("node_skill_map", {})

        passive_nodes = [
            TalentPassiveNode(
                node_id=nid,
                icon_url=self._resolver.icon_url(node_map.get(nid, {}).get("icon", "")),
                level=node_map.get(nid, {}).get("level", 1),
                index=node_map.get(nid, {}).get("index", 0),
            )
            for nid in talent_raw.get("latestPassiveSkillNodes", [])
        ]
        factory_nodes = [
            TalentFactoryNode(
                node_id=nid,
                icon_url=self._resolver.icon_url(node_map.get(nid, {}).get("icon", "")),
                level=node_map.get(nid, {}).get("level", 1),
                index=node_map.get(nid, {}).get("index", 0),
            )
            for nid in talent_raw.get("latestFactorySkillNodes", [])
        ]

        return TalentInfo(
            latest_break_node=break_node,
            ascension=ascension,
            attr_nodes=talent_raw.get("attrNodes", []),
            passive_nodes=passive_nodes,
            factory_nodes=factory_nodes,
        )