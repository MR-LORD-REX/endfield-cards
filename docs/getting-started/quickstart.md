# Your first card

Set `SKPORT_TOKEN` to your viewer account token and `SKPORT_ID` to the target profile ID. The skport-py guides explain [tokens](https://mr-lord-rex.github.io/skport-py/#/getting-started/account-tokens) and [SKPORT IDs](https://mr-lord-rex.github.io/skport-py/#/guides/skport-id-and-privacy).

```python
import asyncio
import os

from endfield_cards import EF_Cards
from skport import SkportClient


async def main() -> None:
    async with SkportClient(tokens=[os.environ["SKPORT_TOKEN"]]) as sdk:
        async with EF_Cards(skport=sdk) as cards:
            result = await cards.profile_card(os.environ["SKPORT_ID"], template=1)
            result.card.save("output/profile.png")
            print(result.model.player.name)


if __name__ == "__main__":
    asyncio.run(main())
```

Saving is explicit: fetching a card does not write images or source data to disk. The default image format is PNG, and `.save()` creates parent directories as needed.

## Create a character card

Inside the same open client, use a character ID returned by the profile:

```python
if result.info.characters:
    character_id = result.info.characters[0].id
    operator = await cards.character_card(
        os.environ["SKPORT_ID"], char_id=character_id, template=1
    )
    operator.card.save("output/character.png")
```

You can also select by `name` or zero-based `index`; supply one selector. [Character cards](../cards/character.md) explains selection and artwork.

## Reuse the client

Keep one SDK and one `EF_Cards` instance open for related requests. The context managers close their owned resources. Closing `EF_Cards` leaves the injected SDK open, so your application can continue using it.

See [configuration](../guides/configuration.md), [results and pagination](../guides/card-results.md), and the repository's [example scripts](https://github.com/mr-lord-rex/endfield-cards/tree/main/examples).
