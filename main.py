from src.endfield_cards import EFCard
from src.endfield_cards.logging_config import setup_logging
from src.endfield_cards.errors import CardBuildError 
import logging
import asyncio

uid = 4572346170
token = ""

logger = logging.getLogger(__name__)


async def main():
    setup_logging(
        level=logging.INFO,
        log_file=None,
        debug=True
    )
    try:
        async with EFCard() as efc:
            # await efc.ef.update_assets()
            # await efc.update_builds()
            
            try:
                card = await efc.get_character_card(uid, char_index=0)
                card.show()
            except CardBuildError as e:
                logger.error(f"Failed to build character card: {e}")
            try:
                card = await efc.get_profile_card(uid)
                card.card.show()
            except CardBuildError as e:
                logger.error(f"Failed to build profile card: {e}")
            
            char_card=await efc.get_character_build('endministrator')
            char_card[0].show()
            
            all=await efc.available_builds()
            print(all)

            # try:
            #     stats_card = await efc.get_live_stats_card(uid, token)
            #     if stats_card:
            #         logger.info("Live stats card built successfully")
            #         stats_card.img.show()
            #     else:
            #         logger.warning("Live stats card is None")
            # except Exception as e:
            #     logger.error(f"Failed to build live stats card: {e}")
            
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}", exc_info=True)
        
if __name__ == "__main__":
    asyncio.run(main())
