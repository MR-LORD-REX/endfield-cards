from src.ef_cards import EFCard
from endfield import Endfield

import asyncio
uid=4225399080
async def main():
    try:
        async with EFCard() as card:
            cards=await card.get_all_characters_card(uid)
            for c in cards:
                c.show()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    