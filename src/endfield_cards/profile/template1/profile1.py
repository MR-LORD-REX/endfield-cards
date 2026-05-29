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


from typing import Literal, List
from PIL import Image, ImageDraw, ImageFont
import asyncio

from .char_showcase import build_char_showcase
from .medals import build_medals
from endfield.models.profile import PlayerProfile , Medals 
from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font

f96=get_font(size=96)
f64=get_font(size=64)
f48=get_font(size=48)
f40=get_font(size=40)

def write_text(draw:ImageDraw.ImageDraw,text:str,pos:tuple,font:ImageFont.FreeTypeFont,fill:tuple):
    draw.text(pos,text,font=font,fill=fill)
    
async def build_avatar(profile:PlayerProfile)->Image.Image:
    main_bg=Image.new("RGBA",(1080,448),(0,0,0,0))
    icon,overlay=await asyncio.gather(
        asset_manager.get_asset_from_url(profile.avatar_url,size=(325,325)),
        asset_manager.get_asset("pfp1_avatar_layout",size=(1080,448))
    )
    main_bg.alpha_composite(icon,(57,61))
    overlay=overlay.copy()
    main_bg.alpha_composite(overlay,(0,0))
    draw=ImageDraw.ImageDraw(main_bg)
    t=[]
    t.append(asyncio.to_thread(write_text,draw,profile.name,pos=(434,61),font=f48,fill=(255,255,255)))
    t.append(asyncio.to_thread(write_text,draw,str(profile.adventure_level),pos=(843,166),font=f48,fill=(255,255,255)))
    t.append(asyncio.to_thread(write_text,draw,str(profile.world_level),pos=(843,235),font=f48,fill=(255,255,255)))
    t.append(asyncio.to_thread(write_text,draw,str(profile.uid),pos=(445,351),font=f40,fill=(255,255,255)))
    await asyncio.gather(*t)
    
    return main_bg
    

async def build_profile1(profile:PlayerProfile)->Image.Image:
    bg,logo=await asyncio.gather(
        asset_manager.get_asset('pfp1_pfp_bg',size=(1080,1467)),
        asset_manager.get_asset('logos_git_WA',size=(320,74))
    )
    bg=bg.copy()
    draw=ImageDraw.ImageDraw(bg)
    t=[]
    
    domain0_level = str(profile.domain_progress[0].level) if len(profile.domain_progress) > 0 else "-"
    domain1_level = str(profile.domain_progress[1].level) if len(profile.domain_progress) > 1 else "-"

    t.append(asyncio.to_thread(write_text, draw, domain1_level, pos=(403, 1259), font=f64, fill=(0,0,0)))
    t.append(asyncio.to_thread(write_text, draw, domain0_level, pos=(815, 1259), font=f64, fill=(0,0,0)))
    t.append(asyncio.to_thread(write_text,draw,str(profile.char_count),pos=(120,950),font=f96,fill=(0,0,0)))
    t.append(asyncio.to_thread(write_text,draw,str(profile.weapon_count),pos=(426,950),font=f96,fill=(0,0,0)))
    t.append(asyncio.to_thread(write_text,draw,str(profile.doc_count),pos=(732,950),font=f96,fill=(0,0,0)))
    
    await asyncio.gather(*t)
    
    t.clear()
    chars,avatar=await asyncio.gather(
        build_char_showcase(profile=profile),
        build_avatar(profile)
    )
    bg.alpha_composite(chars.resize(size=(991,406)),(44,531))
    bg.alpha_composite(avatar,(0,0))
    bg.alpha_composite(logo,(760,0))
    
    return bg
    