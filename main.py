from endfield_cards import Cards
from skport import SkportAPI , SkportClient

import asyncio

async def main():
    api = SkportAPI(["wcIb3Km2m6ur7exHo8QOLXHg"])
    async with SkportClient(api) as sk :
        async with Cards(skport=sk) as renderer:
            card = await renderer.monument_detailed_card(2348675939926,template=2)
            card.card.to_pillow().show()

asyncio.run(main())