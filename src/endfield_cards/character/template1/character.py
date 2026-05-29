
# Copyright (c) 2026 MR-LORD-REX
# All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.


from PIL import Image, ImageDraw, ImageFilter
import asyncio
import logging
import numpy as np
import colorsys
import random

from ...utils.assets.core import asset_manager
from endfield.models.character import CharacterData
from ...utils.char1 import get_pote , build_stars
from ...utils.fonts.fonts import get_font

logger = logging.getLogger(__name__)



def _sample_dominant_hue(img: Image.Image) -> tuple[int, int, int]:
    small = img.resize((80, 80)).convert("RGBA")
    arr = np.array(small).astype(float)

    hue_bins: dict[int, int] = {}
    for row in arr:
        for r, g, b, a in row:
            if a < 100:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if s > 0.30 and 0.40 < l < 0.85:
                bucket = int(h * 60)
                hue_bins[bucket] = hue_bins.get(bucket, 0) + 1

    if not hue_bins:
        return (180, 60, 30)

    dominant = max(hue_bins, key=hue_bins.get)
    rgb = colorsys.hls_to_rgb(dominant / 60.0, 0.55, 0.90)
    return tuple(int(c * 255) for c in rgb)


def _sample_zone_colors(img: Image.Image, num_zones: int = 3) -> list[tuple[int, int, int]]:
    w, h = img.size
    strip_x = int(w * 0.6)
    strip = img.crop((strip_x, 0, min(strip_x + 10, w), h)).convert("RGB")
    arr = np.array(strip).astype(float)

    zone_h = h // num_zones
    colors = []

    for z in range(num_zones):
        zone = arr[z * zone_h:(z + 1) * zone_h]
        pixels = zone.reshape(-1, 3)
        pixels = pixels[pixels.max(axis=1) > 10]

        if len(pixels) == 0:
            colors.append((34, 34, 68))
            continue

        avg = pixels.mean(axis=0) / 255.0
        h_val, l_val, s_val = colorsys.rgb_to_hls(*avg)

        s_val = min(1.0, s_val * 1.3)
        l_val = max(0.05, min(0.70, l_val))

        rgb = colorsys.hls_to_rgb(h_val, l_val, s_val)
        colors.append(tuple(int(c * 255) for c in rgb))

    return colors



def _make_gradient_base(
    width: int,
    height: int,
    zone_colors: list[tuple[int, int, int]],
) -> Image.Image:
    base = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(base)

    zone_h = height // len(zone_colors)
    for i, (r, g, b) in enumerate(zone_colors):
        y0 = i * zone_h
        y1 = y0 + zone_h if i < len(zone_colors) - 1 else height
        dark = (int(r * 0.45), int(g * 0.40), int(b * 0.40), 255)
        draw.rectangle([0, y0, width, y1], fill=dark)

    return base


def _make_dot_grid(
    width: int,
    height: int,
    color: tuple[int, int, int],
    spacing: int = 10,
    radius: int = 1,
) -> Image.Image:
    r, g, b = color
    dot_color = (max(0, r - 50), max(0, g - 50), max(0, b - 50), 160)

    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for y in range(0, height, spacing):
        for x in range(0, width, spacing):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=dot_color)

    return layer


def _make_light_rays(
    width: int,
    height: int,
    color: tuple[int, int, int],
    num_rays: int = 10,
    seed: int = 42,
) -> Image.Image:
    r, g, b = color
    rng = random.Random(seed)
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    skew = height // 2
    for _ in range(num_rays):
        x = rng.randint(-width // 3, width)
        ray_w = rng.randint(30, 180)
        alpha = rng.randint(12, 45)
        pts = [
            (x, -20),
            (x + ray_w, -20),
            (x + ray_w - skew, height + 20),
            (x - skew, height + 20),
        ]
        draw.polygon(pts, fill=(r, g, b, alpha))

    return layer.filter(ImageFilter.GaussianBlur(radius=18))


def _make_radial_glow(
    width: int,
    height: int,
    color: tuple[int, int, int],
    center: tuple[int, int] | None = None,
    intensity: float = 0.55,
) -> Image.Image:
    if center is None:
        center = (width // 2, height // 2)

    r, g, b = color
    cx, cy = center
    Y, X = np.ogrid[:height, :width]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_dist = np.hypot(width, height) / 1.8

    alpha = np.clip(1.0 - dist / max_dist, 0, 1) ** 1.8
    alpha = (alpha * 255 * intensity).astype(np.uint8)

    arr = np.zeros((height, width, 4), dtype=np.uint8)
    arr[:, :, 0] = r
    arr[:, :, 1] = g
    arr[:, :, 2] = b
    arr[:, :, 3] = alpha

    return Image.fromarray(arr, "RGBA")


def _make_vignette(width: int, height: int) -> Image.Image:
    cx, cy = width // 2, height // 2
    Y, X = np.ogrid[:height, :width]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_dist = np.hypot(width, height) / 1.6

    alpha = np.clip(dist / max_dist, 0, 1) ** 1.4
    alpha = (alpha * 180).astype(np.uint8)

    arr = np.zeros((height, width, 4), dtype=np.uint8)
    arr[:, :, 3] = alpha

    return Image.fromarray(arr, "RGBA")


def _build_style_layers(
    width: int,
    height: int,
    splash: Image.Image,
    opacity: float = 0.5,
) -> Image.Image:
    splash = splash.convert("RGBA")

    dominant    = _sample_dominant_hue(splash)
    zone_colors = _sample_zone_colors(splash)

    base  = _make_gradient_base(width, height, zone_colors)
    glow  = _make_radial_glow(width, height, dominant)
    dots  = _make_dot_grid(width, height, dominant)
    rays  = _make_light_rays(width, height, dominant)
    vign  = _make_vignette(width, height)

    canvas = base.copy()
    canvas = Image.alpha_composite(canvas, glow)
    canvas = Image.alpha_composite(canvas, dots)
    canvas = Image.alpha_composite(canvas, rays)
    canvas = Image.alpha_composite(canvas, vign)

    r, g, b, a = canvas.split()
    a = a.point(lambda x: int(x * opacity))
    return Image.merge("RGBA", (r, g, b, a))

async def overlay_icons(
    base: Image.Image,
    draw: ImageDraw.ImageDraw,
    data: CharacterData):
    rarity=data.rarity
    stars,element, weap_type, profession, potential = await asyncio.gather(
        build_stars(rarity, size=(30,30)),
        asset_manager.get_asset(str(data.element),(45,45)),
        asset_manager.get_asset(str(data.weapon_type),(45,45)),
        asset_manager.get_asset(str(data.profession),(45,45)),
        asset_manager.get_asset(f'common_pote_{data.potential_level}',(105,105))
    )
    
    t=[]
    t.append(asyncio.to_thread(base.alpha_composite, stars, (661,658)))
    t.append(asyncio.to_thread(base.alpha_composite, element, (605,652)))
    t.append(asyncio.to_thread(base.alpha_composite, profession, (603,713)))
    t.append(asyncio.to_thread(base.alpha_composite, potential, (1174,510)))
    t.append(asyncio.to_thread(draw.text, (661, 720), data.name, fill=(255, 255, 255, 255), font=get_font(size=38)))
    t.append(asyncio.to_thread(draw.text, (1146, 713), f"{data.level}", fill=(255, 255, 255, 255), font=get_font(size=48)))
    t.append(asyncio.to_thread(draw.text, (1240, 707), "Lv.", fill=(255, 255, 255, 255), font=get_font(size=24)))
    t.append(asyncio.to_thread(draw.text, (1221,728), "/90", fill=(255, 255, 255, 255), font=get_font(size=32)))
    await asyncio.gather(*t)
    
async def build_main_frame(char_data: CharacterData,user_img:Image.Image|None=None) -> Image.Image:
    W, H = 1920, 800

    bg, splash , logo = await asyncio.gather(
        asset_manager.get_asset_from_url(char_data.bg_url, (776, 776)),
        asset_manager.get_asset_from_url(char_data.splash_url, (1369, 1495)),
        asset_manager.get_asset('logos_git_WA',(250,60))
    )


    if bg is None or splash is None:
        logger.warning(f"build_main_frame: failed to load bg or splash for '{char_data.name}'")
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))

    bg     = bg.convert("RGBA")
    splash = splash.convert("RGBA")

    style_layers = await asyncio.to_thread(_build_style_layers, W, H, splash, 0.5)

    main_bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    main_draw = ImageDraw.Draw(main_bg)
    main_bg.alpha_composite(logo, (1650,0))
    main_bg.alpha_composite(bg, (13, 3))
    main_bg.alpha_composite(style_layers, (0, 0))
    main_bg.alpha_composite(splash, (350, -243))

    
    await overlay_icons(main_bg, main_draw, char_data)
    
    return main_bg