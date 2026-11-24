"""AKEF light showcase with a full scene and a compact, ordered build sheet."""

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
    c = PageCanvas("Character", context, size=(1600, 1400), assets=assets, header=False)
    paint_background(c, model, assets, artwork, style="dossier")
    draw_character_art(c, model, (0, 10, 741, 1334), assets, artwork)
    draw_identity(c, model, 746, 35, 812)
    draw_stats(c, model, (746, 210, 1556, 570), layout="columns")
    draw_skills(c, model, (746, 590, 1556, 704))
    draw_weapon(c, model, (746, 719, 1556, 972))
    draw_equipment(c, model, (746, 990, 1556, 1307), columns=4)
    draw_talents(c, model, (36, 1227, 704, 1323))
    return c.finish(page, pages)


def iter_render(model: Any, context: Any, **options: Any) -> Iterator[Image.Image]:
    from . import _shared

    return _shared.iter_render(model, context, variant="dossier", **options)


def urls(model: Any) -> set[str]:
    from . import _shared

    return _shared.urls(model)
