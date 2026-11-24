"""Activity dark variant entry points."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.utils.drawing import PageCanvas

from . import _shared


def draw(model: Any, context: Any, *, assets: Any = None, profile: Any = None) -> PageCanvas:
    """Dark dashboard with a horizontal resource deck and broad event panels."""
    c = PageCanvas("Live status", context, dark=True, assets=assets, size=_shared.SIZE, header=False)
    c.draw.polygon(((900, 0), (1600, 0), (1600, 154), (700, 154)), fill="#202933")
    _shared.draw_header(c, model, profile)
    _shared.draw_sanity(c, model, (40, 184, 540, 502), wide=True)
    for index, (key, label, icon) in enumerate(_shared.METER_INFO):
        x = 560 + index * 253
        _shared.draw_meter(c, model, key, label, icon, (x, 184, x + 241, 502), tall=True)
    _shared.draw_echoes(c, model, (40, 524, 790, 922))
    _shared.draw_contract(c, model, (810, 524, 1560, 922))
    return c


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    """Draw this named variant through the shared family implementation."""
    return _shared.iter_render(model, context, variant="dark", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    """Collect this named variant's explicitly requested images."""
    return list(iter_render(model, context, **options))


urls = _shared.urls
