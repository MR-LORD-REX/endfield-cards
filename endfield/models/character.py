from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

from .weapon import WeaponData
from .equipment import EquipData, SuitSet


class SkillInfo(BaseModel):
    skill_id: int
    icon_url: str
    element: str
    level: int
    max_level: int
    enhanced_level: int


class TalentPassiveNode(BaseModel):
    node_id: str
    icon_url: str
    level: int    # 1–3 tier
    index: int    # position in the talent tree


class TalentFactoryNode(BaseModel):
    node_id: str
    icon_url: str
    level: int
    index: int


class TalentInfo(BaseModel):
    latest_break_node: str    # e.g. "charBreak70"
    ascension: int            # 0–4 mapped from break node via other.json
    attr_nodes: list[str]     # active attribute upgrade node IDs
    passive_nodes: list[TalentPassiveNode]
    factory_nodes: list[TalentFactoryNode]


class ComputedStats(BaseModel):
    """Final computed display stats, matching the in-game character card."""
    # Primary attributes
    str_val: int
    agi: int
    wisd: int
    will: int
    # Core combat stats
    hp: int
    atk: int
    defense: int
    crit_rate: float        # percentage e.g. 5.0
    crit_dmg: float         # percentage e.g. 50.0
    arts_intensity: float   # flat e.g. 30
    # Secondary stats
    healing_received_bonus: float    # percentage e.g. 15.4
    ultimate_gain_efficiency: float  # percentage e.g. 116.0
    # Element damage bonus (None if no relevant equip/weapon bonuses)
    element_dmg_bonus: Optional[float] = None   # percentage e.g. 50.5
    element_dmg_type: Optional[str] = None      # e.g. "Fire"
    # Optional damage bonuses
    normal_skill_dmg_bonus: Optional[float] = None   # percentage e.g. 103.5


class CharacterData(BaseModel):
    template_id: int
    str_id: str         # e.g. "chr_0016_laevat"
    name: str
    rarity: int
    element: str
    profession: str
    weapon_type: str
    level: int
    potential_level: int
    # Art assets
    splash_url: str
    bg_url: str
    round_icon_url: str
    # Build
    weapon: Optional[WeaponData] = None
    equips: list[EquipData] = []
    suit_sets: dict[str, SuitSet] = {}
    # Keys: "normal" | "ultimate" | "combo" | "attack"
    skills: dict[str, Optional[SkillInfo]] = {}
    talents: Optional[TalentInfo] = None
    # Computed (None if calculation failed)
    stats: Optional[ComputedStats] = None
