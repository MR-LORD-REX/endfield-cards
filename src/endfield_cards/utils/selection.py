"""Stable, source-backed selection data accompanying rendered cards."""

from collections.abc import Sequence
from typing import Any

from endfield_cards.models.context import RenderContext
from endfield_cards.models.rendered import (
    CharacterListInfo,
    CharacterSelection,
    ContractInfo,
    ContractSelection,
    EntrySelection,
    MonumentEventInfo,
    MonumentInfo,
    RenderedCard,
    RenderInfo,
    RunSelection,
    StageSelection,
)
from endfield_cards.models.result import CardResult
from endfield_cards.utils.live_info import identifier, live_info, meter_info
from endfield_cards.utils.time import source_datetime


def character_info(
    model: Any, context: RenderContext, *, family: str, character_ids: Any = None
) -> CharacterListInfo:
    characters = list(model.characters if hasattr(model, "characters") else model)
    wanted = (
        {str(value) for value in character_ids} if family == "roster" and character_ids is not None else None
    )
    selected = [
        (index, item)
        for index, item in enumerate(characters)
        if wanted is None or item.identity.skport_id in wanted or item.identity.str_id in wanted
    ]
    per_page = 8 if family == "profile" else 72
    entries = tuple(
        CharacterSelection(
            index,
            source_index,
            item.identity.skport_id,
            item.identity.str_id,
            item.identity.template_id,
            item.name,
            item.showcase_index,
            index // per_page + 1,
            index % per_page,
        )
        for index, (source_index, item) in enumerate(selected)
    )
    counts = getattr(model, "counts", None)
    reported = counts.characters if counts is not None and "characters" in counts.model_fields_set else None
    return CharacterListInfo(
        family,
        context.owner,
        context.source_scope,
        entries,
        getattr(model, "roster_complete", None),
        reported,
    )


def monument_info(model: Any, context: RenderContext, event_id: str | None = None) -> MonumentInfo:
    events = list(model.events) if hasattr(model, "events") else [model]
    entries = []
    for index, event in enumerate(events):
        if event_id is not None and event.id != str(event_id):
            continue
        stages = tuple(
            StageSelection(
                stage_index,
                identifier(event.id),
                identifier(stage.id),
                stage.name,
                identifier(stage.normal_id),
                identifier(stage.hard_id),
                stage.recommended_level,
                stage.normal_cleared if "normal_cleared" in stage.model_fields_set else None,
                stage.hard_cleared if "hard_cleared" in stage.model_fields_set else None,
                stage.normal.duration_seconds if stage.normal is not None else None,
                stage.hard.duration_seconds if stage.hard is not None else None,
            )
            for stage_index, stage in enumerate(event.stages)
        )
        entries.append(
            MonumentEventInfo(
                index,
                identifier(event.id),
                event.name,
                event.is_active if "is_active" in event.model_fields_set else None,
                source_datetime(event.starts_at),
                source_datetime(event.ends_at),
                stages,
            )
        )
    return MonumentInfo(context.owner, tuple(entries))


def contract_info(model: Any, context: RenderContext, contract_id: str | None = None) -> ContractInfo:
    if hasattr(model, "contracts"):
        entries = [model.current] if model.current is not None else []
        entries.extend(item for item in model.contracts if all(item.id != entry.id for entry in entries))
        current_id = identifier(model.current.id) if model.current is not None else None
    else:
        entries, current_id = [model], None
    contracts = []
    for index, item in enumerate(entries):
        if contract_id is not None and item.id != str(contract_id):
            continue
        contracts.append(
            ContractSelection(
                index,
                identifier(item.id),
                item.name,
                identifier(getattr(item, "stage_id", None)),
                getattr(item, "stage_name", ""),
                getattr(item, "stage_recommended_level", None),
                item.best_score if "best_score" in item.model_fields_set else None,
                item.attempts if "attempts" in item.model_fields_set else None,
                source_datetime(item.starts_at),
                source_datetime(item.ends_at),
                source_datetime(item.ends_at_collection),
                tuple(info for meter in item.missions if (info := meter_info(meter)) is not None),
                tuple(
                    RunSelection(
                        run_index,
                        identifier(run.id),
                        source_datetime(run.completed_at),
                        run.duration_seconds,
                        run.score,
                        run.waves,
                    )
                    for run_index, run in enumerate(item.runs)
                ),
                tuple(
                    EntrySelection(entry_index, identifier(modifier.id), modifier.name)
                    for entry_index, modifier in enumerate(item.modifiers)
                ),
                tuple(
                    EntrySelection(entry_index, identifier(enemy.id), enemy.name)
                    for entry_index, enemy in enumerate(item.enemies)
                ),
            )
        )
    return ContractInfo(context.owner, current_id, tuple(contracts))


def render_info(family: str, model: Any, context: RenderContext, **options: Any) -> RenderInfo:
    from endfield_cards.rendering.registry import ALIASES

    family = ALIASES.get(family, family)
    if family in {"profile", "roster"}:
        return character_info(model, context, family=family, character_ids=options.get("character_ids"))
    if family == "activity":
        return live_info(model, context)
    if family in {"monument", "monument_detail"}:
        return monument_info(model, context, options.get("event_id"))
    if family in {"contingency_contract", "contingency_contract_detail"}:
        return contract_info(model, context, options.get("contract_id"))
    return None


def bundle_render(
    family: str, model: Any, cards: Sequence[CardResult], context: RenderContext, **options: Any
) -> RenderedCard[Any, RenderInfo]:
    return RenderedCard(cards, model, render_info(family, model, context, **options))
