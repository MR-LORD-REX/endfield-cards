from typing import Dict, List
from PIL import Image , ImageDraw, ImageFont
import asyncio
import logging

from endfield.models.character import SkillInfo , SkillMeta , ComputedStatsWithDetails , StatDetail
from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font , put_text_in_center
from ...utils.pil import alpha_composite_center

logger=logging.getLogger(__name__)

async def build_skill(skill_info: SkillInfo, value: float | None = None,id:str|None=None) -> Image.Image:
    new= Image.new("RGBA",(132,100),(0,0,0,0))
    font=get_font(size=16)
    if value:
        upper=await asset_manager.get_asset('c1_skill_upper',(132,33))
        upper=upper.copy()
        r_draw=ImageDraw.Draw(upper)
        icon=await asset_manager.get_asset(str(id),(33,33))
        upper.alpha_composite(icon,(2,0))
        value_text=f"{round(value*100,1)}%"
        r_draw.text((40,7),value_text,font=font,fill=(255,255,255))
        
    skill_bg= await asset_manager.get_asset('c1_skill_icon_bg',(77,77))
    skill_bg=skill_bg.copy()
    skill_inner= await asset_manager.get_asset('c1_skill_center',(70,70))
    skill_inner=skill_inner.copy()
    skill_icon= await asset_manager.get_asset_from_url(str(skill_info.icon_url),(70,70))
    if skill_icon:
        await alpha_composite_center(skill_inner,skill_icon)
    else:
        logger.warning(f"Failed to load skill icon from URL: {skill_info.icon_url}")
    await alpha_composite_center(skill_bg,skill_inner)
    lvl_img= await asset_manager.get_asset('c1_skill_lvl',(28,28))
    lvl_img=lvl_img.copy()
    r_draw=ImageDraw.Draw(lvl_img)
    put_text_in_center(f"{int(skill_info.enhanced_level)}",font,r_draw,(255,255,255))
    skill_bg.alpha_composite(lvl_img,(49,49))

    new.alpha_composite(skill_bg,(28,21))
    if value:
        new.alpha_composite(upper,(0,0))
    return new

async def build_skill_panel(skill_meta: SkillMeta,stats:ComputedStatsWithDetails|None=None) -> Image.Image:
    main_bg = Image.new("RGBA",(537,100),(0,0,0,0))
    main_bg=main_bg.copy()
    flow=[]
    flow.append(skill_meta.disp_normal_atk_skill)
    flow.append(skill_meta.normal_skill)
    flow.append(skill_meta.combo_skill)
    flow.append(skill_meta.ultimate_skill)
    
    map={str(_id):index for index, _id in enumerate(flow)}
    skills=sorted(skill_meta.skills,key=lambda s: map.get(str(s.skill_id),float('inf')))
    t=[]
    values=[]
    values.append((stats.all[5].value,stats.all[5].stat_id))
    values.append((stats.all[9].value,stats.all[9].stat_id))
    values.append((stats.all[10].value,stats.all[10].stat_id))
    values.append((stats.all[6].value,stats.all[6].stat_id))
    
    for skill , val in zip(skills,values):
        t.append(build_skill(skill,val[0],val[1]))
        
    skill_imgs=await asyncio.gather(*t)
    for i , img in enumerate(skill_imgs):
        main_bg.alpha_composite(img,(i*132+(3*i),0))
    return main_bg