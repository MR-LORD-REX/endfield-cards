from typing import Literal, List
from PIL import Image, ImageDraw, ImageFont
import asyncio

from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font

from endfield.models.auth.allc import AllCharacters , Character

f24= get_font("EF_fonts",size=24)
f32= get_font("EF_fonts",size=32)
f40= get_font("EF_fonts",size=40)

async def build_char(
    char:Character,
)-> Image.Image:
    bg=await asset_manager.get_asset(f"allc_{char.rarity}star",size=(232,383))
    if not bg:
        raise ValueError(f"Failed to load background for rarity {char.rarity}")
    bg=bg.copy()
    draw=ImageDraw.Draw(bg)
    char_icon=await asset_manager.get_asset_from_url(char.rect_icon,size=(232,326))
    if char_icon:
        bg.alpha_composite(char_icon,(0,0))
    ele,prof,pote,phase=await asyncio.gather(
        asset_manager.get_asset(f"{char.element}",size=(40,40)),
        asset_manager.get_asset(f"{char.proffesion}",size=(40,40)),
        asset_manager.get_asset(f"common_pote_{char.potential_level}",size=(64,64)),
        asset_manager.get_asset(f"phase_{char.evolve_phase}",size=(50,50)),
    )
    if ele:
        bg.alpha_composite(ele,(7,54))
    if prof:
        bg.alpha_composite(prof,(7,5))
        
    if pote:
        bg.alpha_composite(pote,(0,262))
    if phase:
        bg.alpha_composite(phase,(182,276))
    
    draw.text((7, 338), f"{char.name}", fill=(0, 0, 0, 255), font=f24)
    draw.text((100,290), f"Lv.{char.level}", fill=(0, 0, 0, 255), font=f24)
    
    return bg

async def build_allc(
    allc:AllCharacters,
)-> Image.Image:
    H=40+(383*len(allc.characters)//4)+(26*(len(allc.characters)//4))+170
    main_bg=Image.new("RGBA",(1080,H),(220,220,220,255))
    draw=ImageDraw.Draw(main_bg)
    txt="Operators"
    draw.text((437,20), txt, fill=(0, 0, 0, 255), font=f40)
    tasks=[build_char(char) for char in allc.characters]
    chars=await asyncio.gather(*tasks)
    t=[]
    for i , char in enumerate(chars):
        x=(i%4)*(232+21) + 44
        y=(i//4)*(383+26) + 80
        t.append(asyncio.to_thread(main_bg.alpha_composite,char,(x,y)))
    await asyncio.gather(*t)
    return main_bg