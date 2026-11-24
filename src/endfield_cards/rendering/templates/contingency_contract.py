"""Contingency Contract score, medal and source-provided mission dashboard."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.rendering.components import PageCanvas

from ._records import Record, fit_label, iter_records, meter_text, photo, progress, record_page_count, stamp


def contracts(model: Any) -> list[Any]:
    if not hasattr(model, "contracts"):
        return [model]
    result = [model.current] if model.current is not None else []
    result.extend(item for item in model.contracts if all(item.id != existing.id for existing in result))
    return result


def urls(model: Any) -> set[str]:
    links = [image_url(item.poster) for item in contracts(model)]
    links.extend(image_url(item.medal.icon) for item in contracts(model) if item.medal is not None)
    return {link for link in links if link}


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    entries: list[tuple[Any, list[Any]]] = []
    detail_records = []
    for item in contracts(model):
        groups = [item.missions[i : i + 6] for i in range(0, len(item.missions), 6)] or [[]]
        entries.extend((item, group) for group in groups)
        if fit_label(item.name or item.id, 1100, locale=context.locale, size=57, max_lines=2)[2]:
            detail_records.append(
                Record("Contract identity", [item.name or item.id, f"Contract ID: {item.id}"])
            )
        for mission in item.missions:
            if fit_label(mission.name or mission.key, 260, locale=context.locale, size=20, max_lines=1)[2]:
                detail_records.append(Record("Mission", [mission.name or mission.key, meter_text(mission)]))
    if not entries:
        canvas = PageCanvas("CONTINGENCY CONTRACT", context, dark=variant == "dark", assets=assets)
        canvas.text(56, 250, "No Contingency Contract supplied", size=36)
        yield canvas.finish()
        return
    total_pages = len(entries) + (record_page_count(context, detail_records) if detail_records else 0)
    for index, (item, missions) in enumerate(entries):
        canvas = PageCanvas("CONTINGENCY CONTRACT", context, dark=variant == "dark", assets=assets)
        canvas.icon("player.contingency-contract", 1420, 143, size=75)
        canvas.panel((56, 205, 1544, 445))
        photo(canvas, image_url(item.poster), (57, 206, 1543, 444), assets)
        shade = Image.new("RGBA", (1486, 238), "#161A20")
        alpha = Image.new("L", (1486, 1))
        alpha.putdata([int(240 * (1 - x / 1486)) for x in range(1486)])
        shade.putalpha(alpha.resize(shade.size))
        canvas.image.alpha_composite(shade, (57, 206))
        canvas.text(
            88,
            238,
            "CURRENT CONTRACT" if getattr(model, "current", None) is item else "CONTRACT RECORD",
            size=21,
            fill=canvas.accent,
            bold=True,
        )
        label, label_size, _ = fit_label(
            item.name or item.id, 1100, locale=context.locale, size=57, max_lines=2
        )
        canvas.text(88, 280, label, size=label_size, fill="#F4F3EE", bold=True)
        canvas.panel((56, 472, 458, 894))
        canvas.text(88, 503, "BEST SCORE", size=24, fill=canvas.muted, bold=True)
        canvas.text(84, 554, str(item.best_score), size=136, bold=True, width=350, max_lines=1)
        canvas.text(88, 753, f"{item.attempts} attempts", size=29)
        canvas.text(88, 810, "Ends " + stamp(item.ends_at), size=19, width=344)
        canvas.panel((1128, 472, 1544, 894))
        canvas.text(1160, 503, "MEDAL", size=24, fill=canvas.muted, bold=True)
        if item.medal is not None:
            photo(canvas, image_url(item.medal.icon), (1230, 574, 1444, 788), assets, contain=True)
            canvas.text(
                1160,
                814,
                f"{item.medal.name or 'Medal'} · Lv {item.medal.level}"
                + (" · Plated" if item.medal.plated else ""),
                size=23,
                width=352,
            )
        else:
            canvas.text(1160, 628, "Not supplied", size=30)
        canvas.panel((482, 472, 1104, 894))
        canvas.text(512, 503, "MISSIONS", size=24, fill=canvas.muted, bold=True)
        for i, mission in enumerate(missions):
            row, col = divmod(i, 2)
            x, y = 512 + col * 293, 566 + row * 104
            label, label_size, _ = fit_label(
                mission.name or mission.key, 260, locale=context.locale, size=20, max_lines=1
            )
            canvas.text(x, y, label, size=label_size)
            canvas.text(x, y + 31, meter_text(mission), size=24, bold=True, width=260)
            progress(canvas, mission.ratio, x, y + 74, 260)
        if not missions:
            canvas.text(512, 592, "No mission progress supplied", size=25, width=530)
        yield canvas.finish(page=index + 1, pages=total_pages)
    if detail_records:
        yield from iter_records(
            "CONTINGENCY CONTRACT DETAILS",
            context,
            detail_records,
            variant=variant,
            assets=assets,
            page_offset=len(entries),
            total_pages=total_pages,
        )


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
