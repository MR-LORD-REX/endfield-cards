"""Profile family dispatcher; each named variant owns its layout."""

from collections.abc import Iterator
from importlib import import_module
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.errors import UnsupportedVariantError
from endfield_cards.utils.records import iter_records, record_page_count

from ._shared import SIZE_BY_VARIANT, detail_records, medal_url

VARIANTS = tuple(SIZE_BY_VARIANT)


def urls(model: Any) -> set[str]:
    links = [image_url(model.avatar), image_url(model.banner)]
    for character in model.characters:
        links.extend(
            (
                image_url(character.images.portrait)
                or image_url(character.images.half_body)
                or image_url(character.images.avatar),
                image_url(character.element.icons),
                image_url(character.profession.icons),
            )
        )
    links.extend(medal_url(medal) for medal in model.medals)
    return {url for url in links if url}


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "overview",
    assets: dict | None = None,
    details: bool = False,
    **options: Any,
) -> Iterator[Image.Image]:
    if variant not in VARIANTS:
        raise UnsupportedVariantError(f"unknown profile variant {variant!r}")
    validate_owner(model, context)
    groups = [model.characters[i : i + 8] for i in range(0, len(model.characters), 8)] or [[]]
    records = detail_records(model) if details else []
    total = len(groups) + (record_page_count(context, records, size=(1600, 1100)) if details else 0)
    renderer = import_module(f"{__name__}.{variant}")
    for index, group in enumerate(groups):
        yield renderer.render(
            model, context, assets=assets, characters=group, page=index + 1, pages=total, **options
        )
    if details:
        yield from iter_records(
            "Profile information",
            context,
            records,
            assets=assets,
            variant="dark" if variant == "operations" else "light",
            size=(1600, 1100),
            page_offset=len(groups),
            total_pages=total,
        )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
