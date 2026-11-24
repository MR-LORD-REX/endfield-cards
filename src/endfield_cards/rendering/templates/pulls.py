"""Observed pull-history pages without inventing absent pity or guarantees."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.rendering.components import PageCanvas

from ._records import Record, fit_label, iter_records, photo, record_page_count, stamp


def urls(model: Any) -> set[str]:
    return {url for record in model.records if (url := image_url(record.item.icon))}


def _details(model: Any, context: Any) -> list[Record]:
    records = []
    if hasattr(model, "from_time"):
        records.append(
            Record(
                "History window",
                [
                    f"From: {stamp(model.from_time)}",
                    f"To: {stamp(model.to_time)}",
                    "Complete history"
                    if model.complete_history
                    else "Partial history; absent records and pity cannot be inferred",
                ],
            )
        )
    for pity in getattr(model, "pity", []):
        lines = [f"Observed current: {pity.current}", f"Total supplied: {pity.total}"]
        lines.append(
            f"Hard limit: {pity.hard_limit}" if pity.hard_limit is not None else "Hard limit: Not supplied"
        )
        lines.append(
            f"Featured guarantee: {pity.featured_guarantee}"
            if pity.featured_guarantee is not None
            else "Featured guarantee: Not supplied"
        )
        records.append(Record(pity.name or pity.banner_id, lines))
    known_drops = [record for record in model.records if record.pity_at_drop is not None]
    if known_drops:
        records.append(
            Record(
                "Observed pity at drop",
                [
                    f"{record.item.name or record.item.id} · {record.banner_name or record.banner_id}: {record.pity_at_drop}"
                    for record in known_drops
                ],
            )
        )
    for record in model.records:
        name = record.item.name or record.item.id
        banner = record.banner_name or record.banner_id
        shortened_name = fit_label(name, 460, locale=context.locale, size=27, minimum=18, max_lines=1)[2]
        shortened_banner = fit_label(banner, 370, locale=context.locale, size=22, minimum=18, max_lines=1)[2]
        if shortened_name or shortened_banner:
            records.append(Record("Pull record", [name, banner, f"Pulled: {stamp(record.pulled_at)}"]))
    return records


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    groups = [model.records[i : i + 9] for i in range(0, len(model.records), 9)] or [[]]
    details = _details(model, context)
    total_pages = len(groups) + (record_page_count(context, details) if details else 0)
    for page, group in enumerate(groups, 1):
        canvas = PageCanvas("PULL HISTORY", context, dark=variant == "dark", assets=assets)
        complete = getattr(model, "complete_history", False)
        canvas.text(
            56,
            143,
            "Complete supplied history" if complete else "Partial history · supplied window",
            size=24,
            fill=canvas.muted,
        )
        if hasattr(model, "totals"):
            totals = model.totals
            canvas.text(
                56,
                190,
                f"Characters {totals.character_draws}   Weapons {totals.weapon_draws}   Free {totals.free_draws}   Six-star {totals.six_star_draws}",
                size=26,
                bold=True,
            )
        else:
            canvas.text(
                56, 190, "More records available" if model.has_more else "End of supplied page", size=24
            )
        canvas.panel((56, 247, 1544, 899))
        for index, record in enumerate(group):
            y = 270 + index * 66
            photo(canvas, image_url(record.item.icon), (76, y, 128, y + 52), assets, contain=True)
            item_name, item_size, _ = fit_label(
                record.item.name or record.item.id,
                460,
                locale=context.locale,
                size=27,
                minimum=18,
                max_lines=1,
            )
            banner_name, banner_size, _ = fit_label(
                record.banner_name or record.banner_id,
                370,
                locale=context.locale,
                size=22,
                minimum=18,
                max_lines=1,
            )
            canvas.text(148, y + 4, item_name, size=item_size, bold=True)
            canvas.text(626, y + 7, banner_name, size=banner_size)
            rarity = record.rarity if record.rarity is not None else record.item.rarity
            canvas.text(
                1015,
                y + 5,
                str(rarity) if rarity is not None else "—",
                size=26,
                fill=canvas.accent if rarity == 6 else canvas.fg,
                bold=True,
            )
            if rarity is not None:
                canvas.icon("rarity.star", 1048, y + 10, size=22)
            canvas.text(1118, y + 10, stamp(record.pulled_at), size=17, width=260, max_lines=1)
            canvas.text(
                1420,
                y + 5,
                f"×{record.count}" + (" FREE" if record.is_free else ""),
                size=21,
                width=105,
                max_lines=1,
            )
            canvas.draw.line((76, y + 60, 1524, y + 60), fill=canvas.line, width=1)
        if not group:
            canvas.text(88, 307, "No pull records supplied", size=32)
        yield canvas.finish(page=page, pages=total_pages)
    if details:
        yield from iter_records(
            "PULL HISTORY DETAILS",
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
