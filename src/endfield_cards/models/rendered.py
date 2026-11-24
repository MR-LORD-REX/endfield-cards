"""Copy-safe card bundles and immutable selectors for downstream clients."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeAlias, TypeVar

from endfield_cards.models.identity import OwnerIdentity
from endfield_cards.models.result import CardResult


@dataclass(frozen=True)
class CharacterSelection:
    index: int
    source_index: int
    id: str
    canonical_id: str | None
    template_id: int | None
    name: str
    showcase_index: int | None
    page: int
    page_index: int


@dataclass(frozen=True)
class CharacterListInfo:
    family: str
    owner: OwnerIdentity
    source_scope: str
    characters: tuple[CharacterSelection, ...]
    roster_complete: bool | None
    reported_count: int | None


@dataclass(frozen=True)
class MeterInfo:
    key: str
    name: str
    current: float | None
    maximum: float | None
    recovery_at: datetime | None
    refresh_at: datetime | None
    note: str
    complete: bool | None


@dataclass(frozen=True)
class EchoStageInfo:
    index: int
    name: str
    stars: float | None
    plus_task: bool | None


@dataclass(frozen=True)
class EchoCycleInfo:
    index: int
    id: str | None
    name: str
    stars: float | None
    starts_at: datetime | None
    ends_at: datetime | None
    all_plus_tasks: bool | None
    stages: tuple[EchoStageInfo, ...]


@dataclass(frozen=True)
class EchoSeasonInfo:
    index: int
    id: str | None
    name: str
    stars: float | None
    starts_at: datetime | None
    ends_at: datetime | None
    all_plus_tasks: bool | None
    cycles: tuple[EchoCycleInfo, ...]


@dataclass(frozen=True)
class WarEchoesInfo:
    seasons: tuple[EchoSeasonInfo, ...]
    season: EchoSeasonInfo | None
    cycle: EchoCycleInfo | None
    activity_name: str


@dataclass(frozen=True)
class LiveContractInfo:
    index: int
    id: str | None
    name: str
    best_score: float | None
    attempts: float | None
    starts_at: datetime | None
    ends_at: datetime | None
    ends_at_collection: datetime | None
    missions: tuple[MeterInfo, ...]


@dataclass(frozen=True)
class LiveInfo:
    owner: OwnerIdentity
    server_time: datetime | None
    sanity: MeterInfo | None
    daily: MeterInfo | None
    weekly: MeterInfo | None
    battle_pass: MeterInfo | None
    credits: MeterInfo | None
    activities: tuple[MeterInfo, ...]
    war_echoes: WarEchoesInfo | None
    contingency_contract: LiveContractInfo | None
    contracts: tuple[LiveContractInfo, ...]

    @property
    def fully_replenished_at(self) -> datetime | None:
        """Return the supplied Sanity recovery deadline, without estimating one."""
        return self.sanity.recovery_at if self.sanity is not None else None


@dataclass(frozen=True)
class StageSelection:
    index: int
    event_id: str | None
    id: str | None
    name: str
    normal_id: str | None
    hard_id: str | None
    recommended_level: int | None
    normal_cleared: bool | None
    hard_cleared: bool | None
    normal_duration_seconds: float | None
    hard_duration_seconds: float | None


@dataclass(frozen=True)
class MonumentEventInfo:
    index: int
    id: str | None
    name: str
    is_active: bool | None
    starts_at: datetime | None
    ends_at: datetime | None
    stages: tuple[StageSelection, ...]


@dataclass(frozen=True)
class MonumentInfo:
    owner: OwnerIdentity
    events: tuple[MonumentEventInfo, ...]


@dataclass(frozen=True)
class EntrySelection:
    index: int
    id: str | None
    name: str


@dataclass(frozen=True)
class RunSelection:
    index: int
    id: str | None
    completed_at: datetime | None
    duration_seconds: float | None
    score: int | None
    waves: int | None


@dataclass(frozen=True)
class ContractSelection:
    index: int
    id: str | None
    name: str
    stage_id: str | None
    stage_name: str
    stage_recommended_level: int | None
    best_score: int | None
    attempts: int | None
    starts_at: datetime | None
    ends_at: datetime | None
    ends_at_collection: datetime | None
    missions: tuple[MeterInfo, ...]
    runs: tuple[RunSelection, ...]
    modifiers: tuple[EntrySelection, ...]
    enemies: tuple[EntrySelection, ...]


@dataclass(frozen=True)
class ContractInfo:
    owner: OwnerIdentity
    current_id: str | None
    contracts: tuple[ContractSelection, ...]


RenderInfo: TypeAlias = CharacterListInfo | LiveInfo | MonumentInfo | ContractInfo | None
ModelT = TypeVar("ModelT")
InfoT = TypeVar("InfoT")


@dataclass(frozen=True, init=False)
class RenderedCard(Generic[ModelT, InfoT]):
    """Cards, a private source snapshot, and immutable navigation/time data.

    Accessing ``model`` returns a new deep copy. Mutating that model cannot
    change the rendered bytes, metadata, a cached result, or another caller.
    """

    cards: tuple[CardResult, ...]
    info: InfoT
    _model: ModelT = field(repr=False, compare=False)

    def __init__(self, cards: Any, model: ModelT, info: InfoT) -> None:
        object.__setattr__(self, "cards", tuple(cards))
        object.__setattr__(self, "info", info)
        object.__setattr__(self, "_model", deepcopy(model))

    @property
    def model(self) -> ModelT:
        return deepcopy(self._model)

    @property
    def card(self) -> CardResult:
        """Convenience for a single-image result; require explicit page handling otherwise."""
        if len(self.cards) != 1:
            raise ValueError("Use cards to access a result containing multiple or zero images")
        return self.cards[0]
