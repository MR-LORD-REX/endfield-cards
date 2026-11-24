"""Resource dashboard with honest overflow values and source timestamps."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.rendering.components import PageCanvas

from ._records import (
    Record,
    append_model_text,
    fit_label,
    iter_records,
    meter_text,
    progress,
    record_page_count,
    stamp,
)


def urls(model: Any) -> set[str]:
    return set()


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    meters = [
        (name, getattr(model, name))
        for name in ("daily", "weekly", "battle_pass", "credits")
        if getattr(model, name) is not None
    ]
    meters.extend((meter.key or "activity", meter) for meter in model.activities)
    groups = [meters[i : i + 4] for i in range(0, len(meters), 4)] or [[]]
    details = []
    for name, meter in [("Sanity", model.sanity), *meters]:
        if meter is not None:
            lines = [
                meter_text(meter),
                f"Recovery: {stamp(meter.recovery_at)}",
                f"Refresh: {stamp(meter.refresh_at)}",
            ]
            if meter.note:
                lines.append(meter.note)
            details.append(Record(meter.name or name, lines))
    if model.current_event:
        lines = []
        append_model_text(lines, model.current_event)
        details.append(Record("Current event", lines, "player.monument"))
    total_pages = len(groups) + (record_page_count(context, details) if details else 0)
    for page, group in enumerate(groups, 1):
        canvas = PageCanvas("ACTIVITY", context, dark=variant == "dark", size=(1600, 1000), assets=assets)
        canvas.icon("player.activity", 1430, 145, size=80)
        canvas.text(56, 142, "Snapshot " + stamp(model.server_time), size=22, fill=canvas.muted)
        canvas.panel((56, 205, 582, 876))
        canvas.text(92, 237, "SANITY", size=24, bold=True)
        meter = model.sanity
        x, y, diameter = 157, 329, 320
        canvas.draw.arc((x, y, x + diameter, y + diameter), -90, 270, fill="#4B4D53", width=26)
        ratio = min(1.0, max(0.0, meter.ratio)) if meter is not None else 0
        if ratio:
            canvas.draw.arc(
                (x, y, x + diameter, y + diameter), -90, -90 + 360 * ratio, fill=canvas.accent, width=26
            )
        canvas.text(
            x + 69,
            y + 104,
            str(int(meter.current)) if meter is not None else "—",
            size=86,
            bold=True,
            width=240,
            max_lines=1,
        )
        canvas.text(x + 83, y + 205, f"/ {meter.maximum:g}" if meter is not None else "Not supplied", size=29)
        if meter is not None:
            canvas.text(92, 717, "Recovery " + stamp(meter.recovery_at), size=22, width=448)
            if meter.note:
                note, note_size, _ = fit_label(meter.note, 448, locale=context.locale, size=22, minimum=18)
                canvas.text(92, 790, note, size=note_size)
        for index, (key, item) in enumerate(group):
            row, col = divmod(index, 2)
            px, py = 608 + col * 480, 205 + row * 345
            canvas.panel((px, py, px + 454, py + 321))
            title, title_size, _ = fit_label(
                (item.name or key.replace("_", " ")).upper(), 398, locale=context.locale, size=24, minimum=18
            )
            canvas.text(px + 28, py + 24, title, size=title_size, bold=True)
            canvas.text(px + 28, py + 92, meter_text(item), size=44, bold=True, width=398)
            progress(canvas, item.ratio, px + 28, py + 194, 398, 15)
            note, note_size, _ = fit_label(
                item.note or ("Complete" if item.complete else "In progress"),
                398,
                locale=context.locale,
                size=22,
                minimum=18,
            )
            canvas.text(px + 28, py + 230, note, size=note_size)
        if not group:
            canvas.text(640, 255, "No task progression supplied", size=30, fill=canvas.muted)
        yield canvas.finish(page=page, pages=total_pages)
    if details:
        yield from iter_records(
            "ACTIVITY DETAILS",
            context,
            details,
            variant=variant,
            assets=assets,
            page_offset=len(groups),
            total_pages=total_pages,
        )


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
