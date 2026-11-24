"""Monument light variant entry points."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.utils.drawing import PageCanvas

from . import _shared


def render_page(
    model: Any,
    context: Any,
    *,
    entries: list[Any],
    all_events: list[Any],
    offset: int = 0,
    assets: Any = None,
    profile: Any = None,
    page: int = 1,
    pages: int = 1,
) -> Image.Image:
    """Light poster gallery with aligned Normal/Hard stage ledgers."""
    c = PageCanvas(
        "Monument", context, size=_shared.page_size(len(entries), "light"), assets=assets, header=False
    )
    _shared.draw_header(c, model, all_events, profile)
    width = (c.width - 2 * _shared.PAD - 3 * _shared.GAP) // 4
    for index, event in enumerate(entries):
        row, col = divmod(index, 4)
        x, y = (
            _shared.PAD + col * (width + _shared.GAP),
            _shared.TOP + row * (_shared.LIGHT_HEIGHT + _shared.GAP),
        )
        c.panel((x, y, x + width, y + _shared.LIGHT_HEIGHT))
        _shared.draw_art(c, event, (x + 1, y + 1, x + width - 1, y + 282))
        _shared.draw_state(c, event, offset + index + 1, x + 12, y + 13)
        _shared.draw_medal(c, event, (x + width - 76, y + 204, x + width - 12, y + 272))
        _shared.text(
            c,
            x + 17,
            y + 299,
            event.name or event.id or "Unavailable",
            width - 34,
            size=24,
            bold=True,
            max_lines=2,
        )
        _shared.draw_counts(c, event, x + 17, y + 364, width - 34)
        _shared.draw_stage_table(c, event, x + 17, y + 418, width - 34)
        _shared.draw_fastest(c, event, x + 17, y + 558, width - 34)
    if not entries:
        c.panel((36, 216, 1564, c.height - 95))
        _shared.text(c, 66, 267, "No monument events supplied", 1450, size=34, bold=True)
    return c.finish(page, pages)


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    """Draw this named variant through the shared family implementation."""
    return _shared.iter_render(model, context, variant="light", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    """Collect this named variant's explicitly requested images."""
    return list(iter_render(model, context, **options))


urls = _shared.urls
