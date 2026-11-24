"""Activity light variant entry points."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.utils.drawing import PageCanvas

from . import _shared


def draw(model: Any, context: Any, *, assets: Any = None, profile: Any = None) -> PageCanvas:
    """Light dashboard with a Sanity rail and a compact resource/event grid."""
    c = PageCanvas("Live status", context, assets=assets, size=_shared.SIZE, header=False)
    _shared.draw_header(c, model, profile)
    _shared.draw_sanity(c, model, (40, 184, 436, 922))
    for index, (key, label, icon) in enumerate(_shared.METER_INFO):
        row, column = divmod(index, 2)
        x, y = 460 + column * 560, 184 + row * 168
        _shared.draw_meter(c, model, key, label, icon, (x, y, x + 540, y + 152))
    _shared.draw_echoes(c, model, (460, 536, 1000, 922))
    _shared.draw_contract(c, model, (1020, 536, 1560, 922))
    return c


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    """Draw this named variant through the shared family implementation."""
    return _shared.iter_render(model, context, variant="light", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    """Collect this named variant's explicitly requested images."""
    return list(iter_render(model, context, **options))


urls = _shared.urls
