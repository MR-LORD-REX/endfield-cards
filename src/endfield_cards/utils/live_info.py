"""Typed UTC Live information from supplied SDK fields and event dictionaries."""

from typing import Any

from endfield_cards.models.context import RenderContext
from endfield_cards.models.rendered import (
    EchoCycleInfo,
    EchoSeasonInfo,
    EchoStageInfo,
    LiveContractInfo,
    LiveInfo,
    MeterInfo,
    WarEchoesInfo,
)
from endfield_cards.utils.activity import _entries, _select, observed_number
from endfield_cards.utils.time import source_datetime


def identifier(value: Any) -> str | None:
    return str(value) if value is not None and str(value).strip() else None


def observed_bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def meter_info(meter: Any) -> MeterInfo | None:
    if meter is None:
        return None
    fields: set[str] = getattr(meter, "model_fields_set", set())
    current = observed_number(meter.current) if "current" in fields else None
    maximum = observed_number(meter.maximum) if "maximum" in fields else None
    return MeterInfo(
        key=meter.key,
        name=meter.name,
        current=current,
        maximum=maximum,
        recovery_at=source_datetime(meter.recovery_at),
        refresh_at=source_datetime(meter.refresh_at),
        note=meter.note,
        complete=current >= maximum if current is not None and maximum is not None and maximum > 0 else None,
    )


def _raw_meter(key: str, name: str, source: dict[str, Any]) -> MeterInfo:
    current, maximum = observed_number(source.get("count")), observed_number(source.get("total"))
    return MeterInfo(
        key,
        name,
        current,
        maximum,
        None,
        None,
        str(source.get("note") or ""),
        current >= maximum if current is not None and maximum is not None and maximum > 0 else None,
    )


def _war_echoes(source: Any, now: Any) -> WarEchoesInfo | None:
    if not isinstance(source, dict):
        return None
    raw_seasons = _entries(source.get("seasons"))
    if not raw_seasons:
        return None
    seasons = []
    for index, item in enumerate(raw_seasons):
        cycles = []
        for cycle_index, cycle in enumerate(_entries(item.get("weeks"))):
            stages = tuple(
                EchoStageInfo(
                    stage_index,
                    str(stage.get("name") or ""),
                    observed_number(stage.get("star")),
                    observed_bool(stage.get("plusTask")),
                )
                for stage_index, stage in enumerate(_entries(cycle.get("dungeonGroups")))
            )
            cycles.append(
                EchoCycleInfo(
                    cycle_index,
                    identifier(cycle.get("id")),
                    str(cycle.get("name") or ""),
                    observed_number(cycle.get("stars")),
                    source_datetime(cycle.get("startTs")),
                    source_datetime(cycle.get("endTs")),
                    observed_bool(cycle.get("allPlusTasks")),
                    stages,
                )
            )
        seasons.append(
            EchoSeasonInfo(
                index,
                identifier(item.get("id")),
                str(item.get("name") or ""),
                observed_number(item.get("stars")),
                source_datetime(item.get("startTs")),
                source_datetime(item.get("endTs")),
                observed_bool(item.get("allPlusTasks")),
                tuple(cycles),
            )
        )
    selected_raw = _select(raw_seasons, now, "startTs", "endTs")
    selected_index = next(index for index, item in enumerate(raw_seasons) if item is selected_raw)
    season = seasons[selected_index]
    cycles_raw = _entries(selected_raw.get("weeks"))
    selected_cycle = _select(cycles_raw, now, "startTs", "endTs")
    selected_cycle_index = next(
        (index for index, item in enumerate(cycles_raw) if item is selected_cycle), None
    )
    activity = source.get("activity")
    return WarEchoesInfo(
        tuple(seasons),
        season,
        season.cycles[selected_cycle_index] if selected_cycle_index is not None else None,
        str(activity.get("name") or "") if isinstance(activity, dict) else "",
    )


def _contracts(source: Any, now: Any) -> tuple[tuple[LiveContractInfo, ...], LiveContractInfo | None]:
    raw = _entries(source)
    entries = tuple(
        LiveContractInfo(
            index,
            identifier(item.get("id")),
            str(item.get("name") or ""),
            observed_number(item.get("highest")),
            observed_number(item.get("challengeCount")),
            source_datetime(item.get("startAtTs")),
            source_datetime(item.get("gameplayEndAtTs")),
            source_datetime(item.get("endAtTs")),
            tuple(
                _raw_meter(key, label, mission)
                for key, label in (
                    ("weeklyMission", "Weekly"),
                    ("indicatorMission", "Indicators"),
                    ("stageMission", "Stages"),
                )
                if isinstance(mission := item.get(key), dict)
            ),
        )
        for index, item in enumerate(raw)
    )
    selected = _select(raw, now, "startAtTs", "gameplayEndAtTs")
    selected_index = next((index for index, item in enumerate(raw) if item is selected), None)
    return entries, entries[selected_index] if selected_index is not None else None


def live_info(model: Any, context: RenderContext) -> LiveInfo:
    events = model.current_event if isinstance(model.current_event, dict) else {}
    contracts, selected = _contracts(events.get("crisis_contract"), model.server_time)
    return LiveInfo(
        context.owner,
        source_datetime(model.server_time),
        meter_info(model.sanity),
        meter_info(model.daily),
        meter_info(model.weekly),
        meter_info(model.battle_pass),
        meter_info(model.credits),
        tuple(info for meter in model.activities if (info := meter_info(meter)) is not None),
        _war_echoes(events.get("war_echoes"), model.server_time),
        selected,
        contracts,
    )
