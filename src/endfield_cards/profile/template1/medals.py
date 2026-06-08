# Copyright (c) 2026 MR-LORD-REX
# All rights reserved.



from typing import Literal 
from PIL import Image, ImageDraw, ImageFont
import asyncio

from endfield.models.basic.profile import Medals

from ...utils.assets.core import asset_manager

def paste_medal_icon(base_img:Image.Image,medal_icon:Image.Image,index:int):
    index=index-1
    if index%2==0:
        base_img.alpha_composite(medal_icon,(147+index//2*78,13))
    else:
        base_img.alpha_composite(medal_icon,(187+index//2*78,79))


async def build_medals(medals:Medals) -> Image.Image:
    medals_bg=await asset_manager.get_asset("pfp1_medals_bg",size=(635,179))
    medals_bg=medals_bg.copy()
    medal_icons=[]
    for medal in medals.medals:
        medal_icons.append(asset_manager.get_asset_from_url(medal.icon_url,size=(90,90)))
    medal_icons=await asyncio.gather(*medal_icons)
    t=[]
    for medal_icon,medal in zip(medal_icons,medals.medals):
        t.append(asyncio.to_thread(paste_medal_icon,medals_bg,medal_icon,medal.index))
    await asyncio.gather(*t)
    return medals_bg