"""Rectified legacy panorama with a quiet scene backdrop and isolated data panels."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.utils.blending import draw_character_art, paint_background
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import gradient_alpha

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
    c = PageCanvas("Character", context, dark=True, size=(1920, 1000), assets=assets, header=False)
    paint_background(c, model, assets, artwork, style="field")
    draw_character_art(c, model, (496, 100, 1370, 934), assets, artwork)
    identity_veil = Image.new("RGBA", (736, 224), "#161D26")
    identity_veil.putalpha(gradient_alpha(identity_veil.size, start=0.70, maximum=222, reverse=True))
    c.image.alpha_composite(identity_veil, (562, 14))
    # Retain the legacy left-stat / central-art / right-equipment composition.
    c.panel((28, 35, 547, 629))
    c.panel((28, 646, 547, 775))
    c.panel((1323, 34, 1893, 362))
    c.panel((1323, 379, 1893, 923))
    draw_stats(c, model, (49, 57, 526, 610), layout="rows")
    draw_talents(c, model, (48, 662, 525, 755))
    draw_identity(c, model, 583, 29, 704)
    draw_skills(c, model, (39, 801, 1262, 924))
    draw_weapon(c, model, (1343, 50, 1875, 346))
    draw_equipment(c, model, (1343, 395, 1875, 906), columns=2)
    c.draw.line((30, 23, 151, 23), fill=c.accent, width=4)
    return c.finish(page, pages)


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    from . import _shared

    return _shared.iter_render(model, context, variant="field", **options)


def urls(model: Any) -> set[str]:
    from . import _shared

    return _shared.urls(model)
