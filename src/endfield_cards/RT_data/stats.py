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


from PIL import Image , ImageDraw , ImageFont
import asyncio
from datetime import datetime , timedelta , timezone

from .hexagon import hex_bar
from ..utils.assets.core import asset_manager
from ..utils.fonts.fonts import get_font
from ..models.live_stats import LiveStats
from endfield.models.auth.game_stats import GameStats , Settlement

f64=get_font(size=64)
f32=get_font(size=32)
f48=get_font(size=48)


def draw_rect_bracket()-> Image.Image:
    img=Image.new("RGBA",(8,16),(0,0,0,0))
    # render [
    draw=ImageDraw.Draw(img)
    draw.rectangle((0,0,4,16),fill=(0,0,0,255))
    
    draw.rectangle((4,0,8,4),fill=(0,0,0,255))
    draw.rectangle((4,12,8,16),fill=(0,0,0,255))
    
    return img


def paste_text(
    draw: ImageDraw.ImageDraw, 
    text: str, position: tuple, 
    font: ImageFont.FreeTypeFont, 
    fill=(0,0,0)
    ):
    draw.text(position, text, font=font, fill=fill)


async def render_live_stats(stats: GameStats) -> LiveStats:
    main_bg= await asset_manager.get_asset('RT_data_live_data_bg',size=(1024,355))
    main_bg=main_bg.copy()
    f20=get_font(size=20)
    f32=get_font(size=32)
    f24=get_font(size=24)
    
    draw=ImageDraw.Draw(main_bg)
    
    sanity = f"{stats.sanity_point.current}/{stats.sanity_point.max}"
    daily = f"{stats.daily_points.current}"
    weelky = f"{stats.weekly_points.score}"
    BP= f"{stats.battle_pass.current_level}"
    delta=(stats.sanity_point.full_recover_at - 
            datetime.now(timezone.utc) 
            if stats.sanity_point.full_recover_at else 0
        )
    
    if isinstance(delta, timedelta) and delta.total_seconds() < 0:
        delta = timedelta(seconds=0)
        
    minutes= int(delta.total_seconds()//60) if stats.sanity_point.full_recover_at else 0
    second= int(delta.total_seconds()) if stats.sanity_point.full_recover_at else 0
    # format minutes to 00:00
    recovertime = f"{minutes//60:02d}H:{minutes%60:02d}M"
    
    t=[]
    t.append(asyncio.to_thread(paste_text, draw, sanity, (173,100), f20))
    t.append(asyncio.to_thread(paste_text, draw, daily, (819,47),f32))
    t.append(asyncio.to_thread(paste_text, draw, weelky, (843,132),f32))
    t.append(asyncio.to_thread(paste_text, draw, BP, (840,217),f32))
    t.append(asyncio.to_thread(paste_text, draw, recovertime, (114,286),f24))
    await asyncio.gather(*t)
    
    return LiveStats(
        full_recovery_seconds=second,
        full_recovery_minutes=minutes,
        full_recovery_time=stats.sanity_point.full_recover_at,
        img=main_bg
    )
    

def build_money_bar(
    bg: Image.Image,
    rect: Image.Image,
    value: int,
    max_value: int
):
    h_bar=hex_bar(value, max_value)
    h_bar=h_bar.resize((45,58))
    rect.alpha_composite(h_bar,(232,19))
    rect_draw=ImageDraw.Draw(rect)
    
    rect_draw.text((30,23), f"{value//1000}K", font=f32, fill=(0,0,0,255))
    bg.alpha_composite(rect,(725,117))
    

def build_lvl_bar(
    bg: Image.Image,
    rect: Image.Image,
    brac: Image.Image,
    brac_180: Image.Image,
    lvl: int
):  
    lvl_bar=Image.new("RGBA",(255,8),(0,0,0,0))
    draw=ImageDraw.Draw(lvl_bar)
    draw.rectangle((0,0,255,8),fill=(0,0,0,255))
    
    rect_draw=ImageDraw.Draw(rect)
    rect_draw.text((37,12), str(lvl), font=f64, fill=(0,0,0,255))
    rect_draw.text((78,41), "LV.", font=f32, fill=(0,0,0,255))
    
    rect.alpha_composite(brac,(128,50))
    rect.alpha_composite(lvl_bar,(141,54))
    rect.alpha_composite(brac_180,(401,50))
    
    bg.alpha_composite(rect,(152,117))
    
    
    
async def render_settlement(
    bg: Image.Image,
    lvl_rect: Image.Image,
    lvl_rect_small: Image.Image,
    char_circle: Image.Image,
    icon_url: str|None,
    settlement: Settlement
)-> Image.Image:
    
    bg=bg.copy()
    draw=ImageDraw.Draw(bg)
    lvl_rect=lvl_rect.copy()
    lvl_rect_small=lvl_rect_small.copy()
    char_circle=char_circle.copy()
    
    brac=draw_rect_bracket()
    brac=brac.copy()
    brac_180=brac.rotate(180)
    
    if icon_url:
        char_icon=await asset_manager.get_asset_from_url(icon_url,size=(75,75))
        char_circle.alpha_composite(char_icon,(5,5))
    bg.alpha_composite(char_circle,(45,117))
    
    draw.text((45,17), settlement.name, font=f48, fill=(0,0,0,255))
    
    build_lvl_bar(bg, lvl_rect, brac, brac_180, settlement.level)
    build_money_bar(bg, lvl_rect_small, settlement.remaining_money, settlement.max_money)
    
    return bg
    
    

async def render_factory(
    stats: GameStats
    ) -> Image.Image:
    
    main_bg, fact_rect, fact_rect_small, reg_lvl, char_circle , settle_bg = await asyncio.gather(
        asset_manager.get_asset('RT_data_factory_bg',size=(1156,1755)),
        asset_manager.get_asset('RT_data_fact_lvl_rect',size=(437,83)),
        asset_manager.get_asset('RT_data_fact_lvl_rect',size=(313,83)),
        asset_manager.get_asset('RT_data_reg_lvl',size=(98,47)),
        asset_manager.get_asset('RT_data_fact_char_circle',size=(85,85)),
        asset_manager.get_asset('RT_data_settle_bg',size=(1057,236))
    )
    f40=get_font(size=40)
    
    main_bg=main_bg.copy()
    main_draw=ImageDraw.Draw(main_bg)
    
    x=50
    region_y=196
    for i_, region in enumerate(stats.regions.all):
        t=[]
        
        reg_lvl_copy=reg_lvl.copy()
        reg_lvl_copy_draw=ImageDraw.Draw(reg_lvl_copy)
        reg_lvl_copy_draw.text((reg_lvl_copy.width//2, reg_lvl_copy.height//2), f"{region.factory_level} Lv.", font=f40, fill=(255,255,255,255), anchor="mm")
        main_bg.alpha_composite(reg_lvl_copy,(364 if i_==0 else 330, 95 if i_==0 else 1078))
        
        main_draw.text((652,92 if i_==0 else 1080), f"{region.factory_money.current//1000}K/{region.factory_money.max//1000}K", font=f32, fill=(0,0,0,255))
        
        for settlement in region.settlements:
            t.append(render_settlement(settle_bg, fact_rect, fact_rect_small, char_circle, settlement.char_icon, settlement))
        settles=await asyncio.gather(*t)
        for i,settle in enumerate(settles):
            main_bg.alpha_composite(settle,(x,region_y + 260*i))
        region_y += (len(settles)-1)*260 + 236 + 229
        
    return main_bg
    