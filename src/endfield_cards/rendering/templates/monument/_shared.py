"""Observed Monument overview planning, artwork, medals and stage status."""

from __future__ import annotations

import math
from collections.abc import Iterator
from importlib import import_module
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.errors import DataValidationError
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import composite_fitted, fitted
from endfield_cards.utils.records import Record, duration, iter_records, record_page_count

WIDTH = 1600
PAD = 36
GAP = 18
TOP = 216
PER_PAGE = 12
LIGHT_HEIGHT = 590
DARK_HEIGHT = 286
HARD = "#DA786A"
Box = tuple[int, int, int, int]


def text(c: PageCanvas, x: int, y: int, value: object, width: int, *, size: int = 20, **options: Any) -> None:
    c.text(x, y, value, width=width, size=size, max_lines=options.pop("max_lines", 1), **options)


def events(model: Any) -> list[Any]:
    entries = list(model.events)
    identifiers = [item.id for item in entries if item.id]
    if len(set(identifiers)) != len(identifiers):
        raise DataValidationError("Monument contains duplicate event identities", code="duplicate_event")
    return entries


def page_size(count: int, variant: str) -> tuple[int, int]:
    if count == 0:
        return WIDTH, 700
    columns, height = (4, LIGHT_HEIGHT) if variant == "light" else (2, DARK_HEIGHT)
    rows = max(1, math.ceil(count / columns))
    return WIDTH, max(700, TOP + rows * (height + GAP) - GAP + 86)


def urls(model: Any) -> set[str]:
    links = [image_url(event.poster) for event in model.events]
    links.extend(image_url(event.medal.icon) for event in model.events if event.medal is not None)
    return {link for link in links if link}


def totals(entries: list[Any]) -> list[tuple[str, str]]:
    stages = [stage for event in entries for stage in event.stages]
    medals = [event.medal for event in entries if event.medal is not None]
    earned = sum(medal.level > 0 for medal in medals)
    medal_count = str(earned) if len(medals) == len(entries) else f"{earned} known" if medals else "—"
    return [
        ("EVENTS", str(len(entries))),
        ("NORMAL", f"{sum(stage.normal_cleared for stage in stages)}/{len(stages)}"),
        ("HARD", f"{sum(stage.hard_cleared for stage in stages)}/{len(stages)}"),
        ("EARNED MEDALS", medal_count),
    ]


def draw_header(c: PageCanvas, model: Any, entries: list[Any], profile: Any = None) -> None:
    c.icon("player.monument", 43, 39, 31, tint=c.accent if c.dark else "#916900")
    text(c, 86, 37, "ENDFIELD / MONUMENT", 590, size=22, bold=True)
    source = image_url(profile.avatar) if profile is not None else None
    pixels = c.assets.get(source) if source else None
    c.draw.ellipse((41, 90, 125, 174), fill=c.accent)
    if pixels is not None:
        composite_fitted(c.image, pixels, (46, 95, 120, 169), shape="circle", focus=(0.5, 0.25))
    else:
        c.draw.ellipse((46, 95, 120, 169), fill=c.panel_color)
        text(c, 67, 106, c.context.owner.name[:1], 45, size=34, bold=True)
    text(c, 145, 84, c.context.owner.name, 500, size=43, bold=True)
    identity = f"UID {c.context.owner.game_uid}"
    if profile is not None:
        if profile.server_name:
            identity += " · " + profile.server_name
        if "authority_level" in profile.model_fields_set:
            identity += f" · Authority {profile.authority_level}"
    text(c, 147, 142, identity, 530, size=17, fill=c.muted)
    for index, (label, value) in enumerate(totals(entries)):
        x = 738 + index * 207
        c.draw.line((x - 13, 98, x - 13, 167), fill=c.line)
        text(c, x, 94, label, 190, size=13, fill=HARD if label == "HARD" else c.muted, bold=True)
        text(c, x - 1, 118, value, 192, size=33, bold=True)
    c.draw.line((PAD, 190, c.width - PAD, 190), fill=c.line)


def draw_art(c: PageCanvas, event: Any, box: Box, *, clipped: bool = False) -> None:
    x, y, right, bottom = box
    c.draw.rounded_rectangle(box, radius=12, fill="#232A33")
    source = image_url(event.poster)
    pixels = c.assets.get(source) if source else None
    if pixels is None:
        text(
            c,
            x + 15,
            y + (bottom - y) // 2 - 13,
            "Artwork unavailable",
            right - x - 30,
            size=16,
            fill="#B2BBC6",
        )
        return
    composite_fitted(
        c.image,
        pixels,
        box,
        shape="clipped" if clipped else "top-rounded",
        radius=12,
        cut=16,
        focus=(0.5, 0.28),
    )


def draw_medal(c: PageCanvas, event: Any, box: Box) -> None:
    x, y, right, bottom = box
    width, height = right - x, bottom - y
    c.draw.rounded_rectangle(
        box,
        radius=10,
        fill=c.panel_color,
        outline=c.accent if event.medal is not None and event.medal.plated else c.line,
        width=2,
    )
    medal = event.medal
    if medal is None:
        text(c, x + 5, y + height // 2 - 10, "—", width - 10, size=18, fill=c.muted)
        return
    source = image_url(medal.icon)
    pixels = c.assets.get(source) if source else None
    if pixels is not None:
        glyph = fitted(pixels, (width - 8, height - 23), contain=True)
        c.image.alpha_composite(glyph, (x + 4, y + 3))
    text(
        c,
        x + 6,
        bottom - 21,
        f"Lv {medal.level}" + (" · P" if medal.plated else ""),
        width - 12,
        size=11,
        fill=c.accent if c.dark and medal.plated else c.muted,
    )


def fastest(event: Any) -> float | None:
    values = []
    for stage in event.stages:
        for run, cleared in ((stage.normal, stage.normal_cleared), (stage.hard, stage.hard_cleared)):
            if run is not None and (run.completed or cleared) and run.duration_seconds is not None:
                values.append(run.duration_seconds)
    return min(values) if values else None


def draw_state(c: PageCanvas, event: Any, index: int, x: int, y: int, *, active_x: int | None = None) -> None:
    c.draw.rounded_rectangle((x, y, x + 39, y + 29), radius=7, fill="#171D25")
    text(c, x + 7, y + 4, f"{index:02d}", 28, size=15, bold=True, fill="#F4F4F6")
    if event.is_active:
        ax = active_x if active_x is not None else x + 48
        c.draw.rounded_rectangle((ax, y, ax + 66, y + 29), radius=7, fill=c.accent)
        text(c, ax + 8, y + 5, "ACTIVE", 52, size=12, bold=True, fill="#171D25")


def draw_stage_table(
    c: PageCanvas, event: Any, x: int, y: int, width: int, *, maximum: int = 6, row_height: int = 21
) -> None:
    text(c, x, y - 24, "STAGE", width - 76, size=11, bold=True, fill=c.muted)
    text(c, x + width - 60, y - 24, "N", 24, size=11, bold=True, fill=c.muted)
    text(c, x + width - 28, y - 24, "H", 24, size=11, bold=True, fill=HARD)
    visible = event.stages[:maximum] if len(event.stages) <= maximum else event.stages[: maximum - 1]
    for index, stage in enumerate(visible):
        py = y + index * row_height
        text(
            c,
            x,
            py,
            f"{index + 1:02d}  {stage.name or stage.id or 'Unavailable'}",
            width - 76,
            size=12,
            fill=c.muted,
        )
        for clear, px, color in (
            (stage.normal_cleared, x + width - 60, c.fg),
            (stage.hard_cleared, x + width - 28, HARD),
        ):
            c.draw.rounded_rectangle(
                (px + 1, py + 4, px + 13, py + 16), radius=3, fill=color if clear else c.line
            )
    if len(event.stages) > len(visible):
        text(
            c,
            x,
            y + len(visible) * row_height,
            f"+{len(event.stages) - len(visible)} stages",
            width - 76,
            size=12,
            fill=c.muted,
        )
    if not event.stages:
        text(c, x, y + 4, "No stage records supplied", width, size=14, fill=c.muted)


def draw_counts(c: PageCanvas, event: Any, x: int, y: int, width: int) -> None:
    total = len(event.stages)
    left = sum(stage.normal_cleared for stage in event.stages)
    right = sum(stage.hard_cleared for stage in event.stages)
    text(c, x, y, f"Normal {left}/{total}", width // 2, size=16, bold=True)
    text(
        c,
        x + width // 2,
        y,
        f"Hard {right}/{total}",
        width - width // 2,
        size=16,
        bold=True,
        fill=HARD if c.dark else "#A3463B",
    )


def draw_fastest(c: PageCanvas, event: Any, x: int, y: int, width: int) -> None:
    observed = fastest(event)
    text(
        c,
        x,
        y,
        "Fastest clear " + duration(observed) if observed is not None else "Clear time unavailable",
        width,
        size=13,
        fill=c.muted,
    )


def detail_records(entries: list[Any]) -> list[Record]:
    result = []
    for index, event in enumerate(entries, 1):
        lines = [f"Event {index:02d} · ID {event.id}", *event.rules]
        for stage_index, stage in enumerate(event.stages, 1):
            lines.append(f"{stage_index:02d} · {stage.name or stage.id} · ID {stage.id}")
            lines.append(f"Normal {stage.normal_id or 'Unavailable'} · Hard {stage.hard_id or 'Unavailable'}")
        result.append(Record(event.name or event.id or "Monument event", lines))
    return result


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: dict | None = None,
    profile: Any = None,
    event_id: str | None = None,
    details: bool = False,
    **options: Any,
) -> Iterator[Image.Image]:
    entries = events(model)
    if event_id is not None:
        entries = [event for event in entries if event.id == str(event_id)]
        if not entries:
            raise DataValidationError(
                "Selected Monument event is absent from this snapshot", code="event_not_found"
            )
    if profile is not None:
        validate_owner(profile, context)
    groups = [entries[index : index + PER_PAGE] for index in range(0, len(entries), PER_PAGE)] or [[]]
    records = detail_records(entries) if details else []
    total = len(groups) + (record_page_count(context, records) if records else 0)
    module = import_module(f"endfield_cards.rendering.templates.monument.{variant}")
    for page, group in enumerate(groups, 1):
        yield module.render_page(
            model,
            context,
            entries=group,
            all_events=entries,
            offset=(page - 1) * PER_PAGE,
            assets=assets,
            profile=profile,
            page=page,
            pages=total,
        )
    if records:
        yield from iter_records(
            "Monument records",
            context,
            records,
            variant=variant,
            assets=assets,
            page_offset=len(groups),
            total_pages=total,
        )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
