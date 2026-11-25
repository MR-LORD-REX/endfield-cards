"""Create an owned roster. Owner access: https://mr-lord-rex.github.io/skport-py/#/guides/owner-accounts"""

import asyncio
import os
from pathlib import Path

from skport import SkportClient

from endfield_cards import EF_Cards


async def main() -> None:
    """Render the account explicitly selected by its token, saving every page."""
    token = os.environ["SKPORT_TOKEN"]
    output = Path("output/all_characters")

    async with SkportClient(tokens=[token]) as sdk:
        await sdk.warm()
        async with EF_Cards(skport=sdk) as cards:
            roster = await cards.all_characters_card(token, template=1)
            for page in roster.cards:
                name = "1.png" if len(roster.cards) == 1 else f"1-page-{page.page}.png"
                page.save(output / name)


if __name__ == "__main__":
    asyncio.run(main())
