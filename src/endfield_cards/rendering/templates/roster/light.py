"""Light full roster board with rounded portraits and quiet separated loadouts."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.utils.drawing import PageCanvas

from . import _shared as s


def render_page(
    model: Any,
    context: Any,
    *,
    assets: Any = None,
    characters: list[Any],
    all_characters: list[Any],
    selected: bool = False,
    page: int = 1,
    pages: int = 1,
) -> Image.Image:
    c = PageCanvas("All Characters", context, size=s.page_size(len(characters)), assets=assets, header=False)
    c.draw.ellipse((1740, -680, 2980, 590), outline="#E4E0D1", width=4)
    c.panel((s.PAD, 30, c.width - s.PAD, 207))
    s.draw_avatar(c, model, (66, 62, 170, 166))
    s.text(c, 206, 50, context.owner.name, 790, size=58, bold=True)
    s.text(c, 208, 120, s.owner_meta(model, context), 925, size=21, fill=c.muted)
    s.text(
        c,
        210,
        166,
        s.scope_caption(model, context, len(all_characters), selected=selected),
        990,
        size=18,
        fill=c.muted,
    )
    s.text(c, 1745, 46, "ENDFIELD / ALL CHARACTERS", 565, size=24, bold=True)
    for index, (label, value) in enumerate(s.roster_counts(all_characters)):
        x = 1410 + index * 286
        c.draw.rounded_rectangle((x, 97, x + 267, 182), radius=12, fill="#F0EEE6")
        s.text(c, x + 18, 108, label, 230, size=14, fill=c.muted, bold=True)
        s.text(c, x + 18, 128, value, 230, size=38, bold=True)
    for col in range(s.COLUMNS):
        x = s.PAD + col * (s.TILE_WIDTH + s.GAP)
        s.text(c, x + 12, 222, "OPERATOR / SKILLS", 345, size=14, fill=c.muted, bold=True)
        s.text(c, x + 426, 222, "WEAPON / GEAR", 319, size=14, fill=c.muted, bold=True)
    for index, item in enumerate(characters):
        row, col = divmod(index, s.COLUMNS)
        x, y = s.PAD + col * (s.TILE_WIDTH + s.GAP), s.TOP + row * s.ROW_STEP
        c.panel((x, y, x + s.TILE_WIDTH, y + s.ROW_HEIGHT))
        s.draw_portrait(c, item, (x + 12, y + 12, x + 120, y + s.ROW_HEIGHT - 12))
        s.draw_operator(c, item, x + 138, y + 10, 266)
        s.draw_skills(c, item, x + 138, y + 118, 270)
        c.draw.line((x + 417, y + 14, x + 417, y + s.ROW_HEIGHT - 14), fill=c.line)
        s.draw_loadout(c, item, x + 432, y + 12, s.TILE_WIDTH - 445)
    if not characters:
        c.panel((s.PAD, s.TOP, c.width - s.PAD, c.height - 99))
        s.text(c, 87, s.TOP + 56, "No characters supplied", c.width - 174, size=43, bold=True)
        s.text(
            c,
            87,
            s.TOP + 123,
            "This snapshot does not disclose any character entries.",
            c.width - 174,
            size=23,
            fill=c.muted,
        )
    return c.finish(page, pages)


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    return s.iter_render(model, context, variant="light", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))


urls = s.urls
