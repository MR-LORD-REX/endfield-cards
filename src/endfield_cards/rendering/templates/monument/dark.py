"""Monument dark variant entry points."""

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
    """Dark landscape records with retained poster art and readable stage rails."""
    c = PageCanvas(
        "Monument",
        context,
        dark=True,
        size=_shared.page_size(len(entries), "dark"),
        assets=assets,
        header=False,
    )
    c.draw.polygon(((900, 0), (1600, 0), (1600, 191), (732, 191)), fill="#202934")
    _shared.draw_header(c, model, all_events, profile)
    width = (c.width - 2 * _shared.PAD - _shared.GAP) // 2
    for index, event in enumerate(entries):
        row, col = divmod(index, 2)
        x, y = (
            _shared.PAD + col * (width + _shared.GAP),
            _shared.TOP + row * (_shared.DARK_HEIGHT + _shared.GAP),
        )
        c.panel((x, y, x + width, y + _shared.DARK_HEIGHT))
        _shared.draw_art(c, event, (x + 9, y + 9, x + 213, y + _shared.DARK_HEIGHT - 9), clipped=True)
        _shared.draw_state(c, event, offset + index + 1, x + 19, y + 20)
        _shared.draw_medal(c, event, (x + 135, y + 200, x + 201, y + 269))
        tx, room = x + 231, width - 248
        _shared.text(c, tx, y + 14, event.name or event.id or "Unavailable", room, size=25, bold=True)
        _shared.draw_counts(c, event, tx, y + 55, room)
        _shared.draw_stage_table(c, event, tx, y + 114, room, row_height=21)
        _shared.draw_fastest(c, event, tx, y + 251, room)
    if not entries:
        c.panel((36, 216, 1564, c.height - 95))
        _shared.text(c, 66, 267, "No monument events supplied", 1450, size=34, bold=True)
    return c.finish(page, pages)


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    """Draw this named variant through the shared family implementation."""
    return _shared.iter_render(model, context, variant="dark", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    """Collect this named variant's explicitly requested images."""
    return list(iter_render(model, context, **options))


urls = _shared.urls
