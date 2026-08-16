from typing import Literal, List
from PIL import Image, ImageDraw, ImageFont
import asyncio

from ...utils.assets.core import asset_manager
from ...utils.fonts.fonts import get_font

from endfield.models.auth.indie_hard import IndieHardGroup, DungeonGroup , Achievement, AchievementData , Dungeon ,IndieHard , IndieHardCharacter

f20=get_font("EF_fonts",size=20)
f24=get_font("EF_fonts",size=24)
f32=get_font("EF_fonts",size=32)
f36=get_font("EF_fonts",size=36)

element_map = {
    "Electric":"Pulse",
    "Physical":"Physical",
    "Cryo": "Cryst",
    "Nature": "Natural",
    "Heat":"Fire",
}
# MARCH 10 2026 AT 12:00 AM UTC
def ts_to_day(ts:int)->str:
    from datetime import datetime, timezone
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%B %d %Y at %I:%M %p UTC")

def sec_to_min(sec:int)->str:
    m, s = divmod(sec, 60)
    return f"{m}m:{s}s"
    

async def build_completion(
    clears: List[DungeonGroup]
)-> Image.Image:
    total=len(clears)
    W=206*total+10*(total-1)
    main_bg = Image.new("RGBA", (W,22), (0,0,0,0))
    done , not_done = await asyncio.gather(
        asset_manager.get_asset("monu_done",size=(206,22)),
        asset_manager.get_asset("monu_not_done",size=(206,22))
    )
    if not done or not not_done:
        raise ValueError("Failed to load done or not_done images for completion bar.")
    for i,clear in enumerate(clears):
        if clear.normal_dungeon.is_pass or clear.hard_dungeon.is_pass:
            main_bg.alpha_composite(done,(i*216,0))
        else:
            main_bg.alpha_composite(not_done,(i*216,0))
    
    return main_bg.resize((638,10))

async def domain_card(data: IndieHardGroup) -> Image.Image:
    main_bg = await asset_manager.get_asset("monu_bg",size=(991,332))
    if not main_bg:
        raise ValueError("Failed to load main background image for monument card.")
    main_bg = main_bg.copy()
    draw = ImageDraw.Draw(main_bg)
    if data.achieve.level>0:
        achivement_icon = await asset_manager.get_asset_from_url(data.achieve.achievement_data.plated_icon, size=(115, 115))
        if achivement_icon:
            main_bg.alpha_composite(achivement_icon, (838,153))
            txt="Engraved Medal Aquired"
            draw.text((297,197), txt, font=f24, fill=(255, 255, 255, 255))
    else:
        txt="Medal not Aquired"
        draw.text((297,197), txt, font=f24, fill=(255, 255, 255, 255))
    domain_icon= await asset_manager.get_asset_from_url(data.pic, size=(272,340))
    if domain_icon:
        main_bg.alpha_composite(domain_icon, (0,0))
    domain_name=data.name
    draw.text((273,29), domain_name, font=f36, fill=(255, 255, 255, 255))
    comp=await build_completion(data.dungeon_groups)
    main_bg.alpha_composite(comp,(331,93))
    total=len(data.dungeon_groups)
    normal=sum(1 for d in data.dungeon_groups if d.normal_dungeon.is_pass)
    hard=sum(1 for d in data.dungeon_groups if d.hard_dungeon.is_pass)
    txt=f"Normal Cleared: {normal}/{total} | Agony Cleared: {hard}/{total}"
    draw.text((297, 275), txt, font=f24, fill=(255,255, 255, 255))
    
    return main_bg

async def Build_monument_card(data: IndieHard) -> Image.Image:
    W=1080
    H=40 + 332*len(data.indie_hard_groups) + 10*(len(data.indie_hard_groups)-1)
    main_bg = Image.new("RGBA", (W,H), (30,30,30,255))
    t=[]
    for domain in data.indie_hard_groups:
        t.append(domain_card(domain))
    cards=await asyncio.gather(*t)
    for i,card in enumerate(cards):
        main_bg.alpha_composite(card,(44,40+i*(332+10)))
    return main_bg


async def render_char(
    char: IndieHardCharacter
) -> Image.Image:
    bg = await asset_manager.get_asset(f"monu_{char.rarity.value}star", size=(133,133))
    if not bg:
        raise ValueError(f"Failed to load background image for character {char.char_id} with rarity {char.rarity}.")
    lvl=Image.new("RGBA",(40,35),(0,0,0,190))
    draw=ImageDraw.Draw(lvl)
    draw.text((5,5),f"{char.level}",font=f20,fill=(255,255,255,255))
    bg=bg.copy()
    char_icon = await asset_manager.get_asset_from_url(char.avatar_url, size=(133,133))
    if char_icon:
        bg.alpha_composite(char_icon, (0,0))
    ele,pote=await asyncio.gather(
        asset_manager.get_asset(element_map[char.property.value], size=(30,30)),
        asset_manager.get_asset(f"common_pote_{char.potential_level}", size=(45,45))
    )
    if ele:
        bg.alpha_composite(ele, (3,3))
    if pote:
        bg.alpha_composite(pote, (88,88))
    bg.alpha_composite(lvl, (0,90))
        
    return bg

async def render_team(
    chars: List[IndieHardCharacter]
) -> Image.Image:
    W=133*len(chars)+10*(len(chars)-1)
    team_bg = Image.new("RGBA", (W,133), (0,0,0,0))
    t=[]
    for char in chars:
        t.append(render_char(char))
    char_imgs=await asyncio.gather(*t)
    for i,img in enumerate(char_imgs):
        team_bg.alpha_composite(img,(i*(133+10),0))
    return team_bg

async def render_dungeon(
    dungeons: DungeonGroup
) -> Image.Image:
    W=991
    H=375
    dungeon_bg = Image.new("RGBA", (W,H), (42,42,42,255))
    draw = ImageDraw.Draw(dungeon_bg)
    normal_team = await render_team(dungeons.normal_dungeon.best_record.chars) if dungeons.normal_dungeon.best_record else None
    hard_team = await render_team(dungeons.hard_dungeon.best_record.chars) if dungeons.hard_dungeon.best_record else None
    t=[]
    
    n_name=dungeons.normal_dungeon.name
    h_name=dungeons.hard_dungeon.name
    
    n_time=ts_to_day(int(dungeons.normal_dungeon.best_record.ts)) if dungeons.normal_dungeon.best_record else "N/A"
    h_time=ts_to_day(int(dungeons.hard_dungeon.best_record.ts)) if dungeons.hard_dungeon.best_record else "N/A"
    
    n_clear=f"Cleared in {sec_to_min(int(dungeons.normal_dungeon.best_record.pass_ts))}" if dungeons.normal_dungeon.best_record else "Not Cleared"
    h_clear=f"Cleared in {sec_to_min(int(dungeons.hard_dungeon.best_record.pass_ts))}" if dungeons.hard_dungeon.best_record else "Not Cleared"
    
    if normal_team:
        t.append(asyncio.to_thread(dungeon_bg.alpha_composite, normal_team, (15, 47)))
    if hard_team:
        t.append(asyncio.to_thread(dungeon_bg.alpha_composite, hard_team, (15,230)))
        
    t.append(asyncio.to_thread(draw.text, (15, 0), n_name, font=f32, fill=(255, 255, 255, 255)))
    t.append(asyncio.to_thread(draw.text, (15, 187), h_name, font=f32, fill=(255, 255, 255, 255)))
    
    t.append(asyncio.to_thread(draw.text, (625, 120), n_time, font=f20, fill=(255, 255, 255, 255)))
    t.append(asyncio.to_thread(draw.text, (625, 317), h_time, font=f20, fill=(255, 255, 255, 255)))
    
    t.append(asyncio.to_thread(draw.text, (637, 50), n_clear, font=f32, fill=(255, 255, 255, 255)))
    t.append(asyncio.to_thread(draw.text, (637, 248), h_clear, font=f32, fill=(255, 255, 255, 255)))
    
    await asyncio.gather(*t)
    
    return dungeon_bg

async def build_domain_showcase(
    domain: IndieHardGroup
) -> Image.Image:
    W=1080
    H=40 + 332 + 10 + 375*len(domain.dungeon_groups) + 10*(len(domain.dungeon_groups)-1)
    main_bg = Image.new("RGBA", (W,H), (30,30,30,255))
    top=await domain_card(domain)
    main_bg.alpha_composite(top,(44,40))
    t=[]
    for i,dungeon in enumerate(domain.dungeon_groups):
        t.append(render_dungeon(dungeon))
    dungeon_imgs=await asyncio.gather(*t)
    t.clear()
    for i,img in enumerate(dungeon_imgs):
        t.append(asyncio.to_thread(main_bg.alpha_composite, img, (44,40+332+10+i*(375+10))))
    await asyncio.gather(*t)

    return main_bg