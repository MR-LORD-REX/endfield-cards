"""AKEF midnight profile with a compact identity band and shaded operator tiles."""

from typing import Any

from PIL import Image

from ._shared import (
    draw_avatar,
    draw_caption,
    draw_empty,
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
    """Preserve the midnight reference's identity, medals, facts and eight portraits."""
    group = model.characters[:8] if characters is None else characters
    canvas = new_canvas(context, "operations", assets)
    paint_banner(canvas, model, (0, 0, 1600, 324), dark=True, rounded=False)
    draw_avatar(canvas, model, (44, 44, 168, 168), shape="rounded", ring="yellow")
    canvas.text(
        202,
        25,
        "ENDFIELD / " + canvas.t("Profile").upper(),
        size=17,
        bold=True,
        fill=canvas.accent,
        width=796,
        max_lines=1,
    )
    canvas.text(200, 52, context.owner.name, size=68, bold=True, width=798, max_lines=1)
    values = facts(model)
    metadata = [f"UID {context.owner.game_uid}"]
    if model.server_name:
        metadata.append(model.server_name)
    age = next((value for label, value in values if label == "Days"), None)
    if age is not None:
        metadata.append(canvas.t("Days") + " " + age)
    canvas.text(202, 136, "  /  ".join(metadata), size=22, fill=canvas.muted, width=796, max_lines=1)
    line = model.biography or model.mission
    if line:
        canvas.text(44, 192, line, size=24, width=982, max_lines=1)
    if model.medals:
        canvas.text(1090, 25, canvas.t("Medals"), size=15, fill=canvas.muted, bold=True)
        medal_board(canvas, model, 1080, 49, 476)
    cell = 1512 // max(1, len(values))
    for index, (label, value) in enumerate(values):
        x = 44 + index * cell
        canvas.text(x, 247, canvas.t(label).upper(), size=16, fill=canvas.muted, width=cell - 22, max_lines=1)
        canvas.text(
            x,
            274,
            value,
            size=34,
            bold=True,
            fill=canvas.accent if label == "Authority" else canvas.fg,
            width=cell - 22,
            max_lines=1,
        )
        if index:
            canvas.draw.line((x - 15, 249, x - 15, 312), fill=canvas.line, width=1)
    canvas.draw.line((44, 324, 1556, 324), fill=canvas.line, width=1)
    draw_caption(canvas, model, group, page, pages, 44, 348, 1512)
    if not group:
        draw_empty(canvas, (44, 386, 1556, 1306))
    for index, character in enumerate(group):
        row, column = divmod(index, 4)
        x, y = 44 + column * 384, 386 + row * 472
        draw_tile(canvas, character, (x, y, x + 360, y + 448), style="operations")
    return canvas.finish(page, pages)
