"""Copy-safe image fitting, antialiased masks and gradient compositing."""

from PIL import Image, ImageChops, ImageDraw, ImageOps


def fitted(
    source: Image.Image,
    size: tuple[int, int],
    *,
    focus: tuple[float, float] = (0.5, 0.2),
    contain: bool = False,
) -> Image.Image:
    pixels = ImageOps.exif_transpose(source).convert("RGBA")
    if contain:
        glyph = ImageOps.contain(pixels, size, Image.Resampling.LANCZOS)
        result = Image.new("RGBA", size)
        result.alpha_composite(glyph, ((size[0] - glyph.width) // 2, (size[1] - glyph.height) // 2))
        return result
    return ImageOps.fit(pixels, size, Image.Resampling.LANCZOS, centering=focus)


def shape_mask(
    size: tuple[int, int], *, shape: str = "rounded", radius: int = 16, cut: int = 28
) -> Image.Image:
    scale = 3
    w, h = size
    mask = Image.new("L", (w * scale, h * scale))
    draw = ImageDraw.Draw(mask)
    if shape == "circle":
        draw.ellipse((0, 0, w * scale - 1, h * scale - 1), fill=255)
    elif shape == "hexagon":
        draw.polygon(
            [
                (w * scale / 2, 0),
                (w * scale - 1, h * scale / 4),
                (w * scale - 1, h * scale * 3 / 4),
                (w * scale / 2, h * scale - 1),
                (0, h * scale * 3 / 4),
                (0, h * scale / 4),
            ],
            fill=255,
        )
    elif shape == "clipped":
        draw.polygon(
            [
                (0, 0),
                ((w - cut) * scale, 0),
                (w * scale - 1, cut * scale),
                (w * scale - 1, h * scale - 1),
                (0, h * scale - 1),
            ],
            fill=255,
        )
    elif shape == "top-rounded":
        draw.rounded_rectangle(
            (0, 0, w * scale - 1, (h + radius) * scale - 1), radius=radius * scale, fill=255
        )
    elif shape == "rectangle":
        draw.rectangle((0, 0, w * scale - 1, h * scale - 1), fill=255)
    else:
        draw.rounded_rectangle((0, 0, w * scale - 1, h * scale - 1), radius=radius * scale, fill=255)
    return mask.resize(size, Image.Resampling.LANCZOS)


def gradient_alpha(
    size: tuple[int, int],
    *,
    start: float = 0.0,
    end: float = 1.0,
    maximum: int = 255,
    vertical: bool = True,
    reverse: bool = False,
) -> Image.Image:
    count = size[1] if vertical else size[0]
    strip = Image.new("L", (1, count) if vertical else (count, 1))
    for position in range(count):
        fraction = min(1.0, max(0.0, (position / max(1, count - 1) - start) / max(0.001, end - start)))
        value = int(maximum * ((1.0 - fraction) if reverse else fraction))
        strip.putpixel((0, position) if vertical else (position, 0), value)
    return strip.resize(size)


def masked(pixels: Image.Image, mask: Image.Image) -> Image.Image:
    result = pixels.convert("RGBA")
    result.putalpha(ImageChops.multiply(result.getchannel("A"), mask))
    return result


def composite_fitted(
    canvas: Image.Image,
    source: Image.Image,
    box: tuple[int, int, int, int],
    *,
    shape: str = "rounded",
    radius: int = 16,
    cut: int = 28,
    focus: tuple[float, float] = (0.5, 0.2),
    contain: bool = False,
) -> None:
    x, y, right, bottom = box
    size = (right - x, bottom - y)
    pixels = fitted(source, size, focus=focus, contain=contain)
    canvas.alpha_composite(masked(pixels, shape_mask(size, shape=shape, radius=radius, cut=cut)), (x, y))
