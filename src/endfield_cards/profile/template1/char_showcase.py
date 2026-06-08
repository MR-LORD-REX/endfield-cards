# Copyright (c) 2026 MR-LORD-REX
# All rights reserved.



from typing import Literal 
from PIL import Image, ImageDraw, ImageFont
import asyncio

from endfield.models.basic.profile import PlayerProfile , ProfileCharacter

from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font

f10=get_font(size=10)

def paste_char_icon(base_img:Image.Image,char_icon:Image.Image,index:int):
    base_img.alpha_composite(char_icon,(151+index*104,91))


async def get_bottom(element:str,lvl:int)->Image.Image:
    ele,bg=await asyncio.gather(
        asset_manager.get_asset(element,size=(16,16)),
        asset_manager.get_asset("pfp_char_bottom",size=(96,25))
    )
    bg=bg.copy()
    ele=ele.copy()
    bg.alpha_composite(ele,(5,0))
    draw=ImageDraw.ImageDraw(bg)
    draw.text((69,4),f"{lvl}",font=f10,fill=(0,0,0))
    return bg

async def build_char_icon(char:ProfileCharacter)->Image.Image:
    char_icon,bg,btm,prof=await asyncio.gather(
        asset_manager.get_asset_from_url(char.round_icon_url,size=(107,107)),
        asset_manager.get_asset("pfp_char_bg",size=(96,139)),
        get_bottom(char.element,char.level),
        asset_manager.get_asset(char.profession,size=(16,16))
    )
    bg=bg.copy()
    bg.alpha_composite(char_icon,(-6,16))
    bg.alpha_composite(btm,(0,114))
    bg.alpha_composite(prof,(5,4))
    return bg

async def build_char_showcase(profile:PlayerProfile)->Image.Image:
    bg=await asset_manager.get_asset("pfp_char_show_bg",size=(607,251))
    bg=bg.copy()
    t=[]
    for char in profile.characters:
        t.append(build_char_icon(char))
    char_icons=await asyncio.gather(*t)
    t.clear()
    for i,char_icon in enumerate(char_icons):
        t.append(asyncio.to_thread(paste_char_icon,bg,char_icon,i))
    await asyncio.gather(*t)
    return bg