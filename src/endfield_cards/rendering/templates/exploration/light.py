"""Exploration light composition: per-area category tiles."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from . import _shared

urls = _shared.urls


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    return _shared.iter_render(model, context, variant="light", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
