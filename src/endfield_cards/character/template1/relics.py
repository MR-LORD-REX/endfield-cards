# Copyright (c) 2026 MR-LORD-REX
# All rights reserved.


from typing import List
from PIL import Image, ImageDraw, ImageFont
import logging
import asyncio

logger = logging.getLogger(__name__)

from endfield.models.basic.equipment import EquipData, AttrModifier

from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font, put_text_in_center
from ...utils.char1 import get_relic_level_image

_FONT_20 = get_font(size=20)

_IMG_X = 99
_TXT_X = 151


async def render_attributes(
    attr: AttrModifier,
    bg_img: Image.Image,
    bg_draw: ImageDraw.ImageDraw,
    index: int,
):
    img_y = 10 + index * 46

    if attr.enhance_level > 1:
        stat_img, enc_img = await asyncio.gather(
            asset_manager.get_asset(str(attr.attr_type), (34, 34)),
            get_relic_level_image(attr.enhance_level),
        )
    else:
        stat_img = await asset_manager.get_asset(str(attr.attr_type), (34, 34))
        enc_img = None

    if stat_img is None:
        logger.warning(f"Stat image for attr_type '{attr.attr_type}' not found")
        return

    if enc_img is not None:
        bg_img.alpha_composite(enc_img, (241, img_y + 15))

    bg_img.alpha_composite(stat_img, (_IMG_X, img_y))

    value = f"{round(attr.value * 100, 1)}%" if attr.value < 1.5 else f"{int(attr.value)}"
    bg_draw.text((151, img_y + 7), f"+{value}", font=_FONT_20, fill=(255, 255, 255))


async def build_relic(equip_data: EquipData) -> Image.Image | None:
    main_attr = equip_data.attr_modifiers[0]
    has_extra = len(equip_data.attr_modifiers) > 4

    coros = [
        asset_manager.get_asset("c1_relic_bg", (272, 144)),
        asset_manager.get_asset(str(main_attr.attr_type), (30, 30)),
        asset_manager.get_asset_from_url(equip_data.icon_url, (115, 124)),
    ]
    fetch_gold = equip_data.rarity == 5
    fetch_extra = has_extra

    if fetch_gold:
        coros.append(asset_manager.get_asset("c1_relic_gold_line"))
    if fetch_extra:
        coros.append(
            asset_manager.get_asset(
                str(equip_data.attr_modifiers[4].attr_type), (34, 34)
            )
        )

    results = await asyncio.gather(*coros)

    bg_img = results[0].copy()
    main_stat_img = results[1]
    icon = results[2]
    idx = 3
    gold_line = results[idx] if fetch_gold else None
    idx += fetch_gold
    extra_stat = results[idx] if fetch_extra else None

    if gold_line:
        bg_img.alpha_composite(gold_line, (0, -2))

    bg_draw = ImageDraw.Draw(bg_img)
    bg_img.alpha_composite(icon, (-7, 29))
    bg_img.alpha_composite(main_stat_img, (5, 5))
    bg_draw.text((42, 11), f"+{int(main_attr.value)}", font=_FONT_20, fill=(0, 0, 0))

    if extra_stat:
        bg_img.alpha_composite(extra_stat, (72, 100))

    await asyncio.gather(
        *[
            render_attributes(sub_attr, bg_img, bg_draw, i)
            for i, sub_attr in enumerate(equip_data.attr_modifiers[1:4])
        ]
    )
    return bg_img


async def build_relic_panel(equips: List[EquipData]) -> Image.Image:
    new = Image.new("RGBA", (563, 300), (0, 0, 0, 0))
    equips = sorted(equips, key=lambda x: x.slot_id)
    equips[1], equips[2] = equips[2], equips[1]
    equips[0], equips[2] = equips[2], equips[0]

    relic_imgs = await asyncio.gather(*[build_relic(equip) for equip in equips])

    for i, img in enumerate(relic_imgs):
        if img is None:
            continue
        x = 0 if i % 2 == 0 else 291
        y = (i // 2) * 157
        new.alpha_composite(img, (x, y))
    return new