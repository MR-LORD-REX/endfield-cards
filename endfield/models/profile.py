from __future__ import annotations
from pydantic import BaseModel


class DomainProgress(BaseModel):
    domain_id: str
    level: int


class ProfileCharacter(BaseModel):
    """Lightweight character entry from the player's charList (not full build data)."""
    template_id: int
    str_id: str
    name: str
    level: int
    potential_level: int
    rarity: int
    element: str
    profession: str
    splash_url: str
    round_icon_url: str


class PlayerProfile(BaseModel):
    uid: str
    name: str
    short_id: str
    signature: str
    adventure_level: int
    world_level: int
    char_count: int
    weapon_count: int
    doc_count: int
    domain_progress: list[DomainProgress]
    # Only the 4 showcase characters with basic info
    characters: list[ProfileCharacter]
    ttl: int | None = None
