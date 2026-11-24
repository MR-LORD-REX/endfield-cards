"""AKEF poster profile with a yellow identity rail and clipped portrait cards."""

from typing import Any

from PIL import Image, ImageDraw

from ._shared import draw_avatar, draw_caption, draw_empty, draw_tile, facts, medal_board, new_canvas

INK = "#171A20"
SOFT_INK = "#514922"


def _facts(canvas: Any, values: list[tuple[str, str]]) -> None:
    if len(values) > 12:
        rows = (len(values) + 1) // 2
        step = min(64, 456 // rows)
        for index, (label, value) in enumerate(values):
            row, column = divmod(index, 2)
            x, y = 42 + column * 163, 467 + row * step
            canvas.text(x, y, canvas.t(label).upper(), size=14, fill=SOFT_INK, width=151, max_lines=1)
            canvas.text(
                x, y + 23, value, size=min(28, step - 31), bold=True, fill=INK, width=151, max_lines=1
            )
        return
    step = min(48, 456 // max(1, len(values)))
    for index, (label, value) in enumerate(values):
        y = 467 + index * step
        canvas.text(
            42, y + 6, canvas.t(label).upper(), size=min(17, step - 14), fill=SOFT_INK, width=222, max_lines=1
        )
        canvas.text(280, y, value, size=min(28, step - 8), bold=True, fill=INK, width=88, max_lines=1)


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
    """Keep the poster reference's avatar, identity, facts, medals and clipped tiles."""
    group = model.characters[:8] if characters is None else characters
    canvas = new_canvas(context, "identity", assets)
    canvas.background = "#EEECE4"
    canvas.image.paste(canvas.background, (0, 0, canvas.width, canvas.height))
    rail = Image.new("RGBA", (410, 1134), canvas.accent)
    draw = ImageDraw.Draw(rail)
    for position in range(-1134, 410, 64):
        draw.line((position, 1134, position + 1134, 0), fill="#F6C20D", width=17)
    canvas.image.alpha_composite(rail)
    canvas.text(42, 15, "ENDFIELD", size=13, bold=True, fill=SOFT_INK)
    draw_avatar(canvas, model, (42, 48, 200, 206), shape="rectangle", ring=INK)
    canvas.text(42, 238, context.owner.name, size=60, bold=True, fill=INK, width=326, max_lines=1)
    canvas.text(
        42, 316, f"UID {context.owner.game_uid}", size=22, bold=True, fill=INK, width=326, max_lines=1
    )
    if model.server_name:
        canvas.text(42, 352, model.server_name.upper(), size=18, fill=SOFT_INK, width=326, max_lines=1)
    line = model.biography or model.mission
    if line:
        canvas.text(42, 385, line, size=21, fill=INK, width=326, max_lines=2)
    canvas.draw.rectangle((42, 447, 368, 451), fill=INK)
    _facts(canvas, facts(model))
    if model.medals:
        canvas.text(
            42, 939, canvas.t("Medals").upper(), size=16, bold=True, fill=SOFT_INK, width=326, max_lines=1
        )
        medal_board(canvas, model, 42, 970, 326)
    canvas.text(452, 43, canvas.t("Profile").upper(), size=47, bold=True, fill=INK, width=1176, max_lines=1)
    canvas.draw.rectangle((1788, 49, 1878, 55), fill=INK)
    canvas.draw.rectangle((1788, 68, 1834, 74), fill=canvas.accent)
    draw_caption(canvas, model, group, page, pages, 452, 104, 1424)
    if not group:
        draw_empty(canvas, (452, 146, 1876, 1058))
    for index, character in enumerate(group):
        row, column = divmod(index, 4)
        x, y = 452 + column * 361, 146 + row * 466
        draw_tile(canvas, character, (x, y, x + 341, y + 446), style="identity")
    return canvas.finish(page, pages)
