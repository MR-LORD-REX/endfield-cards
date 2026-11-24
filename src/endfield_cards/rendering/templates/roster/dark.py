"""Dark full roster with clipped portraits, column rails and inset loadout bands."""

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
    c = PageCanvas(
        "All Characters", context, dark=True, size=s.page_size(len(characters)), assets=assets, header=False
    )
    c.image.paste("#141A22", (0, 0, c.width, c.height))
    c.draw.rectangle((0, 0, 13, c.height - 66), fill=c.accent)
    for x in range(1560, c.width + 1000, 150):
        c.draw.line((x - 820, 0, x, 230), fill="#202B35", width=1)
    s.draw_avatar(c, model, (59, 59, 163, 163), clipped=True)
    s.text(c, 206, 40, "ENDFIELD / ALL CHARACTERS", 1130, size=21, bold=True, fill=c.accent)
    s.text(c, 206, 76, context.owner.name, 890, size=52, bold=True)
    s.text(c, 208, 145, s.owner_meta(model, context), 1130, size=20, fill=c.muted)
    s.text(
        c,
        42,
        211,
        s.scope_caption(model, context, len(all_characters), selected=selected),
        1150,
        size=18,
        fill=c.muted,
    )
    for index, (label, value) in enumerate(s.roster_counts(all_characters)):
        x = 1410 + index * 290
        c.draw.line((x, 57, x, 173), fill="#40505F", width=2)
        s.text(c, x + 25, 74, label, 240, size=14, fill=c.muted, bold=True)
        s.text(c, x + 23, 105, value, 240, size=49, bold=True)
    c.draw.line((s.PAD, 237, c.width - s.PAD, 237), fill=c.line, width=2)
    for col in range(1, s.COLUMNS):
        x = s.PAD + col * (s.TILE_WIDTH + s.GAP) - s.GAP // 2
        c.draw.line((x, s.TOP, x, c.height - 99), fill="#3B4652", width=1)
    for index, item in enumerate(characters):
        row, col = divmod(index, s.COLUMNS)
        x, y = s.PAD + col * (s.TILE_WIDTH + s.GAP), s.TOP + row * s.ROW_STEP
        c.draw.polygon(
            (
                (x, y),
                (x + s.TILE_WIDTH - 19, y),
                (x + s.TILE_WIDTH, y + 19),
                (x + s.TILE_WIDTH, y + s.ROW_HEIGHT),
                (x, y + s.ROW_HEIGHT),
            ),
            fill="#242B35",
        )
        c.draw.rectangle((x + 422, y + 7, x + s.TILE_WIDTH - 8, y + s.ROW_HEIGHT - 7), fill="#1B222B")
        s.draw_portrait(c, item, (x + 11, y + 12, x + 119, y + s.ROW_HEIGHT - 12), clipped=True)
        s.draw_operator(c, item, x + 138, y + 10, 266)
        s.draw_skills(c, item, x + 138, y + 118, 270)
        s.draw_loadout(c, item, x + 436, y + 12, s.TILE_WIDTH - 449)
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
    return s.iter_render(model, context, variant="dark", **options)


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))


urls = s.urls
