from src.endfield_cards import Cards
from skport import SkportAPI , SkportClient

import asyncio

async def main():
    api = SkportAPI([""])
    async with SkportClient(api) as sk :
        async with Cards(skport=sk) as renderer:
            card = await renderer.