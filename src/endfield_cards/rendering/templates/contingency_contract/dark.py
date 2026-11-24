"""Contingency Contract dark variant entry points."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from . import _shared


def draw(model: Any, context: Any, *, item: Any, assets: Any = None, profile: Any = None) -> Any:
    """Dark full-width scene above score, linear missions and broad enemy strip."""
    c = _shared.new_canvas(context, dark=True, assets=assets)
    if item is not None:
        _shared.hero(c, item, (0, 0, 1600, 404), full=True)
    _shared.owner_header(c, profile)
    if item is None:
        c.panel((40, 180, 1560, 902))
        _shared.text(c, 75, 237, "No Contingency Contract supplied", 1450, size=38, bold=True)
        return c
    _shared.title(c, item, (42, 179, 1515, 329))
    deadlines = "Gameplay ends " + _shared.display_time(item.ends_at, c.context)
    deadlines += " · Collection ends " + _shared.display_time(item.ends_at_collection, c.context)
    _shared.text(c, 42, 345, deadlines, 1517, size=16, fill=c.muted)
    _shared.score(c, item, (40, 419, 484, 697))
    _shared.missions(c, item, (508, 419, 1560, 697), radial=False)
    _shared.encounter(c, item, (40, 718, 1560, 922))
    _shared.history(c, model, item, (42, 379, 1517, 403))
    return c


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    """Draw this named variant through the shared family implementation."""
    return _shared.iter_render(model, context, variant="dark", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    """Collect this named variant's explicitly requested images."""
    return list(iter_render(model, context, **options))


urls = _shared.urls
