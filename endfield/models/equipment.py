from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class AttrModifier(BaseModel):
    """A single stat modifier from an equipment piece at its current enhance level."""
    index: int          # position in the attr_modifiers array
    attr_type: int      # prop ID e.g. 41 = Wisd
    attr_name: str      # human-readable e.g. "Wisd_base"
    formula: str        # "BaseAddition" | "BaseMultiplier" | "BaseFinalMultiplier"
    enhance_level: int  # 0–3
    value: float        # resolved value at enhance_level


class EquipData(BaseModel):
    slot_id: int        # 0–3
    template_id: int
    rarity: int
    suit_id: str
    icon_url: str
    attr_modifiers: list[AttrModifier]


class SuitSetEffect(BaseModel):
    """Active set bonus effect and its blackboard values."""
    equip_count: int                # pieces required to activate
    blackboard: dict[str, float]    # full blackboard (includes conditional effects)
    stat_blackboard: dict[str, float]  # static-only subset (for stat display)


class SuitSet(BaseModel):
    suit_id: str
    name: Optional[str] = None    # English name from detail JSON e.g. "Hot Work"
    icon_url: str
    pieces_equipped: int
    is_active: bool               # True if any set bonus threshold is reached
    active_bonus: Optional[SuitSetEffect] = None
