import logging
from PIL import Image, ImageDraw
import asyncio
import aiohttp
import traceback
from io import BytesIO
from typing import Tuple

from endfield import Endfield
from endfield.models.basic.character import CharacterData
from endfield.models.auth.game_stats import GameStats

from .utils.assets.core import asset_manager
from .models.profile1 import ProfileCard_1 , Character
from .models.live_stats import LiveStats

from .builds.guides import get_character_build , get_all_character_list , fetch_build_data
from .builds.map import builds_map

from .character.template1.char1 import _build_character1
from .profile.template1.profile1 import build_profile1
from .RT_data.stats import render_live_stats , render_factory

from .errors import CardBuildError, ComponentBuildError, DataFetchError, ErrorSeverity


logger = logging.getLogger(__name__)

logging.getLogger('PIL').setLevel(logging.WARNING)


class EFCard:
    """
    paramters: 
    """
    
    def __init__(self,ef:Endfield |None=None,cache_assets:bool=False , debug:bool=False,session:aiohttp.ClientSession|None=None):
        self.ef = ef if ef is not None else Endfield(debug=debug)
        self.asset_manager = asset_manager
        self.logger = logger
        self.asset_manager.cache.enabled = cache_assets
        self.asset_manager.set_debug(debug)
        if session:
            self.ef._session = session
            self.asset_manager.session = session

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
        """
        Build a character card for the given UID and character index.
        
        Args:
            uid: User ID
            char_index: Character index in showcase
            user_img: Optional user avatar image
            template: Card template version (default: 1)
            
        Returns:
            Image.Image: Character card image
            
        Raises:
            CardBuildError: If critical error occurs during card building
        """
        try:
            if template == 1:
                try:
                    char_data = await self.ef.get_character_showcase(uid, char_index)
                except Exception as e:
                    error = DataFetchError(
                        message=f"Failed to fetch character showcase data",
                        data_source="Endfield API",
                        uid=uid,
                        original_error=e,
                        context={"char_index": char_index}
                    )
                    error.log()
                    raise CardBuildError(
                        message=f"Cannot build character card without character data",
                        card_type="character",
                        uid=uid,
                        original_error=e,
                        context={"char_index": char_index}
                    )
                
                try:
                    return await _build_character1(char_data=char_data,user_img=user_img)
                except Exception as e:
                    error = CardBuildError(
                        message=f"Failed to build character card: {e}",
                        card_type="character",
                        uid=uid,
                        original_error=e,
                        context={"char_index": char_index}
                    )
                    error.log()
                    raise
            else:
                logger.warning(f"Template {template} not implemented, defaulting to template 1")
                return await self.get_character_card(uid, char_index, user_img, template=1)
        except CardBuildError:
            # Re-raise card build errors
            raise
        except Exception as e:
            # Catch any unexpected errors
            error = CardBuildError(
                message=f"Unexpected error building character card: {e}",
                card_type="character",
                uid=uid,
                original_error=e,
                context={"char_index": char_index}
            )
            error.log()
            raise
                
    async def get_all_characters_card(self,uid:int,user_imgs: list[Image.Image]|None=None,template:int=1) -> list[Image.Image]:
        """
        Build character cards for all characters in showcase.
        Failed individual characters are logged but don't stop the whole build.
        
        Args:
            uid: User ID
            user_imgs: Optional list of user avatar images
            template: Card template version (default: 1)
            
        Returns:
            list[Image.Image]: List of character card images
            
        Raises:
            CardBuildError: If critical error prevents fetching showcase data
        """
        try:
            if template == 1:
                try:
                    showcase = await self.ef.get_showcase(uid)
                    characters = showcase.characters
                except Exception as e:
                    error = DataFetchError(
                        message=f"Failed to fetch showcase data",
                        data_source="Endfield API",
                        uid=uid,
                        original_error=e
                    )
                    error.log()
                    raise CardBuildError(
                        message=f"Cannot build character cards without showcase data",
                        card_type="showcase",
                        uid=uid,
                        original_error=e
                    )
                
                tasks = [
                    self._build_character1_safe(
                        char,
                        user_imgs[i] if user_imgs and i < len(user_imgs) else None,
                        i
                    )
                    for i, char in enumerate(characters)
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Filter out errors and collect successful results
                cards = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        error = ComponentBuildError(
                            message=f"Failed to build character {i}: {result}",
                            component_name=f"Character[{i}]",
                            original_error=result
                        )
                        error.log()
                        # Continue without this card
                    else:
                        cards.append(result)
                
                if not cards:
                    raise CardBuildError(
                        message=f"All character cards failed to build",
                        card_type="showcase",
                        uid=uid,
                        context={"total_characters": len(characters), "successful": 0}
                    )
                
                return cards
            else:
                logger.warning(f"Template {template} not implemented, defaulting to template 1")
                return await self.get_all_characters_card(uid, user_imgs, template=1)
        except CardBuildError:
            raise
        except Exception as e:
            error = CardBuildError(
                message=f"Unexpected error building all characters cards: {e}",
                card_type="showcase",
                uid=uid,
                original_error=e
            )
            error.log()
            raise
                
    async def get_profile_card(self,uid:int,template:int=1) -> ProfileCard_1:
        """
        Build a profile card for the given UID.
        
        Args:
            uid: User ID
            template: Card template version (default: 1)
            
        Returns:
            ProfileCard_1: Profile card with character data
            
        Raises:
            CardBuildError: If critical error prevents fetching profile data
        """
        try:
            try:
                profile_data = await self.ef.get_profile(uid)
            except Exception as e:
                error = DataFetchError(
                    message=f"Failed to fetch profile data",
                    data_source="Endfield API",
                    uid=uid,
                    original_error=e
                )
                error.log()
                raise CardBuildError(
                    message=f"Cannot build profile card without profile data",
                    card_type="profile",
                    uid=uid,
                    original_error=e
                )
            
            if template == 1:
                try:
                    card = await build_profile1(profile_data)
                except Exception as e:
                    error = ComponentBuildError(
                        message=f"Failed to render profile card layout",
                        component_name="ProfileRenderer[template1]",
                        original_error=e
                    )
                    error.log()
                    raise CardBuildError(
                        message=f"Failed to render profile card: {e}",
                        card_type="profile",
                        uid=uid,
                        original_error=e
                    )
                
                chars = []
                for i, char in enumerate(profile_data.characters):
                    try:
                        chars.append(Character(
                            name=char.name,
                            slot_index=i,  
                        ))
                    except Exception as e:
                        error = ComponentBuildError(
                            message=f"Failed to process character {i} in profile",
                            component_name=f"ProfileCharacter[{i}]",
                            original_error=e
                        )
                        error.log()
                        
                return ProfileCard_1(
                    card=card,
                    characters=chars,
                    char_count=len(chars)
                )
            else:
                logger.warning(f"Template {template} not implemented, defaulting to template 1")
                return await self.get_profile_card(uid, template=1)
        except CardBuildError:
            raise
        except Exception as e:
            error = CardBuildError(
                message=f"Unexpected error building profile card: {e}",
                card_type="profile",
                uid=uid,
                original_error=e
            )
            error.log()
            raise
            
    async def _build_character1_safe(self, char_data, user_img, index: int) -> Image.Image:
        """
        Args:
            char_data: Character data
            user_img: Optional user image
            index: Character index for logging
            
        Returns:
            Image.Image: Character card image
            
        Raises:
            Exception: On component build failure (caught by caller)
        """
        try:
            return await _build_character1(char_data=char_data, user_img=user_img)
        except Exception as e:
            error = ComponentBuildError(
                message=f"Failed to build character card template",
                component_name=f"CharacterBuilder[{index}]",
                original_error=e
            )
            error.log()
            raise
            
    async def get_live_stats_card(self,uid:int,token:str,server:int=3) -> LiveStats|None:
        """
        Build a live game stats card.
        
        Args:
            uid: User ID
            token: Game token for authentication
            server: Server ID (default: 3, asia = 3 , europe/america = 2)
            
        Returns:
            LiveStats: Live stats card data or None if failed
        """
        try:
            try:
                stats = await self.ef.get_game_stats(token, server)
            except Exception as e:
                error = DataFetchError(
                    message=f"Failed to fetch game stats",
                    data_source="GameStats API",
                    uid=uid,
                    original_error=e,
                    context={"server": server}
                )
                error.log()
                return None
            
            if stats:
                try:
                    return await render_live_stats(stats=stats)
                except Exception as e:
                    error = ComponentBuildError(
                        message=f"Failed to render live stats card",
                        component_name="LiveStatsRenderer",
                        original_error=e
                    )
                    error.log()
                    return None
            else:
                logger.warning(f"No game stats returned for uid={uid}, server={server}")
                return None
        except Exception as e:
            logger.error(f"Unexpected error building live stats card for uid={uid}: {e}")
            return None 
        
    async def get_factory_stats_card(self,uid:int,token:str,server:int=3) -> Image.Image|None:
        """
        Build a factory stats card.
        
        Args:
            uid: User ID
            token: Game token for authentication
            server: Server ID (default: 3, asia = 3 , europe/america = 2)
            
        Returns:
            Image.Image: Factory stats card image or None if failed
        """
        try:
            try:
                stats = await self.ef.get_game_stats(token, server)
            except Exception as e:
                error = DataFetchError(
                    message=f"Failed to fetch game stats for factory",
                    data_source="GameStats API",
                    uid=uid,
                    original_error=e,
                    context={"server": server}
                )
                error.log()
                return None
            
            if stats:
                try:
                    return await render_factory(stats=stats)
                except Exception as e:
                    error = ComponentBuildError(
                        message=f"Failed to render factory stats card",
                        component_name="FactoryStatsRenderer",
                        original_error=e
                    )
                    error.log()
                    return None
            else:
                logger.warning(f"No game stats returned for uid={uid}, server={server}")
                return None
        except Exception as e:
            logger.error(f"Unexpected error building factory stats card for uid={uid}: {e}")
            return None
        
    async def update_builds(self):
        """
        Fetch the latest build data and update the local mapping.
        
        Returns:
            None
        """
        try:
            await fetch_build_data()
            logger.info("Build data updated successfully")
        except Exception as e:
            logger.error(f"Failed to update build data: {e}")
            
    async def get_character_build(self,character:builds_map) -> Tuple[Image.Image, str]:
        """
        Get the character build image for the specified character.
        
        Args:
            character: Character name from builds_map
        
        Returns:
            Image.Image: Character build image
        """
        try:
            build_url = get_character_build(character)
            if not build_url:
                raise ValueError(f"No build URL found for character '{character}'")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(build_url) as response:
                    if response.status == 200:
                        img_data = await response.read()
                        img=Image.open(BytesIO(img_data)).convert("RGBA")
                        return img , build_url
                    else:
                        raise Exception(f"Failed to fetch build image: {response.status}")
        except Exception as e:
            logger.error(f"Error fetching build for character '{character}': {e}")
            return Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)) , ""
        
    async def available_builds(self) -> dict[str, dict[str, str]]:
        """
        Get the build data for all characters.
        
        Returns:
            dict[str, dict[str, str]]: Mapping of character names to their icon urls
        """
        try:
            return get_all_character_list()
        except Exception as e:
            logger.error(f"Error fetching all character builds: {e}")
            return {}
        
        