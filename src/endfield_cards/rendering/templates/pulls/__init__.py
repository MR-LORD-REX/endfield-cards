"""Pulls family with explicit named variant modules."""

from collections.abc import Iterator
from importlib import import_module
from typing import Any

from PIL import Image

from endfield_cards.errors import UnsupportedVariantError

from . import _shared

urls = _shared.urls
VARIANTS = ("light", "dark")


def iter_render(model: Any, context: Any, *, variant: str = "light", **options: Any) -> Iterator[Image.Image]:
    """Select a named family variant without changing its rendering contract."""
    if variant not in VARIANTS:
        raise UnsupportedVariantError(f"unknown pulls variant {variant!r}; choose {VARIANTS}")
    module = import_module(f"{__name__}.{variant}")
    return module.iter_render(model, context, **options)


def render(model: Any, context: Any, *, variant: str = "light", **options: Any) -> list[Image.Image]:
    """Collect separately encoded-compatible pages for this family."""
    return list(iter_render(model, context, variant=variant, **options))


__all__ = ["render", "iter_render", "urls"]
