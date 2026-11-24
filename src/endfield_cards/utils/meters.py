"""Bounded progress graphics with source values rendered separately."""

from PIL import Image, ImageDraw

from endfield_cards.utils.drawing import PageCanvas


def bar(c: PageCanvas, box: tuple[int, int, int, int], ratio: float) -> None:
    x, y, right, bottom = box
    height = bottom - y
    c.draw.rounded_rectangle(box, radius=height // 2, fill=c.line)
    length = int((right - x) * min(1.0, max(0.0, ratio)))
    if length:
        c.draw.rounded_rectangle((x, y, x + max(height, length), bottom), radius=height // 2, fill=c.accent)


def ring(c: PageCanvas, x: int, y: int, size: int, ratio: float) -> None:
    scale, stroke = 3, max(14, size // 12)
    layer = Image.new("RGBA", (size * scale, size * scale))
    d = ImageDraw.Draw(layer)
    box = (2, 2, size * scale - 3, size * scale - 3)
    d.arc(box, 0, 360, fill=c.line, width=stroke * scale)
    if ratio > 0:
        d.arc(box, -90, -90 + 360 * min(1.0, ratio), fill=c.accent, width=stroke * scale)
    c.image.alpha_composite(layer.resize((size, size), Image.Resampling.LANCZOS), (x, y))
