from src.endfield_cards import EFCard
from endfield import Endfield


import asyncio
uid=4546876184
token=""
async def main():
    try:
        async with EFCard(debug=True) as efc:
            card=await efc.get_character_card(uid, char_index=2)
            card.show()
            card=await efc.get_profile_card(uid)
            card.card.show()
            # stats_card=await efc.get_live_stats_card(uid, token)
            # if stats_card:
            #     stats_card.img.show()
            # factory_card=await efc.get_factory_stats_card(uid, token)
            # if factory_card:
            #     factory_card.show()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    