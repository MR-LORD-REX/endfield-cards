from __future__ import annotations
from pydantic import BaseModel


class WeaponStatBonus(BaseModel):
    """A static stat bonus granted by a weapon skill (e.g. flat Wisd, ATK%)."""
    prop_id: int
    prop_name: str
    value: float
    is_percentage: bool
    display: str       # human-readable e.g. "132" or "33.0%"
    icon_url: str


class BlackboardEntry(BaseModel):
    key: str
    value: float


class WeaponPassiveSkill(BaseModel):
    """A conditional/combat passive weapon skill with its blackboard at resolved level."""
    skill_id: str
    level: int
    blackboard: list[BlackboardEntry]
    tag_id: str


class WeaponData(BaseModel):
    template_id: int
    weapon_id: str             # e.g. "wpn_sword_0006"
    name: str                  # e.g. "Forgeborn Scathe"
    rarity: int
    weapon_type: str           # e.g. "Sword"
    level: int
    refine_lv: int
    breakthrough_lv: int
    base_atk: float            # base ATK at current level from upgrade table
    skill_levels: list[int]    # resolved [skill0_lv, skill1_lv, skill2_lv]
    icon_url: str
    stat_bonuses: list[WeaponStatBonus]    # attr_wisd / attr_atk style skills
    passive_skills: list[WeaponPassiveSkill]  # combat passive skills
