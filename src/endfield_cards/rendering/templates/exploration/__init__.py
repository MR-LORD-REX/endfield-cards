"""Exploration family with two separately selectable compositions."""

from collections.abc import Iterator
from importlib import import_module
from typing import Any

from PIL import Image

from endfield_cards.errors import UnsupportedVariantError

from . import _shared

VARIANTS = ("light", "dark")
urls = _shared.urls


def iter_render(model: Any, context: Any, *, variant: str = "light", **options: Any) -> Iterator[Image.Image]:
    if variant not in VARIANTS:
        raise UnsupportedVariantError(f"unknown exploration variant {variant!r}; choose {VARIANTS}")
    module = import_module(f"{__name__}.{variant}")
    return module.iter_render(model, context, **options)


def render(model: Any, context: Any, *, variant: str = "light", **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, variant=variant, **options))
