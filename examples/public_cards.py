"""Create public cards. Credential setup: https://mr-lord-rex.github.io/skport-py/"""

import asyncio
import os
from pathlib import Path

from skport import SkportClient

from endfield_cards import CardsConfig, EF_Cards, OutputConfig


async def main() -> None:
    """Save a profile, factory status and exploration card as PNGs."""
    token = os.environ["SKPORT_TOKEN"]
    skport_id = os.environ["SKPORT_ID"]
    config = CardsConfig(locale="en", output=OutputConfig(format="PNG"))
    output = Path("output")

    async with SkportClient(tokens=[token]) as sdk:
        await sdk.warm()
        async with EF_Cards(skport=sdk, config=config) as cards:
            profile = await cards.profile_card(skport_id, template=1)
            profile.card.save(output / "profile/1.png")

            factory = await cards.factory_card(skport_id, template=1)
            factory.card.save(output / "factory/1.png")

            exploration = await cards.exploration_card(skport_id, template=2)
            exploration.card.save(output / "exploration/2.png")


if __name__ == "__main__":
    asyncio.run(main())
