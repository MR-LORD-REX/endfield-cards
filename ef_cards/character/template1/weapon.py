from typing import List
from PIL import Image, ImageDraw
import asyncio
import logging

from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font
from ...utils.char1 import build_stars

from endfield.models.weapon import WeaponSkill
from endfield.models.weapon import Gem, WeaponData, MainStat

font = get_font(size=20)
logger = logging.getLogger(__name__)


async def build_attri_level(base_lvl: int = 1, current_lvl: int = 1, max_lvl: int = 9) -> Image.Image | None:
    main_bg, gold, white, none_img = await asyncio.gather(
        asset_manager.get_asset('c1_weapon_attri_lvl_bg', (110, 20)),
        asset_manager.get_asset('c1_weapon_attri_lvl_gold', (14, 14)),
        asset_manager.get_asset('c1_weapon_attri_lvl_white', (14, 14)),
        asset_manager.get_asset('c1_weapon_attri_lvl_none', (14, 14)),
    )
    if any(img is None for img in (main_bg, gold, white, none_img)):
        logger.warning("build_attri_level: one or more level indicator assets failed to load")
        return None

    main_bg = main_bg.copy()
    for i in range(base_lvl):
        main_bg.alpha_composite(white, (7 + i * 10, 3))
    for i in range(base_lvl, current_lvl):
        main_bg.alpha_composite(gold, (7 + i * 10, 3))
    for i in range(current_lvl, max_lvl):
        main_bg.alpha_composite(none_img, (7 + i * 10, 3))
    return main_bg


async def build_attri_section(weapon_skill: WeaponSkill) -> Image.Image | None:
    attri_lvl, icon = await asyncio.gather(
        build_attri_level(weapon_skill.base_lvl, weapon_skill.current_lvl, weapon_skill.max_lvl),
        asset_manager.get_asset(str(weapon_skill.prop_id), (27, 27)),
    )
    if attri_lvl is None:
        logger.warning(f"build_attri_section: level bar is None for prop_id='{weapon_skill.prop_id}'")
        return None
    if icon is None:
        logger.warning(f"build_attri_section: icon not found for prop_id='{weapon_skill.prop_id}'")
        return None

    main_bg = Image.new("RGBA", (110, 57), (0, 0, 0, 0))
    main_bg.alpha_composite(attri_lvl, (0, 0))
    main_bg.alpha_composite(icon, (4, 30))

    draw = ImageDraw.Draw(main_bg)
    value_text = f"+{round(weapon_skill.value * 100, 1)}%" if weapon_skill.value < 1.5 else f"+{int(weapon_skill.value)}"
    draw.text((35, 33), value_text, font=font, fill=(255, 255, 255))

    return main_bg


async def build_gem(gem: Gem) -> Image.Image:
    if gem is None:
        logger.warning("build_gem: no gem data provided, returning transparent placeholder")
        return Image.new("RGBA", (70, 70), (0, 0, 0, 0))

    bg_key = 'c1_weapon_gem_bg_gold' if gem.rarity >= 4 else 'c1_weapon_gem_bg_gray'

    bg, inner, outer = await asyncio.gather(
        asset_manager.get_asset(bg_key, (70, 70)),
        asset_manager.get_asset_from_url(gem.inner_icon_url, (70, 70)),
        asset_manager.get_asset_from_url(gem.cover_icon_url, (70, 70)),
    )

    if bg is None:
        logger.warning(f"build_gem: background image failed to load for rarity {gem.rarity}")
        return Image.new("RGBA", (70, 70), (0, 0, 0, 50))

    bg = bg.copy()

    if inner is None or outer is None:
        logger.warning(f"build_gem: failed to load inner or outer icon for gem with rarity {gem.rarity}")
        return bg

    outer.alpha_composite(inner)
    bg.alpha_composite(outer)
    return bg


async def build_middle_bg(main_stat: MainStat, gem_d: Gem, pote_level: int = 0, lvl: int = 1) -> Image.Image:
    f32 = get_font(size=32)
    f48 = get_font(size=48)

    pote, attri_icon, middle_bg, gem = await asyncio.gather(
        asset_manager.get_asset(f"common_pote_{pote_level}", (60, 60)),
        asset_manager.get_asset(str(main_stat.prop_id), (36, 36)),
        asset_manager.get_asset('c1_weapon_middle_bg', (404, 73)),
        build_gem(gem_d),
    )

    lvl_frame = Image.new("RGBA", (36, 36), (0, 0, 0, 150))
    if attri_icon:
        x = (36 - attri_icon.width) // 2
        y = (36 - attri_icon.height) // 2
        lvl_frame.alpha_composite(attri_icon, (x, y))

    middle_frame = Image.new("RGBA", (404, 112), (0, 0, 0, 0))
    m_d = ImageDraw.Draw(middle_frame)

    middle_bg = middle_bg.copy()
    middle_frame.alpha_composite(middle_bg, (0, 15))
    middle_frame.alpha_composite(gem, (304, 39))
    middle_frame.alpha_composite(pote, (17, 0))
    middle_frame.alpha_composite(lvl_frame, (17, 72))

    m_d.text((60, 80), f"{main_stat.value}", font=font, fill=(255, 255, 255))
    m_d.text((188, 14), "/90", font=f32, fill=(255, 255, 255))
    m_d.text((126, 0), str(lvl), font=f48, fill=(255, 255, 255))

    return middle_frame




async def build_weapon_panel(weapon_data: WeaponData) -> Image.Image | None:
    stars, weap, line, m_d, sections = await asyncio.gather(
        build_stars(weapon_data.rarity),
        asset_manager.get_asset_from_url(weapon_data.icon_url, (164, 159)),
        asset_manager.get_asset('c1_weapon_line', (7, 30)),
        build_middle_bg(weapon_data.main_stat, weapon_data.gem, weapon_data.refine_lv, weapon_data.level),
        asyncio.gather(*[build_attri_section(skill) for skill in weapon_data.skills]),
    )

    main_frame = Image.new("RGBA", (756, 297), (0, 0, 0, 0))
    mf_draw = ImageDraw.Draw(main_frame)

    main_frame.alpha_composite(stars, (455, 73))

    if weap is not None:
        main_frame.alpha_composite(weap, (584, 0))

    main_frame.alpha_composite(line, (563, 28))
    mf_draw.text((563, 28), weapon_data.name, font=get_font(size=24), anchor="rt", fill=(255, 255, 255))

    skill_panel = Image.new("RGBA", (344, 57), (0, 0, 0, 0))
    for i, sec in enumerate(sections):
        if sec is None:
            logger.warning(f"build_weapon_panel: section {i} is None, skipping composite")
            continue
        skill_panel.alpha_composite(sec, (i * 117, 0))
        skill_panel.resize((404, 57))

    main_frame.alpha_composite(m_d, (339, 113))
    main_frame.alpha_composite(skill_panel, (339, 240))
    
    return main_frame