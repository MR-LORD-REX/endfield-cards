"""Light profile: circular identity, fact chips and a prominent medal board."""

from typing import Any

from PIL import Image

from ._shared import (
    draw_avatar,
    draw_caption,
    draw_empty,
    draw_identity,
    draw_tile,
    facts,
    medal_board,
    new_canvas,
    paint_banner,
)


def render(
    model: Any,
    context: Any,
    *,
    assets: dict | None = None,
    characters: list[Any] | None = None,
    page: int = 1,
    pages: int = 1,
    **options: Any,
) -> Image.Image:
    group = model.characters[:8] if characters is None else characters
    c = new_canvas(context, "overview", assets)
    paint_banner(c, model, (44, 42, 1556, 382))
    draw_avatar(c, model, (76, 80, 212, 216), shape="circle")
    draw_identity(c, model, 246, 70, 690 if model.medals else 1210, name_size=68)
    c.text(77, 250, "ENDFIELD / " + c.t("Profile"), size=16, fill=c.muted, bold=True)
    x, y, end = 76, 281, 974 if model.medals else 1518
    for label, value in facts(model):
        translated = c.t(label)
        font = c.fonts.get(17, weight="semibold", locale=context.locale, text=translated)
        width = int(font.getlength(translated)) + len(value) * 13 + 51
        if x + width > end:
            x, y = 76, y + 51
        c.draw.rounded_rectangle((x, y, x + width, y + 41), radius=20, fill="#252A33")
        c.text(x + 15, y + 9, translated, size=17, fill="#B6BCC5", width=width - 44, max_lines=1)
        offset = int(font.getlength(translated)) + 28
        c.text(
            x + offset,
            y + 6,
            value,
            size=22,
            bold=True,
            fill=c.accent if label == "Authority" else "#F4F3EE",
            width=width - offset - 12,
            max_lines=1,
        )
        x += width + 10
    if model.medals:
        c.text(1047, 77, c.t("Medals"), size=17, fill=c.muted, bold=True)
        medal_board(c, model, 1025, 116, 508)
    draw_caption(c, model, group, page, pages, 44, 410, 1512)
    if not group:
        draw_empty(c, (44, 454, 1556, 1308))
    for index, character in enumerate(group):
        row, col = divmod(index, 4)
        x, y = 44 + col * 384, 454 + row * 438
        draw_tile(c, character, (x, y, x + 360, y + 414), style="overview")
    return c.finish(page, pages)
