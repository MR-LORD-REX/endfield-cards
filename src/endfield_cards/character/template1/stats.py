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


from typing import Dict, List
from PIL import Image , ImageDraw, ImageFont
import asyncio

from endfield.models.basic.character import ComputedStatsWithDetails , StatDetail
from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font , put_text_in_center

async def add_main_stats(main_bg:Image.Image , stats: List[StatDetail]) -> None:
    base_x=38
    base_y=79
    font=get_font(size=28)
    for i , stat in enumerate(stats):
        value=stat.value
        rect=await asset_manager.get_asset('c1_stats_top_stat_rect',(100,68))
        rect=rect.copy()
        if stat.main_attri:
            main_attri_img=await asset_manager.get_asset('c1_stats_main_stat',(106,5))
            rect.alpha_composite(main_attri_img,(0,63))
        elif stat.sub_attri:
            sub_attri_img=await asset_manager.get_asset('c1_stats_sub_stat',(106,5))
            rect.alpha_composite(sub_attri_img,(0,63))
        r_draw=ImageDraw.Draw(rect)
        put_text_in_center(f"{int(value)}",font,r_draw,(255,255,255))
        main_bg.alpha_composite(rect,(base_x+i*133,base_y))
        stat_img=await asset_manager.get_asset(str(stat.stat_id),(64,64))
        main_bg.alpha_composite(stat_img,((base_x+22)+i*133,base_y-40))
        
async def add_sub_stats(main_bg:Image.Image ,draw:ImageDraw.ImageDraw , stat: StatDetail,index) -> None:
    value_tr_x=540
    value_tr_y=186
    icon_pos=(16,177)
    name=(65,182)
    font=get_font(size=24)
    icon_img=await asset_manager.get_asset(str(stat.stat_id),(42,42))
    main_bg.alpha_composite(icon_img,(icon_pos[0],icon_pos[1]+index*52))
    draw.text((name[0],name[1]+index*52),stat.name,font=font,fill=(255,255,255))
    value_text=f"{int(stat.value)}" if stat.value > 2 else f"{round(stat.value*100,1)}%"
    draw.text((value_tr_x,value_tr_y+index*52),value_text,font=font,fill=(255,255,255),anchor="rt")
            
        

async def build_stats_panel(stats: ComputedStatsWithDetails) -> Image.Image | None:
    main_bg = Image.new("RGBA",(552,659),(0,0,0,0))
    main_bg=main_bg.copy()
    draw=ImageDraw.Draw(main_bg)
    await add_main_stats(main_bg,stats.all[11:15])
    sub_stats=stats.all[0:5]
    sub_stats.append(stats.all[8])
    t=[]
    for stat in [stats.all[7]] + stats.all[15:23]:
        if stat.value:
            sub_stats.append(stat)
    for i , stat in enumerate(sub_stats):
        t.append(add_sub_stats(main_bg,draw,stat,i))
    await asyncio.gather(*t)
    return main_bg
    
    
    
    