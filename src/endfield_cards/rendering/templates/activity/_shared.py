"""Observed Live resources, event art and source-clock component rendering."""

from collections.abc import Iterator
from dataclasses import replace
from importlib import import_module
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.utils.activity import event_status, event_summaries
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import composite_fitted, fitted, masked, shape_mask
from endfield_cards.utils.meters import bar, ring
from endfield_cards.utils.records import (
    Record,
    append_model_text,
    iter_records,
    meter_text,
    number,
    record_page_count,
)
from endfield_cards.utils.time import display_time, remaining

SIZE = (1600, 1000)
METER_INFO = (
    ("daily", "Daily activity", "player.daily"),
    ("weekly", "Weekly routine", "player.activity"),
    ("battle_pass", "Battle pass", "player.development"),
    ("credits", "Credits", "player.room-reception"),
)
Box = tuple[int, int, int, int]


def text(
    c: PageCanvas,
    x: int,
    y: int,
    value: object,
    width: int,
    *,
    size: int = 20,
    bold: bool = False,
    muted: bool = False,
    color: str | None = None,
    lines: int = 1,
) -> None:
    c.text(
        x,
        y,
        value,
        width=width,
        size=size,
        bold=bold,
        fill=color or (c.muted if muted else c.fg),
        max_lines=lines,
    )


def signal(c: PageCanvas) -> str:
    return c.accent if c.dark else "#916900"


def center(c: PageCanvas, x: int, y: int, value: str, width: int, *, size: int, **options: Any) -> None:
    font = c.fonts.get(
        size, weight="semibold" if options.get("bold") else "regular", locale=c.context.locale, text=value
    )
    offset = max(0, int((width - c.draw.textlength(value, font=font)) / 2))
    text(c, x + offset, y, value, width - offset, size=size, **options)


def urls(model: Any) -> set[str]:
    return {item.poster for item in event_summaries(model) if item is not None and item.poster}


def draw_header(c: PageCanvas, model: Any, profile: Any = None) -> None:
    c.draw.line((40, 153, 1560, 153), fill=c.line)
    c.draw.line((40, 14, 149, 14), fill=c.accent, width=4)
    avatar = image_url(profile.avatar) if profile is not None else None
    source = c.assets.get(avatar) if avatar else None
    c.draw.ellipse((41, 36, 143, 138), fill=c.accent)
    if source is not None:
        composite_fitted(c.image, source, (46, 41, 138, 133), shape="circle", focus=(0.5, 0.25))
    else:
        c.draw.ellipse((46, 41, 138, 133), fill=c.panel_color)
        center(c, 46, 59, c.context.owner.name[:1], 92, size=46, bold=True)
    text(c, 166, 39, c.context.owner.name, 915, size=50, bold=True)
    identity = f"UID {c.context.owner.game_uid}"
    if profile is not None:
        if profile.server_name:
            identity += " · " + profile.server_name
        if "authority_level" in profile.model_fields_set:
            identity += f" · Authority {profile.authority_level}"
    text(c, 168, 107, identity, 905, size=21, muted=True)
    text(c, 1218, 42, "LIVE STATUS", 342, size=24, bold=True, color=signal(c))
    text(c, 1104, 91, display_time(model.server_time, c.context), 456, size=20, muted=True)
    text(c, 1218, 120, "SOURCE SNAPSHOT", 342, size=13, muted=True)
    if model.activities:
        items = [f"{meter.name or meter.key}: {meter_text(meter)}" for meter in model.activities[:4]]
        if len(model.activities) > 4:
            items.append(f"+{len(model.activities) - 4} activities")
        text(c, 40, 161, " · ".join(items), 1520, size=13, muted=True)


def draw_sanity(c: PageCanvas, model: Any, box: Box, *, wide: bool = False) -> None:
    x, y, right, bottom = box
    c.panel(box)
    c.icon("player.sanity", x + 22, y + 22, 28, tint=signal(c))
    text(c, x + 61, y + 23, "Sanity", right - x - 86, size=23, bold=True)
    meter = model.sanity
    size = 233 if wide else 286
    gx, gy = x + 17 if wide else x + (right - x - size) // 2, y + 71 if wide else y + 126
    ring(c, gx, gy, size, meter.ratio if meter is not None else 0)
    value = number(meter.current) if meter is not None else "—"
    maximum = f"/ {number(meter.maximum)}" if meter is not None else "Unavailable"
    value_size = 65 if wide else 85
    value_bounds = c.fonts.get(value_size, weight="semibold", locale=c.context.locale, text=value).getbbox(
        value
    )
    maximum_bounds = c.fonts.get(23, locale=c.context.locale, text=maximum).getbbox(maximum)
    value_height = value_bounds[3] - value_bounds[1]
    maximum_height = maximum_bounds[3] - maximum_bounds[1]
    block_height = value_height + maximum_height + 13
    top = gy + (size - block_height) / 2
    c.centered_text((gx + 28, top, gx + size - 28, top + value_height), value, size=value_size, bold=True)
    c.centered_text(
        (gx + 28, top + value_height + 13, gx + size - 28, top + block_height), maximum, size=23, fill=c.muted
    )
    state = (
        "Unavailable"
        if meter is None
        else "Full"
        if meter.complete
        else "Recovering"
        if meter.recovery_at is not None
        else "Recovery unavailable"
    )
    tx, ty, width = (x + 270, y + 107, right - x - 286) if wide else (x + 25, gy + size + 48, right - x - 50)
    text(
        c,
        tx,
        ty,
        state,
        width,
        size=25,
        bold=True,
        color=signal(c) if meter is not None and meter.complete else c.muted,
    )
    if meter is not None and meter.current > meter.maximum and meter.maximum > 0:
        text(c, tx, ty + 44, "Above capacity", width, size=17, muted=True)
    if meter is not None and not meter.complete and meter.recovery_at is not None:
        text(
            c,
            tx,
            ty + 44,
            "Full in " + remaining(meter.recovery_at, model.server_time),
            width,
            size=18,
            muted=True,
        )
        if not wide:
            text(c, tx, ty + 79, display_time(meter.recovery_at, c.context), width, size=16, muted=True)
    if not wide:
        c.draw.line((tx, bottom - 137, right - 25, bottom - 137), fill=c.line)
        text(c, tx, bottom - 114, "RESOURCES", width, size=13, muted=True, bold=True)
        text(c, tx, bottom - 83, "Captured at source time", width, size=17, muted=True)
        text(c, tx, bottom - 54, display_time(model.server_time, c.context), width, size=16, muted=True)
    if meter is not None and meter.note:
        text(c, tx, min(bottom - 31, ty + 107), meter.note, width, size=14, muted=True)


def draw_meter(
    c: PageCanvas, model: Any, key: str, label: str, icon: str, box: Box, *, tall: bool = False
) -> None:
    x, y, right, bottom = box
    c.panel(box)
    c.icon(icon, x + 18, y + 20, 25, tint=signal(c), preserve_color=key == "credits")
    width = right - x - 36
    text(c, x + 53, y + 18, label, width - 35, size=18, bold=True)
    meter = getattr(model, key, None)
    text(
        c,
        x + 18,
        y + (79 if tall else 51),
        meter_text(meter) if meter is not None else "Unavailable",
        width,
        size=35 if tall else 33,
        bold=True,
    )
    bar(
        c,
        (x + 18, bottom - (73 if tall else 45), right - 18, bottom - (63 if tall else 37)),
        meter.ratio if meter is not None else 0,
    )
    note = "Unavailable" if meter is None else meter.note
    if meter is not None and meter.refresh_at is not None:
        note = (note + " · " if note else "") + "Refresh in " + remaining(meter.refresh_at, model.server_time)
    elif meter is not None and meter.recovery_at is not None:
        note = (
            (note + " · " if note else "") + "Recovery in " + remaining(meter.recovery_at, model.server_time)
        )
    elif meter is not None and not note:
        note = (
            "Complete" if meter.complete else "In progress" if meter.maximum > 0 else "Capacity unavailable"
        )
    text(
        c,
        x + 18,
        bottom - (48 if tall else 30),
        note,
        width,
        size=15 if tall else 13,
        muted=True,
        lines=2 if tall else 1,
    )
    if tall and meter is not None and meter.refresh_at is not None:
        text(
            c, x + 18, y + 146, display_time(meter.refresh_at, c.context), width, size=14, muted=True, lines=2
        )


def _event_panel(c: PageCanvas, box: Box, poster: str | None, *, dark: bool) -> None:
    x, y, right, bottom = box
    c.panel(box)
    source = c.assets.get(poster) if poster else None
    if source is not None:
        size = right - x, bottom - y
        pixels = fitted(source, size, focus=(0.5, 0.3))
        pixels.putalpha(pixels.getchannel("A").point(lambda alpha: alpha * (70 if dark else 26) // 255))
        c.image.alpha_composite(masked(pixels, shape_mask(size, radius=12)), (x, y))


def draw_echoes(c: PageCanvas, model: Any, box: Box) -> None:
    x, y, right, bottom = box
    echo, _ = event_summaries(model)
    _event_panel(c, box, echo.poster if echo is not None else None, dark=c.dark)
    c.icon("player.war-echoes", x + 20, y + 19, 28, tint=signal(c))
    text(c, x + 61, y + 20, "War Echoes", right - x - 83, size=21, bold=True)
    if echo is None:
        text(c, x + 23, y + 87, "No season supplied", right - x - 46, size=25, muted=True)
        return
    text(
        c,
        x + 23,
        y + 66,
        echo.cycle or echo.season or "Unavailable",
        right - x - 132,
        size=28,
        bold=True,
        lines=2,
    )
    if echo.cycle and echo.season:
        text(c, x + 23, y + 111, echo.season, right - x - 46, size=15, muted=True)
    c.icon("rarity.star", right - 44, y + 70, 22, tint=signal(c))
    text(c, right - 106, y + 65, number(echo.stars), 55, size=30, bold=True)
    top = y + 152
    visible = echo.stages[:4]
    for index, (name, stars, plus) in enumerate(visible):
        py = top + index * 34
        text(c, x + 23, py, name or "Unavailable", right - x - 111, size=17)
        text(c, right - 90, py - 1, number(stars), 40, size=22, bold=True)
        c.icon("rarity.star", right - 44, py + 3, 16, tint=signal(c))
        if plus is True:
            text(c, right - 123, py + 2, "+", 25, size=15, color=signal(c))
    if len(echo.stages) > len(visible):
        text(
            c,
            x + 23,
            top + 138,
            f"+{len(echo.stages) - len(visible)} stages",
            right - x - 46,
            size=13,
            muted=True,
        )
    elif echo.all_plus_tasks is True:
        text(c, x + 23, top + 138, "All bonus tasks complete", right - x - 46, size=14, color=signal(c))
    text(
        c,
        x + 23,
        bottom - 42,
        event_status(echo.starts_at, echo.ends_at, model.server_time),
        right - x - 46,
        size=17,
        muted=True,
    )


def draw_contract(c: PageCanvas, model: Any, box: Box) -> None:
    previous = c.panel_color, c.fg, c.muted, c.line
    c.panel_color, c.fg, c.muted, c.line = "#202832", "#F3F4F6", "#B0B9C5", "#3D4856"
    try:
        x, y, right, bottom = box
        _, contract = event_summaries(model)
        _event_panel(c, box, contract.poster if contract is not None else None, dark=True)
        c.icon("player.contingency-contract", x + 20, y + 19, 27, tint=c.accent)
        text(c, x + 61, y + 20, "Contingency Contract", right - x - 83, size=21, bold=True)
        if contract is None:
            text(c, x + 23, y + 87, "No contract supplied", right - x - 46, size=25, muted=True)
            return
        text(c, x + 23, y + 64, contract.name or "Unavailable", right - x - 46, size=25, bold=True, lines=2)
        text(c, x + 23, y + 138, "BEST", 105, size=13, muted=True)
        text(c, x + 23, y + 162, number(contract.score), 115, size=58, bold=True, color=c.accent)
        text(c, x + 23, y + 236, f"Attempts {number(contract.attempts)}", 143, size=13, muted=True)
        mx, width = x + 182, right - x - 205
        for index, (name, current, maximum) in enumerate(contract.missions[:3]):
            py = y + 139 + index * 51
            text(c, mx, py, name, width * 3 // 5, size=16, muted=True)
            text(
                c,
                mx + width * 3 // 5,
                py - 1,
                f"{number(current)} / {number(maximum)}",
                width * 2 // 5,
                size=20,
                bold=True,
            )
            bar(
                c,
                (mx, py + 29, mx + width, py + 35),
                current / maximum if current is not None and maximum is not None and maximum > 0 else 0,
            )
        text(
            c,
            x + 23,
            bottom - 42,
            event_status(contract.starts_at, contract.ends_at, model.server_time),
            right - x - 46,
            size=17,
            muted=True,
        )
    finally:
        c.panel_color, c.fg, c.muted, c.line = previous


def detail_records(model: Any) -> list[Record]:
    records = []
    for key in ("sanity", "daily", "weekly", "battle_pass", "credits"):
        meter = getattr(model, key, None)
        if meter is not None:
            lines = [meter_text(meter), meter.note]
            if meter.recovery_at is not None:
                lines.append("Recovery: " + meter.recovery_at.isoformat())
            if meter.refresh_at is not None:
                lines.append("Refresh: " + meter.refresh_at.isoformat())
            records.append(Record(meter.name or key, lines))
    records.extend(
        Record(meter.name or meter.key, [meter_text(meter), meter.note]) for meter in model.activities
    )
    if model.current_event:
        event_lines: list[str] = []
        append_model_text(event_lines, model.current_event)
        records.append(Record("Event records", event_lines))
    return records


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: dict | None = None,
    profile: Any = None,
    details: bool = False,
    **options: Any,
) -> Iterator[Image.Image]:
    context = replace(context, display_timezone="UTC")
    if profile is not None:
        validate_owner(profile, context)
    module = import_module(f"endfield_cards.rendering.templates.activity.{variant}")
    c = module.draw(model, context, assets=assets, profile=profile)
    records = detail_records(model) if details else []
    total = 1 + (record_page_count(context, records) if records else 0)
    yield c.finish(1, total)
    if records:
        yield from iter_records(
            "Live details", context, records, variant=variant, assets=assets, page_offset=1, total_pages=total
        )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
