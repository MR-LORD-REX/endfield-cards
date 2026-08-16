from src.endfield_cards import EFCard
from src.endfield_cards.logging_config import setup_logging
from src.endfield_cards.errors import CardBuildError 
import logging
import asyncio

uid = 6697262238
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
            await efc.ef.update_assets()
            await efc.update_builds()

            card=await efc.get_character_card(uid,2)
            card.show()
            
            try:
                cards = await efc.get_allc_card(token)
                cards.card.show()
                cards.card.save("test/allc_card.png")
                
                chars=[]
                for c in cards.allChars.characters:
                    chars.append(efc.get_game_character(token,c.char_id))
                cards=await asyncio.gather(*chars)
                for c in cards[:5]:
                    c.show()
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

            try:
                stats_card = await efc.get_live_stats_card(uid, token)
                if stats_card:
                    logger.info("Live stats card built successfully")
                    stats_card.img.show()
                else:
                    logger.warning("Live stats card is None")
            except Exception as e:
                logger.error(f"Failed to build live stats card: {e}")
            
            try:
                monument_card = await efc.get_monument_showcase_card(token)
                if monument_card:
                    logger.info("Monument showcase card built successfully")
                    monument_card.card.show()
                    monument_card.card.save("test/monument_showcase_card.png")
                    for domain in monument_card.domains:
                        logger.info(f"Domain: {domain.name}, Slot: {domain.slot}")
                else:
                    logger.warning("Monument showcase card is None")
            except CardBuildError as e:
                logger.error(f"Failed to build monument showcase card: {e}")
                
            try:
                card=await efc.get_monument_domain_card(token, 1)  # Replace 1 with the desired domain slot
                if card:
                    logger.info("Domain showcase card built successfully")
                    card.show()
                    card.save("test/domain_showcase_card.png")
                else:
                    logger.warning("Domain showcase card is None")
            except CardBuildError as e:
                logger.error(f"Failed to build domain showcase card: {e}")
            
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}", exc_info=True)
        
if __name__ == "__main__":
    asyncio.run(main())
