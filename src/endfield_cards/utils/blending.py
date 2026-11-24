"""Deterministic artwork framing and soft background blending without caller mutation."""

from typing import Any, cast

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

from endfield_cards.models import Artwork
from endfield_cards.utils.drawing import ELEMENT_COLORS, PageCanvas, element_key
from endfield_cards.utils.images import fitted


def hero_url(model: Any) -> str | None:
    """Prefer the full-resolution scene over small profile/half-body portraits."""
    for name in ("splash", "half_body", "portrait", "avatar"):
        links = getattr(model.images, name, None)
        if links is not None and links.url:
            return links.url
    return None


def artwork_source(model: Any, assets: Any) -> Image.Image | None:
    if assets is None:
        return None
    custom = assets.get("custom_art")
    if custom is not None:
        return custom
    url = hero_url(model)
    return assets.get(url) if url else None


def dominant_colour(
    source: Image.Image | None, fallback: tuple[int, int, int] = (64, 86, 103)
) -> tuple[int, int, int]:
    if source is None:
        return fallback
    buckets: dict[tuple[int, int, int], tuple[int, int, int, int]] = {}
    preview = source.convert("RGBA").resize((32, 32), Image.Resampling.BOX)
    for position in range(1024):
        r, g, b, a = cast(tuple[int, int, int, int], preview.getpixel((position % 32, position // 32)))
        if a < 96 or max(r, g, b) - min(r, g, b) < 25 or not 30 < (r + g + b) / 3 < 210:
            continue
        key = r // 40, g // 40, b // 40
        count, red, green, blue = buckets.get(key, (0, 0, 0, 0))
        buckets[key] = count + 1, red + r, green + g, blue + b
    if not buckets:
        return fallback
    count, red, green, blue = max(buckets.values(), key=lambda value: value[0])
    return red // count, green // count, blue // count


def paint_background(
    canvas: PageCanvas, model: Any, assets: Any, artwork: Artwork | None = None, *, style: str = "field"
) -> None:
    """Retain the scene's colour in a quiet backdrop beneath the data panels."""
    source = artwork_source(model, assets)
    colour = dominant_colour(source)
    w, h = canvas.width, canvas.height
    dark = canvas.dark
    canvas.image.paste("#171D25" if dark else "#F2F1EC", (0, 0, w, h))
    if style == "field" and source is not None:
        echo = fitted(source, (w, h), focus=artwork.focal_point if artwork else (0.5, 0.45))
        echo = echo.filter(ImageFilter.GaussianBlur(28))
        echo.putalpha(echo.getchannel("A").point(lambda alpha: alpha * 42 // 255))
        canvas.image.alpha_composite(echo)
    glow = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(glow)
    draw.ellipse((int(w * 0.20), -120, int(w * 0.74), int(h * 1.20)), fill=(*colour, 48 if dark else 27))
    canvas.image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(85)))
    grid = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(grid)
    if style == "field":
        for x in range(18, w, 30):
            for y in range(20, h - 70, 30):
                draw.point((x, y), fill=(205, 216, 224, 13))
    for x in range(int(w * 0.62), w + h, 110):
        draw.line((x - h, h, x, 0), fill=(140, 158, 174, 9 if dark else 12), width=1)
    canvas.image.alpha_composite(grid)


def _edge_mask(size: tuple[int, int], *, edge: int, bottom: int) -> Image.Image:
    w, h = size
    mask = Image.new("L", size, 255)
    draw = ImageDraw.Draw(mask)
    for position in range(edge):
        value = int(255 * (position / max(1, edge)) ** 0.8)
        draw.line((position, 0, position, h), fill=value)
        draw.line((w - 1 - position, 0, w - 1 - position, h), fill=value)
    for position in range(bottom):
        value = int(255 * position / max(1, bottom))
        draw.line((0, h - 1 - position, w, h - 1 - position), fill=value)
    top_mask = Image.new("L", size, 255)
    top_draw = ImageDraw.Draw(top_mask)
    for position in range(min(38, h // 8)):
        top_draw.line((0, position, w, position), fill=int(255 * position / max(1, min(38, h // 8))))
    mask = ImageChops.multiply(mask, top_mask)
    return mask


def draw_character_art(
    canvas: PageCanvas,
    model: Any,
    box: tuple[int, int, int, int],
    assets: Any,
    artwork: Artwork | None = None,
    *,
    portrait: bool = False,
) -> None:
    x, y, right, bottom = box
    width, height = right - x, bottom - y
    original = artwork_source(model, assets)
    if original is None:
        canvas.text(
            x + 35,
            y + height // 2,
            canvas.t("Unavailable"),
            size=25,
            fill=canvas.muted,
            width=width - 70,
            max_lines=1,
        )
        return
    source = ImageOps.exif_transpose(original).convert("RGBA")
    if artwork is not None:
        layer = fitted(source, (width, height), focus=artwork.focal_point, contain=artwork.fit == "contain")
    elif portrait:
        focus = model.images.focal_point or (0.5, 0.32)
        layer = fitted(source, (width, height), focus=focus)
    else:
        # Enka supplies cropped scenes with varying dimensions, rather than one fixed square.
        focus = model.images.focal_point or (0.5, 0.32)
        top, end = int(source.height * 0.06), source.height
        crop_height = end - top
        crop_width = min(source.width, int(crop_height * width / height))
        centre = focus[0] * source.width
        left = max(0, min(source.width - crop_width, int(centre - crop_width / 2)))
        framed = source.crop((left, top, left + crop_width, end))
        layer = fitted(framed, (width, height), focus=(0.5, 0.40))
    mask = _edge_mask(layer.size, edge=min(115, width // 5), bottom=min(95, height // 6))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mask))
    shadow = Image.new("RGBA", layer.size, "#0C121B")
    shadow.putalpha(layer.getchannel("A").point(lambda alpha: alpha // (4 if canvas.dark else 6)))
    canvas.image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)), (x + 10, y + 10))
    canvas.image.alpha_composite(layer, (x, y))


def element_colour(model: Any) -> str:
    return ELEMENT_COLORS.get(element_key(model), "#83919E")
