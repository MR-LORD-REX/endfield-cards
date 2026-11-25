# endfield-cards

Async Endfield image cards powered by [skport-py](https://mr-lord-rex.github.io/skport-py/).
Use `EF_Cards` to fetch data, choose a numeric template, and receive the card and its source model. Requires Python 3.11+.

```console
pip install endfield-cards
```

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


asyncio.run(main())
```

[Documentation](https://mr-lord-rex.github.io/endfield-cards/) · [Card gallery](https://mr-lord-rex.github.io/endfield-cards/#/gallery) · [Examples](examples/)

For [SKPORT IDs and profile privacy](https://mr-lord-rex.github.io/skport-py/#/guides/skport-id-and-privacy)
and [account tokens](https://mr-lord-rex.github.io/skport-py/#/getting-started/account-tokens), follow the skport-py documentation.
Pulls and Wiki cards currently raise `CardNotImplementedError`.

UI references: [akef-cards](https://github.com/ShresthVaibhav/akef-cards).
All game assets belong to **Hypergryph**. This unofficial library is not affiliated with or endorsed by Hypergryph, SKPORT, or any other organization.
Code is licensed under [GPL-3.0-only](LICENSE.txt).
