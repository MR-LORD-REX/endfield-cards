from endfield_cards import EFCard
from endfield import Endfield

import asyncio
uid=4225399080
async def main():
    try:
        async with EFCard(debug=True) as ef:
            card=await ef.get_character_card(uid, char_index=1)
            card.show()
            card=await ef.get_profile_card(uid)
            card.card.show()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    