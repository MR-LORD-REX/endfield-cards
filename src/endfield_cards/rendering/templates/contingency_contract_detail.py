"""Complete Contingency Contract rules, records, teams, indicators and enemies."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.errors import DataValidationError

from ._records import (
    Record,
    append_model_text,
    iter_records,
    medal_lines,
    meter_text,
    run_lines,
    stamp,
    team_images,
)
from .contingency_contract import contracts


def _selected(model: Any, contract_id: str | None = None) -> list[Any]:
    selected = contracts(model)
    if contract_id is not None:
        selected = [item for item in selected if item.id == str(contract_id)]
        if not selected:
            raise DataValidationError(
                "Selected Contingency Contract is absent from this snapshot", code="contract_not_found"
            )
    return selected


def urls(model: Any) -> set[str]:
    links = []
    for item in _selected(model):
        links.append(image_url(item.poster))
        links.extend(image_url(modifier.icon) for modifier in item.modifiers)
        links.extend(image_url(enemy.icon) for enemy in item.enemies)
        links.extend(url for run in item.runs for url, _ in team_images(run))
    return {link for link in links if link}


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    records = []
    for item in _selected(model, options.get("contract_id")):
        lines = [
            f"Best score: {item.best_score} · Attempts: {item.attempts}",
            f"Starts: {stamp(item.starts_at)}",
            f"Ends: {stamp(item.ends_at)}",
            f"Collection ends: {stamp(item.ends_at_collection)}",
            *medal_lines(item.medal),
        ]
        if item.rules:
            lines.append(item.rules)
        records.append(
            Record(
                item.name or item.id,
                lines,
                "player.contingency-contract",
                [(image_url(item.poster), item.name)],
            )
        )
        for mission in item.missions:
            lines = [meter_text(mission)]
            if mission.note:
                lines.append(mission.note)
            if mission.refresh_at:
                lines.append("Refresh: " + stamp(mission.refresh_at))
            records.append(Record(mission.name or mission.key, lines))
        for run in item.runs:
            records.append(Record(f"Run {run.id or 'record'}", run_lines(run), images=team_images(run)))
        for modifier in item.modifiers:
            lines = [f"Score: {modifier.score} · {'Unlocked' if modifier.is_unlocked else 'Locked'}"]
            if modifier.description:
                lines.append(modifier.description)
            append_model_text(lines, modifier.params)
            records.append(
                Record(
                    modifier.name or modifier.id, lines, images=[(image_url(modifier.icon), modifier.name)]
                )
            )
        for enemy in item.enemies:
            lines = []
            if enemy.level is not None:
                lines.append(f"Level: {enemy.level}")
            if enemy.description:
                lines.append(enemy.description)
            if enemy.ability:
                lines.append(enemy.ability)
            records.append(
                Record(enemy.name or enemy.id, lines, images=[(image_url(enemy.icon), enemy.name)])
            )
    yield from iter_records("CONTINGENCY CONTRACT DETAILED", context, records, variant=variant, assets=assets)


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    """Collect the explicitly requested render batch."""
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
