import logging
from PIL import Image, ImageDraw
import asyncio
import aiohttp
import traceback

from .utils.assets.core import asset_manager
from endfield import Endfield
from endfield.models.character import CharacterData
from .character.template1.char1 import _build_character1
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
        
        
    async def get_character_card(self,uid:int,char_index:int=0,user_img:Image.Image|None=None,template:int=1) -> Image.Image:
        try:
            if template == 1:
                char_data = await self.ef.get_character_showcase(uid, char_index)
                return await _build_character1(char_data=char_data,user_img=user_img)
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
            traceback.print_exc()
            return ProfileCard_1(
                card=Image.new("RGBA", (1080, 1467), (0, 0, 0, 0)),
                characters=[],
                char_count=0
            )