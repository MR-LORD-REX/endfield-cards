"""Same-character comparison with explicit owners and full source detail pages."""

from collections.abc import Iterator
from dataclasses import replace
from typing import Any

from PIL import Image, ImageDraw

from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.templates import character, comparison
from endfield_cards.utils.drawing import PageCanvas


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
    c = comparison.render_canvas(
        first,
        second,
        context,
        second_context,
        variant=variant,
        assets=assets,
        artwork=artwork,
        second_artwork=second_artwork,
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
