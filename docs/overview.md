# Endfield cards

Create Endfield cards with one async call. `EF_Cards` fetches normalized data through skport-py, renders your chosen numeric template, and returns the images together with the source model.

```python
result = await cards.profile_card(skport_id, template=1)
result.card.save("output/profile.png")
profile = result.model
```

## Start here

1. [Install the library](getting-started/installation.md).
2. [Create your first card](getting-started/quickstart.md).
3. Choose a [card method](reference/client.md) and [template number](reference/templates.md).

The library provides Profile, Character, Compare, All Characters, Live, Factory, Exploration, Monument, and Contingency Contract cards. Monument and Contingency Contract also have separate detailed cards. Pulls and Wiki cards are not implemented yet.

## Cards and data

Each call returns a `RenderedCard`. Use `result.card` for a single image, `result.cards` for all pages, `result.model` for the fetched SDK model, and `result.info` for supported character selectors or activity deadlines. See [card results](guides/card-results.md).

For numeric data alone, use [skport-py](https://mr-lord-rex.github.io/skport-py/#/reference/endfield). It handles authentication, target discovery, and game calculations. Endfield cards adds the rendering step.

Configure output format, language, and resource limits once when creating `EF_Cards`; pass the target and template to each method. [Configuration](guides/configuration.md) covers these settings.

## Examples and credits

Browse the [card gallery](gallery.md) for every implemented template. The repository also includes [runnable examples](https://github.com/mr-lord-rex/endfield-cards/tree/main/examples). Card guides show their relevant output images.

UI references come from [akef-cards](https://github.com/ShresthVaibhav/akef-cards). All game assets belong to **Hypergryph**. This unofficial library is not affiliated with or endorsed by Hypergryph, SKPORT, or any other organization. See [attribution](attribution.md).
