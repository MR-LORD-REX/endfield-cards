"""Same-character comparison with explicit owners and full source detail pages."""

from collections.abc import Iterator
from dataclasses import replace
from typing import Any

from PIL import Image, ImageDraw

from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.components import PageCanvas, art_url, place_art
from endfield_cards.rendering.templates import character


def validate_pair(first: Any, second: Any) -> None:
    left, right = first.identity, second.identity
    if not left.str_id or not right.str_id or left.str_id != right.str_id:
        raise DataValidationError(
            "comparison requires the same canonical character", code="character_mismatch"
        )
    if (
        left.template_id is not None
        and right.template_id is not None
        and left.template_id != right.template_id
    ):
        raise DataValidationError("comparison canonical template IDs disagree", code="character_mismatch")


def iter_render(
    first: Any,
    second: Any,
    context: Any,
    second_context: Any,
    *,
    variant: str = "field",
    assets: dict | None = None,
    artwork: Any = None,
    second_artwork: Any = None,
    details: bool = False,
) -> Iterator[Image.Image]:
    validate_pair(first, second)
    combined = replace(context, comparison_owner=second_context.owner)
    c = PageCanvas(
        "Comparison", combined, dark=variant in {"field", "terminal"}, size=(1600, 1100), assets=assets
    )
    c.text(50, 143, first.name, size=40, bold=True, width=1500)
    for index, model in enumerate((first, second)):
        x = 40 + index * 770
        source = (assets or {}).get("custom_art" if index == 0 else "second_custom_art") or (
            assets or {}
        ).get(art_url(model))
        place_art(c, source, (x, 217, x + 750, 610), artwork if index == 0 else second_artwork, blend=True)
        owner = context.owner if index == 0 else second_context.owner
        c.text(x + 22, 630, owner.name, size=31, bold=True, width=695)
        c.text(
            x + 22,
            675,
            f"UID {owner.game_uid}  ·  Lv {model.level}/{model.max_level}  ·  P{model.potential}",
            size=22,
        )
        y = 734
        for stat_id in (1, 2, 3, 9, 10):
            if model.stats is None or stat_id not in model.stats.values:
                continue
            stat = model.stats.values[stat_id]
            y += c.row(stat.name or f"Property {stat_id}", stat.display, x + 22, y, width=695)
        if model.weapon is not None and y + 30 < c.height - 66:
            c.text(
                x + 22,
                y,
                f"{model.weapon.name} · Lv {model.weapon.level} · R{model.weapon.refinement}",
                size=18,
                fill=c.muted,
                width=695,
                max_lines=1,
            )
    if not details:
        yield c.finish()
        return
    total = (
        1
        + character.page_count(first, context, variant=variant, details=True)
        + character.page_count(second, second_context, variant=variant, details=True)
    )
    yield c.finish(1, total)
    page_number = 1
    for index, (model, owner_context, custom) in enumerate(
        ((first, context, artwork), (second, second_context, second_artwork))
    ):
        copy_assets = assets.fork() if assets is not None and hasattr(assets, "fork") else dict(assets or {})
        if index == 1:
            copy_assets.pop("custom_art", None)
            if "second_custom_art" in copy_assets:
                copy_assets["custom_art"] = copy_assets["second_custom_art"]
        own_combined = replace(
            owner_context, comparison_owner=context.owner if index else second_context.owner
        )
        for image in character.iter_render(
            model, own_combined, variant=variant, assets=copy_assets, artwork=custom, details=True
        ):
            page_number += 1
            footer = PageCanvas("Comparison", combined, size=image.size)
            footer.image, footer.draw = image, ImageDraw.Draw(image)
            yield footer.finish(page_number, total)


def render(first: Any, second: Any, context: Any, second_context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(first, second, context, second_context, **options))
