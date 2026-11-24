"""AKEF in-game character sheet with shaded artwork and clipped technical panels."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.models import Artwork
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import gradient_alpha

from .components import (
    draw_equipment,
    draw_identity,
    draw_skills,
    draw_stats,
    draw_talents,
    draw_weapon,
)

SIZE = (1920, 1240)


class _TerminalCanvas(PageCanvas):
    """The in-game reference's cut corners and restrained signal tabs."""

    def panel(self, box: tuple[int, int, int, int]) -> None:
        x, y, right, bottom = box
        cut = 14
        self.draw.polygon(
            [
                (x, y),
                (right - cut, y),
                (right, y + cut),
                (right, bottom),
                (x + cut, bottom),
                (x, bottom - cut),
            ],
            fill=self.panel_color,
            outline=self.line,
            width=1,
        )
        self.draw.line((x + 1, y + 1, x + 40, y + 1), fill=self.accent, width=3)


def render(
    model: Any,
    context: Any,
    *,
    assets: dict | None = None,
    artwork: Artwork | None = None,
    **options: Any,
) -> Image.Image:
    """Keep the reference's left statistics, central hero and right equipment stacks."""
    from endfield_cards.utils.blending import draw_character_art, paint_background

    canvas = _TerminalCanvas("Character", context, dark=True, size=SIZE, assets=assets, header=False)
    canvas.background = "#13161C"
    canvas.panel_color = "#20252E"
    canvas.line = "#444C58"
    canvas.muted = "#ADB6C5"
    paint_background(canvas, model, assets, artwork, style="terminal")
    shade = Image.new("RGBA", SIZE, "#0D1015")
    shade.putalpha(gradient_alpha(SIZE, start=0.35, maximum=95))
    canvas.image.alpha_composite(shade)
    draw_character_art(canvas, model, (505, 68, 1258, 1174), assets, artwork)

    canvas.draw.polygon([(44, 38), (206, 38), (192, 67), (44, 67)], fill=canvas.accent)
    canvas.text(56, 43, canvas.t("Character").upper(), size=17, bold=True, fill="#171B22")
    draw_identity(canvas, model, 44, 80, 438)
    draw_stats(canvas, model, (44, 275, 482, 835))
    draw_talents(canvas, model, (44, 860, 482, 1068))

    draw_skills(canvas, model, (1280, 48, 1876, 238), columns=2)
    draw_weapon(canvas, model, (1280, 262, 1876, 595))
    draw_equipment(canvas, model, (1280, 622, 1876, 1102), columns=2)

    for x, y, sx, sy in ((20, 20, 1, 1), (1900, 20, -1, 1), (20, 1154, 1, -1), (1900, 1154, -1, -1)):
        canvas.draw.line((x, y, x + 34 * sx, y), fill=canvas.accent, width=2)
        canvas.draw.line((x, y, x, y + 34 * sy), fill=canvas.accent, width=2)
    return canvas.finish()


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    """Yield one concise terminal image; optional detail export belongs to the family."""
    yield render(model, context, **options)
