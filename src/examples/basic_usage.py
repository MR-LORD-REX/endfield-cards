from ef_cards import EFCard
from endfield import Endfield

import asyncio
uid=4225399080
async def main():
    try:
        async with EFCard(debug=True) as ef_card:
            profile_card = await ef_card.get_profile_card(uid)
            profile_card.card.show()
            print(f"Characters in profile: {[char.name for char in profile_card.characters]}")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())