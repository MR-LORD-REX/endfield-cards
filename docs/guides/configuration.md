# Configuration

Use `CardsConfig` when creating `EF_Cards`. Output encoding, labels, display timezone, cache settings, and rendering limits apply to its card methods.

```python
from endfield_cards import CardsConfig, EF_Cards, OutputConfig

config = CardsConfig(
    locale="en",
    display_timezone="Asia/Calcutta",
    output=OutputConfig(format="WEBP", quality=90),
)

async with EF_Cards(skport=sdk, config=config) as cards:
    result = await cards.profile_card(skport_id, template=2)
    result.card.save("output/profile.webp")
```

## SDK or API

Supply exactly one of `skport=` or `api=`. An injected SDK or API remains open when the cards client closes.

```python
from endfield_cards import EF_Cards
from skport import SkportAPI

async with SkportAPI(tokens=[token]) as api:
    async with EF_Cards(api=api) as cards:
        result = await cards.profile_card(skport_id)
```

Authentication, retry policy, canonical game assets, source image preference, and stat calculations belong to skport-py's [client configuration](https://mr-lord-rex.github.io/skport-py/#/guides/languages-and-configuration).

## Image format

`OutputConfig` supports `"PNG"`, `"JPEG"`, and `"WEBP"`. PNG is the default. `quality` accepts 1–100 for lossy formats. Match your filename extension to the configured format: `.save()` writes the encoded bytes and does not convert them based on the filename.

Set `max_bytes` to reject a page that exceeds your application's encoded-image limit:

```python
output = OutputConfig(format="JPEG", quality=85, max_bytes=4_000_000)
```

## Language and time

Supported locales are `"en"`, `"ja"`, `"ko"`, `"zh-Hans"`, and `"zh-Hant"`. Without an explicit `CardsConfig`, the client inherits the SDK's locale. With a config, `locale` controls both SDK fetches and card labels. Name-based character selection uses that language.

`display_timezone` accepts an IANA timezone such as `"UTC"` or `"Asia/Calcutta"`. Live cards and returned Live deadlines use UTC.

## Caching and limits

The defaults provide two render workers, eight admitted jobs, and eight concurrent image downloads. Rendering does not block the event loop.

Image and encoded-render caches are bounded in memory. Disk image caching is optional:

```python
from pathlib import Path
from endfield_cards import CacheConfig, CardsConfig

config = CardsConfig(cache=CacheConfig(directory=Path(".card-cache")))
```

Call `await cards.clear_cache()` to clear cached card resources, or inspect `cards.cache_stats`. Custom artwork renders bypass the encoded-render cache. For artwork controls, see [custom artwork](artwork.md).
