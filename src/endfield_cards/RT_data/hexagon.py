from PIL import Image, ImageDraw
import math
import numpy as np

def hex_bar(
    value: float,
    max_value: float,
    size: int = 100,
    fill_color: tuple = (220, 220, 0),
    empty_color: tuple = (160, 160, 160),
    padding: int = 4,
) -> Image.Image:
    
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size / 2, size / 2
    r = size / 2 - padding

    # Flat-top hexagon: angles 0°, 60°, 120°, 180°, 240°, 300°
    points = [
        (cx + r * math.cos(math.radians(60 * i - 90)),
        cy + r * math.sin(math.radians(60 * i - 90)))
        for i in range(6)
    ]

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)

    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    ratio = max(0.0, min(1.0, value / max_value if max_value > 0 else 0))
    fill_top_y = max_y - ratio * (max_y - min_y)

    draw.polygon(points, fill=(*empty_color, 255))

    if ratio > 0:
        fill_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ImageDraw.Draw(fill_layer).rectangle(
            [(0, fill_top_y), (size, size)],
            fill=(*fill_color, 255),
        )
        clipped = np.minimum(
            np.array(fill_layer.getchannel("A")),
            np.array(mask),
        )
        fill_layer.putalpha(Image.fromarray(clipped.astype(np.uint8)))

        img = Image.alpha_composite(img, fill_layer)

    return img


