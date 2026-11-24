"""Bounded character roster tiles retaining source order and scope."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.components import PageCanvas

from ._records import Record, fit_label, iter_records, photo, record_page_count


def _characters(model: Any) -> list[Any]:
    return list(model.characters if hasattr(model, "characters") else model)


def urls(model: Any) -> set[str]:
    return {
        url
        for item in _characters(model)
        if (url := image_url(item.images.portrait) or image_url(item.images.avatar))
    }


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    characters = _characters(model)
    wanted = options.get("character_ids")
    if wanted is not None:
        wanted = {str(value) for value in wanted}
        characters = [
            item for item in characters if item.identity.skport_id in wanted or item.identity.str_id in wanted
        ]
    if len({item.identity.skport_id for item in characters}) != len(characters):
        raise DataValidationError(
            "Roster contains duplicate character identities", code="duplicate_character"
        )
    groups = [characters[i : i + 12] for i in range(0, len(characters), 12)] or [[]]
    labels = {}
    detail_records = []
    for item in characters:
        name = item.name or item.identity.skport_id
        title, title_size, title_shortened = fit_label(name, 170, locale=context.locale)
        profession = item.profession.name or item.profession.key
        caption, caption_size, caption_shortened = fit_label(
            profession, 92, locale=context.locale, size=16, minimum=14
        )
        labels[item.identity.skport_id] = title, title_size, caption, caption_size
        if title_shortened or caption_shortened:
            detail_records.append(
                Record("Character identity", [name, f"Character ID: {item.identity.skport_id}", profession])
            )
    total_pages = len(groups) + (record_page_count(context, detail_records) if detail_records else 0)
    for page, group in enumerate(groups, 1):
        canvas = PageCanvas("ROSTER", context, dark=variant == "dark", size=(1600, 1100), assets=assets)
        scope = "Owned roster" if context.source_scope == "owner" else "Public showcase"
        complete = getattr(model, "roster_complete", None)
        canvas.text(
            56,
            134,
            f"{scope} · {len(characters)} supplied" + (" · Complete" if complete is True else ""),
            size=23,
            fill=canvas.muted,
        )
        if not group:
            canvas.panel((56, 205, 1544, 840))
            canvas.text(96, 265, "No characters supplied", size=42, bold=True)
            canvas.text(96, 335, "This snapshot does not disclose any character entries.", size=26)
        for index, item in enumerate(group):
            row, col = divmod(index, 4)
            x, y = 56 + col * 378, 190 + row * 272
            canvas.panel((x, y, x + 354, y + 250))
            portrait = image_url(item.images.portrait) or image_url(item.images.avatar)
            photo(canvas, portrait, (x + 2, y + 2, x + 152, y + 248), assets)
            canvas.draw.rectangle((x, y + 242, x + 354, y + 250), fill=canvas.accent)
            tx = x + 168
            title, title_size, caption, caption_size = labels[item.identity.skport_id]
            canvas.text(tx, y + 20, title, size=title_size, bold=True)
            canvas.text(tx, y + 102, f"Lv {item.level}/{item.max_level}", size=28, bold=True)
            canvas.text(
                tx, y + 142, f"E{item.evolution} · P{item.potential} · {item.rarity}", size=20, width=149
            )
            canvas.icon("rarity.star", tx + 145, y + 146, size=17)
            if item.profession.key:
                canvas.icon(
                    f"profession.{item.profession.key.removeprefix('profession_').upper()}",
                    tx,
                    y + 191,
                    size=26,
                )
            if item.element.key:
                canvas.icon(
                    f"element.{item.element.key.removeprefix('char_property_').lower()}",
                    tx + 38,
                    y + 191,
                    size=26,
                )
            canvas.text(tx + 77, y + 191, caption, size=caption_size)
        yield canvas.finish(page=page, pages=total_pages)
    if detail_records:
        yield from iter_records(
            "ROSTER DETAILS",
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
    """Collect the explicitly requested roster batch."""
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
