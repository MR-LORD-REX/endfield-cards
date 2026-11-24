"""Contingency Contract light variant entry points."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from . import _shared


def draw(model: Any, context: Any, *, item: Any, assets: Any = None, profile: Any = None) -> Any:
    """Light operation banner, score/medal tile, radial missions and enemy ledger."""
    c = _shared.new_canvas(context, dark=False, assets=assets)
    _shared.owner_header(c, profile)
    c.draw.line((40, 145, 1560, 145), fill=c.line)
    if item is None:
        c.panel((40, 180, 1560, 902))
        _shared.text(c, 75, 237, "No Contingency Contract supplied", 1450, size=38, bold=True)
        return c
    _shared.hero(c, item, (40, 170, 1060, 440))
    _shared.title(c, item, (65, 205, 1032, 430))
    _shared.score(c, item, (1080, 170, 1560, 440))
    _shared.missions(c, item, (40, 460, 1560, 660), radial=True)
    _shared.encounter(c, item, (40, 680, 1060, 922))
    _shared.schedule(c, model, item, (1080, 680, 1560, 922))
    _shared.history(c, model, item, (65, 409, 1033, 433))
    return c


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    """Draw this named variant through the shared family implementation."""
    return _shared.iter_render(model, context, variant="light", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    """Collect this named variant's explicitly requested images."""
    return list(iter_render(model, context, **options))


urls = _shared.urls
