"""Selected Monument events, full stage runs, teams, enemies and rules."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.errors import DataValidationError

from ._records import Record, iter_records, medal_lines, run_lines, stamp, team_images


def _events(model: Any, event_id: str | None = None) -> list[Any]:
    events = list(model.events) if hasattr(model, "events") else [model]
    if event_id is not None:
        events = [event for event in events if event.id == str(event_id)]
        if not events:
            raise DataValidationError(
                "Selected Monument event is absent from this snapshot", code="event_not_found"
            )
    return events


def urls(model: Any) -> set[str]:
    links = []
    for event in _events(model):
        links.append(image_url(event.poster))
        if event.medal is not None:
            links.append(image_url(event.medal.icon))
        for stage in event.stages:
            links.extend(image_url(enemy.icon) for enemy in stage.enemies)
            for run in (stage.normal, stage.hard):
                if run is not None:
                    links.extend(url for url, _ in team_images(run))
    return {link for link in links if link}


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    records = []
    for event in _events(model, options.get("event_id")):
        lines = [
            "Active" if event.is_active else "Inactive",
            f"Starts: {stamp(event.starts_at)}",
            f"Ends: {stamp(event.ends_at)}",
            *medal_lines(event.medal),
            *event.rules,
        ]
        records.append(
            Record(
                event.name or event.id,
                lines,
                "player.monument-event",
                [(image_url(event.poster), event.name)],
            )
        )
        for stage in event.stages:
            level = (
                f"Recommended level: {stage.recommended_level}"
                if stage.recommended_level is not None
                else "Recommended level not supplied"
            )
            records.append(
                Record(
                    stage.name or stage.id,
                    [
                        level,
                        f"Normal: {'Cleared' if stage.normal_cleared else 'Not cleared'}",
                        f"Hard: {'Cleared' if stage.hard_cleared else 'Not cleared'}",
                    ],
                )
            )
            for difficulty, run in (("Normal", stage.normal), ("Hard", stage.hard)):
                if run is not None:
                    records.append(
                        Record(
                            f"{stage.name or stage.id} · {difficulty}",
                            run_lines(run),
                            images=team_images(run),
                        )
                    )
            for enemy in stage.enemies:
                lines = []
                if enemy.level is not None:
                    lines.append(f"Level: {enemy.level}")
                if enemy.description:
                    lines.append(enemy.description)
                if enemy.ability:
                    lines.append(enemy.ability)
                records.append(
                    Record(
                        f"{stage.name or stage.id} · {enemy.name or enemy.id}",
                        lines,
                        images=[(image_url(enemy.icon), enemy.name)],
                    )
                )
    yield from iter_records("MONUMENT DETAILED", context, records, variant=variant, assets=assets)


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    """Collect the explicitly requested render batch."""
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
