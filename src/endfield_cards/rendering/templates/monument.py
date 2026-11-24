"""Monument overview with event art, medal state and both difficulty counters."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.rendering.components import PageCanvas

from ._records import Record, fit_label, iter_records, photo, progress, record_page_count


def urls(model: Any) -> set[str]:
    links = [image_url(event.poster) for event in model.events]
    links.extend(image_url(event.medal.icon) for event in model.events if event.medal is not None)
    return {link for link in links if link}


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    groups = [model.events[i : i + 4] for i in range(0, len(model.events), 4)] or [[]]
    names = {}
    detail_records = []
    for event in model.events:
        label, label_size, shortened = fit_label(event.name or event.id, 310, locale=context.locale, size=32)
        names[event.id] = label, label_size
        if shortened:
            detail_records.append(Record("Monument event", [event.name or event.id, f"Event ID: {event.id}"]))
    total_pages = len(groups) + (record_page_count(context, detail_records) if detail_records else 0)
    for page, group in enumerate(groups, 1):
        canvas = PageCanvas("MONUMENT", context, dark=variant == "dark", size=(1600, 1000), assets=assets)
        canvas.icon("player.monument", 1400, 134, size=70)
        total_stages = sum(len(event.stages) for event in model.events)
        normal = sum(stage.normal_cleared for event in model.events for stage in event.stages)
        hard = sum(stage.hard_cleared for event in model.events for stage in event.stages)
        canvas.text(
            56,
            140,
            f"{len(model.events)} events · Normal {normal}/{total_stages} · Hard {hard}/{total_stages}",
            size=25,
            fill=canvas.muted,
        )
        if not group:
            canvas.text(56, 250, "No monument events supplied", size=34)
        for index, event in enumerate(group):
            x, y, width = 56 + index * 378, 208, 354
            canvas.panel((x, y, x + width, 884))
            photo(canvas, image_url(event.poster), (x + 2, y + 2, x + width - 2, y + 300), assets)
            if event.is_active:
                canvas.draw.rectangle((x + 18, y + 20, x + 131, y + 55), fill=canvas.accent)
                canvas.text(x + 31, y + 26, "ACTIVE", size=20, fill="#1A1C21", bold=True)
            label, label_size = names[event.id]
            canvas.text(x + 22, y + 322, label, size=label_size, bold=True)
            total = len(event.stages)
            for offset, label, count in (
                (435, "NORMAL", sum(stage.normal_cleared for stage in event.stages)),
                (520, "HARD", sum(stage.hard_cleared for stage in event.stages)),
            ):
                canvas.text(x + 22, y + offset, f"{label}   {count}/{total}", size=25, bold=True)
                progress(canvas, count / total if total else 0, x + 22, y + offset + 46, width - 44)
            if event.medal is not None:
                photo(
                    canvas,
                    image_url(event.medal.icon),
                    (x + width - 99, y + 592, x + width - 22, y + 662),
                    assets,
                    contain=True,
                )
                canvas.text(x + 22, y + 601, f"Medal Lv {event.medal.level}", size=23, width=230)
                if event.medal.plated:
                    canvas.text(x + 22, y + 636, "PLATED", size=18, fill=canvas.accent)
            else:
                canvas.text(x + 22, y + 602, "Medal not supplied", size=22)
        yield canvas.finish(page=page, pages=total_pages)
    if detail_records:
        yield from iter_records(
            "MONUMENT DETAILS",
            context,
            detail_records,
            variant=variant,
            assets=assets,
            page_offset=len(groups),
            total_pages=total_pages,
        )


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
