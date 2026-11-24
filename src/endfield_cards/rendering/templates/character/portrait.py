"""Single vertical showcase sharing the AKEF information hierarchy."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.utils.blending import draw_character_art, paint_background
from endfield_cards.utils.drawing import PageCanvas

from .components import draw_equipment, draw_identity, draw_skills, draw_stats, draw_talents, draw_weapon


def render(
    model: Any,
    context: Any,
    *,
    assets: Any = None,
    artwork: Any = None,
    page: int = 1,
    pages: int = 1,
    **options: Any,
) -> Image.Image:
    c = PageCanvas("Character", context, size=(1100, 1950), assets=assets, header=False)
    paint_background(c, model, assets, artwork, style="portrait")
    draw_identity(c, model, 41, 28, 1020)
    draw_character_art(c, model, (22, 192, 1078, 591), assets, artwork, portrait=True)
    draw_stats(c, model, (43, 595, 1057, 957), layout="columns")
    draw_skills(c, model, (43, 972, 1057, 1088))
    draw_weapon(c, model, (43, 1103, 1057, 1360))
    draw_equipment(c, model, (43, 1378, 1057, 1718), columns=4)
    draw_talents(c, model, (43, 1732, 1057, 1830))
    return c.finish(page, pages)


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    from . import _shared

    return _shared.iter_render(model, context, variant="portrait", **options)


def urls(model: Any) -> set[str]:
    from . import _shared

    return _shared.urls(model)
