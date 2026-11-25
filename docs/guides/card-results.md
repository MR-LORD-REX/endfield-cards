# Card results

Every card method returns `RenderedCard`, which contains images, a copy of the fetched SDK model, and method-specific information.

## Image access

For exactly one image, use `result.card`:

```python
result = await cards.profile_card(skport_id)
result.card.save("output/profile.png")
```

`result.cards` is a tuple containing every page. Use it when a collection can span multiple images or when requesting `details=True`:

```python
for page in result.cards:
    page.save(f"output/profile/{page.page}.png")
```

`result.card` raises `ValueError` if the result has zero or multiple pages. Extra pages are never silently discarded.

Each `CardResult` provides:

- `data`: encoded image bytes.
- `format`, `width`, and `height`: image properties.
- `template`: the numeric template used by the public method.
- `page` and `pages`: one-based page position and total page count.
- `issues`: nonfatal rendering or image-source issues.
- `save(path)`: write the encoded image atomically.
- `to_pillow()`: decode a fresh Pillow image for further processing.

## Source data

`result.model` returns a new deep copy of the normalized skport-py model. Modifying it does not change the images, cached results, or another caller's data.

```python
operator = await cards.character_card(skport_id, index=0)
build = operator.model
print(build.name, build.level)
if build.stats is not None:
    print(build.stats.attack)
```

Profile returns `PlayerCard`; Character returns `CharacterBuild`; Compare returns a pair of builds; All Characters returns a list of builds. Live returns `LiveStatus`, Factory and Exploration return `FactoryState`, Monument returns `MonumentState`, and Contingency Contract returns `ContractState`. See skport-py's [output model reference](https://mr-lord-rex.github.io/skport-py/#/reference/output-models) for their fields.

## Selectors and deadlines

`result.info` contains immutable convenience information where supported:

- Profile and All Characters: owner identity, source scope, and character IDs/indexes.
- Live: resource meters, activities, server time, and supplied deadlines.
- Monument: event IDs and stage selectors.
- Contingency Contract: contract IDs, stages, missions, and battle selectors.
- Character, Compare, Factory, and Exploration: `None`.

```python
profile = await cards.profile_card(skport_id)
for selection in profile.info.characters:
    print(selection.name, selection.id)

live = await cards.live_card(skport_id)
print(live.info.fully_replenished_at)
```

Missing source values remain missing. Cards do not invent absent stats, progress, or historical loadouts.
