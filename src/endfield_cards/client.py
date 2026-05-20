import logging
from PIL import Image, ImageDraw
import asyncio
import aiohttp

from .utils.assets.core import asset_manager
from endfield import Endfield
from endfield.models.character import CharacterData
from .character.template1.character import build_main_frame
from .character.template1.weapon import build_weapon_panel
from .character.template1.relics import build_relic_panel
from .character.template1.skills import build_skill_panel
from .character.template1.stats import build_stats_panel
from .profile.template1.profile1 import build_profile1
from .models.profile1 import ProfileCard_1 , Character

logger = logging.getLogger(__name__)

logging.getLogger('PIL').setLevel(logging.WARNING)


class EFCard:
    def __init__(self,ef:Endfield |None=None,cache_assets:bool=False , debug:bool=False):
        self.ef = ef if ef is not None else Endfield(debug=debug)
        self.asset_manager = asset_manager
        self.logger = logger
        
    async def __aenter__(self):
        if self.ef is None:
            self.ef = Endfield(debug=self.logger.isEnabledFor(logging.DEBUG))
        await self.ef.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
    
    async def close(self):
        try:
            await self.asset_manager.close()
        except Exception as e:
            self.logger.debug(f"Error closing asset manager: {e}")
        
        try:
            if self.ef:
                await self.ef.close()
        except Exception as e:
            self.logger.debug(f"Error closing Endfield client: {e}")
        
    def composite_image(self,base:Image.Image,overlay:tuple[Image.Image,tuple[int,int]]):
        base.alpha_composite(overlay[0], overlay[1])
        
    def __exit__(self, exc_type, exc, tb):
        pass
        
    async def _build_character1(
        self,
        char_data: CharacterData,
        user_img: Image.Image | None = None
        ) -> Image.Image:
        try:
            main_frame = await build_main_frame(char_data,user_img)
            result = await asyncio.gather(
                build_weapon_panel(char_data.weapon),
                build_relic_panel(char_data.equips),
                build_stats_panel(char_data.detailed_stats),
                build_skill_panel(char_data.skills,char_data.detailed_stats),
            )
            t=[]
            loc=[(1140,50),(1328,366),(19,0),(19,674)]
            for panel,l in zip(result,loc):
                t.append(asyncio.to_thread(self.composite_image,main_frame,(panel,l)))
            await asyncio.gather(*t)
            return main_frame
        except Exception as e:
            logger.error(f"Error building character card: {e}")
            return Image.new("RGBA", (1920,800), (0, 0, 0, 0))
        
    async def get_character_card(self,uid:int,char_index:int=0,user_img:Image.Image|None=None,template:int=1) -> Image.Image:
        try:
            if template == 1:
                char_data = await self.ef.get_character_showcase(uid, char_index)
                return await self._build_character1(char_data,user_img)
            else:
                logger.warning(f"Template {template} not implemented, defaulting to template 1")
                return await self.get_character_card(uid, char_index, user_img, template=1)
        except Exception as e:
            logger.error(f"Error building character card for uid={uid}, char_index={char_index}: {e}")
            return Image.new("RGBA", (1920, 800), (0, 0, 0, 0))
                
    async def get_all_characters_card(self,uid:int,user_imgs: list[Image.Image]|None=None,template:int=1) -> list[Image.Image]:
        try:
            if template == 1:
                showcase = await self.ef.get_showcase(uid)
                characters = showcase.characters
                tasks = [
                    self._build_character1(
                        char,
                        user_imgs[i] if user_imgs and i < len(user_imgs) else None
                    )
                    for i, char in enumerate(characters)
                ]
                return await asyncio.gather(*tasks)
            else:
                logger.warning(f"Template {template} not implemented, defaulting to template 1")
                return await self.get_all_characters_card(uid, user_imgs, template=1)
        except Exception as e:
            logger.error(f"Error building all characters card for uid={uid}: {e}")
            return []
                
    async def get_profile_card(self,uid:int,template:int=1) -> ProfileCard_1:
        try:
            profile_data = await self.ef.get_profile(uid)
            if template == 1:
                card=await build_profile1(profile_data)
                chars=[]
                for i,char in enumerate(profile_data.characters):
                    chars.append(Character(
                        name=char.name,
                        slot_index=i,  
                    ))
                return ProfileCard_1(
                    card=card,
                    characters=chars,
                    char_count=len(chars)
                )
            else:
                logger.warning(f"Template {template} not implemented, defaulting to template 1")
                return await self.get_profile_card(uid, template=1)
        except Exception as e:
            logger.error(f"Error building profile card for uid={uid}: {e}")
            return ProfileCard_1(
                card=Image.new("RGBA", (1080, 1467), (0, 0, 0, 0)),
                characters=[],
                char_count=0
            )