"""Observed display summaries of the SDK's live-event dictionaries."""

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from endfield_cards.utils.time import remaining, source_datetime


def observed_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def _entries(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _select(entries: list[dict[str, Any]], now: datetime | None, start: str, end: str) -> dict[str, Any]:
    clock = source_datetime(now)
    if clock is not None:
        for item in entries:
            begins, ends = source_datetime(item.get(start)), source_datetime(item.get(end))
            if (begins is None or begins <= clock) and (ends is None or ends > clock):
                return item
    return entries[-1] if entries else {}


@dataclass(frozen=True)
class EchoSummary:
    season: str
    cycle: str
    stars: float | None
    stages: tuple[tuple[str, float | None, bool | None], ...]
    starts_at: datetime | None
    ends_at: datetime | None
    poster: str | None
    all_plus_tasks: bool | None


@dataclass(frozen=True)
class ContractSummary:
    name: str
    score: float | None
    attempts: float | None
    missions: tuple[tuple[str, float | None, float | None], ...]
    starts_at: datetime | None
    ends_at: datetime | None
    poster: str | None


def event_summaries(model: Any) -> tuple[EchoSummary | None, ContractSummary | None]:
    events = model.current_event if isinstance(model.current_event, dict) else {}
    raw = events.get("war_echoes")
    season = _select(
        _entries(raw.get("seasons")) if isinstance(raw, dict) else [], model.server_time, "startTs", "endTs"
    )
    echo = None
    if season:
        cycle = _select(_entries(season.get("weeks")), model.server_time, "startTs", "endTs")
        stages = tuple(
            (str(stage.get("name") or ""), observed_number(stage.get("star")), stage.get("plusTask"))
            for stage in _entries(cycle.get("dungeonGroups"))
        )
        echo = EchoSummary(
            str(season.get("name") or ""),
            str(cycle.get("name") or ""),
            observed_number(cycle.get("stars", season.get("stars"))),
            stages,
            source_datetime(cycle.get("startTs", season.get("startTs"))),
            source_datetime(cycle.get("endTs", season.get("endTs"))),
            season.get("headerImage") or season.get("kvImage"),
            cycle.get("allPlusTasks", season.get("allPlusTasks")),
        )
    source = _select(
        _entries(events.get("crisis_contract")), model.server_time, "startAtTs", "gameplayEndAtTs"
    )
    contract = None
    if source:
        missions = tuple(
            (name, observed_number(item.get("count")), observed_number(item.get("total")))
            for key, name in (
                ("weeklyMission", "Weekly"),
                ("indicatorMission", "Indicators"),
                ("stageMission", "Stages"),
            )
            if isinstance(item := source.get(key), dict)
        )
        contract = ContractSummary(
            str(source.get("name") or "").removeprefix("Contingency Contract:").strip(),
            observed_number(source.get("highest")),
            observed_number(source.get("challengeCount")),
            missions,
            source_datetime(source.get("startAtTs")),
            source_datetime(source.get("gameplayEndAtTs")),
            source.get("headerImage") or source.get("kvImage"),
        )
    return echo, contract


def event_status(starts_at: datetime | None, ends_at: datetime | None, now: datetime | None) -> str:
    clock = source_datetime(now)
    if clock is None:
        return "Time unavailable"
    if starts_at is not None and starts_at > clock:
        return "Starts in " + remaining(starts_at, clock)
    if ends_at is None:
        return "End time unavailable"
    return "Ended" if ends_at <= clock else "Ends in " + remaining(ends_at, clock)
