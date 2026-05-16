from typing import Literal , Optional , Any
import logging

from PIL import Image

from .assets.core import asset_manager

logger=logging.getLogger(__name__)

async def get_relic_level_image(level: int) -> Optional[Image.Image]:
    base_img= await asset_manager.get_asset('c1_enc_lvl')
    if level == 2:
        return base_img
    else:
        size=base_img.size
        size=((size[0]*(level-1)+(4*(level-2)),size[1]))
        new_img = Image.new("RGBA", size)
        for i in range(level):
            new_img.alpha_composite(base_img, (i * (base_img.size[0] + 4),0))
        return new_img
    
async def build_stars(star_count: int,size: tuple|None=(21, 21)) -> Image.Image:
    star_img = await asset_manager.get_asset("common_star", size=size)
    star_img = star_img.copy()
    stars_frame = Image.new("RGBA", (size[0]*star_count,size[1]), (0, 0, 0, 0))
    for i in range(star_count):
        stars_frame.alpha_composite(star_img, (i * 21, 0))
    return stars_frame

async def get_pote(lvl: int,size:tuple=(24,24))-> Optional[Image.Image]:
    if lvl < 0 or lvl >5 :
        logger.warning(f"get_pote: invalid level {lvl}, must be between 0 and 5")
        return None
    pote_img = await asset_manager.get_asset(f"common_pote_{lvl}", size=size)
    if pote_img is None:
        logger.warning(f"get_pote: asset not found for level {lvl}")
        return None
    return pote_img