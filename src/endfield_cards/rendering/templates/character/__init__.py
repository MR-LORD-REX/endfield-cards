"""Character family with explicit named variant modules."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.errors import UnsupportedVariantError

from . import _shared

urls = _shared.urls
records = _shared.records
page_count = _shared.page_count
iter_records = _shared.iter_records
record_page_count = _shared.record_page_count
VARIANTS = ("field", "dossier", "terminal", "portrait")


def iter_render(model: Any, context: Any, *, variant: str = "field", **options: Any) -> Iterator[Image.Image]:
    """Select a named family variant without changing its rendering contract."""
    if variant not in VARIANTS:
        raise UnsupportedVariantError(f"unknown character variant {variant!r}; choose {VARIANTS}")
    return _shared.iter_render(model, context, variant=variant, **options)


def render(model: Any, context: Any, *, variant: str = "field", **options: Any) -> list[Image.Image]:
    """Collect separately encoded-compatible pages for this family."""
    return list(iter_render(model, context, variant=variant, **options))


__all__ = ["render", "iter_render", "urls", "records", "page_count", "iter_records", "record_page_count"]
