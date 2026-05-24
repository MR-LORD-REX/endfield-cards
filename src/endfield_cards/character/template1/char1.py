
import logging
import asyncio
from PIL import Image

from endfield.models.character import CharacterData
from .character import build_main_frame
from .weapon import build_weapon_panel
from .relics import build_relic_panel
from .skills import build_skill_panel
from .stats import build_stats_panel

logger = logging.getLogger(__name__)

def composite_image(base:Image.Image,overlay:tuple[Image.Image,tuple[int,int]]):
    base.alpha_composite(overlay[0], overlay[1])


async def _build_character1(
    char_data: CharacterData,
    user_img: Image.Image | None = None
    ) -> Image.Image:
    try:
        main=char_data.main_attribute.attri_id
        sub=char_data.sub_attribute.attri_id
        main_frame = await build_main_frame(char_data,user_img)
        result = await asyncio.gather(
            build_weapon_panel(weapon_data=char_data.weapon,main=main,sub=sub),
            build_relic_panel(char_data.equips),
            build_stats_panel(char_data.detailed_stats),
            build_skill_panel(char_data.skills,char_data.detailed_stats),
        )
        t=[]
        loc=[(1140,50),(1328,366),(19,0),(19,674)]
        for panel,l in zip(result,loc):
            t.append(asyncio.to_thread(composite_image,main_frame,(panel,l)))
        await asyncio.gather(*t)
        return main_frame
    except Exception as e:
        logger.error(f"Error building character card: {e}")
        return Image.new("RGBA", (1920,800), (0, 0, 0, 0))