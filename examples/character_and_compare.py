"""Create operator cards. Credential setup: https://mr-lord-rex.github.io/skport-py/"""

import asyncio
import os
from pathlib import Path

from skport import SkportClient

from endfield_cards import EF_Cards


async def main() -> None:
    """Show one operator and compare that operator between two public profiles."""
    token = os.environ["SKPORT_TOKEN"]
    first_id = os.environ["SKPORT_ID"]
    second_id = os.environ["SKPORT_COMPARE_ID"]
    name = os.environ["CHARACTER_NAME"]
    output = Path("output")

    async with SkportClient(tokens=[token]) as sdk:
        await sdk.warm()
        async with EF_Cards(skport=sdk) as cards:
            character = await cards.character_card(first_id, name=name, template=3)
            character.card.save(output / "character/3.png")
            print(character.model.name)

            comparison = await cards.compare_card(first_id, second_id, name=name, template=2)
            comparison.card.save(output / "compare/2.png")


if __name__ == "__main__":
    asyncio.run(main())
