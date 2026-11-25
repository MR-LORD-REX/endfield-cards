# EF_Cards reference

`EF_Cards` is the public async client. Create it once with an SDK or API, then call a card method with the target and template number.

```python
from endfield_cards import EF_Cards

async with EF_Cards(skport=sdk, config=config) as cards:
    result = await cards.profile_card(skport_id, template=1)
```

## Constructor

```python
cards = EF_Cards(skport=sdk, config=config)
```

Supply exactly one of `skport` (`SkportClient`) or `api` (`SkportAPI`). `config` is a [CardsConfig](../guides/configuration.md). Advanced callers can share an `AssetStore` or aiohttp session; `session` and `url_policy` cannot be supplied together with `asset_store`.

Injected resources are borrowed. `await cards.aclose()` closes rendering resources created by the cards client and cancels its active requests. `close` is an alias for `aclose`. Prefer `async with` to close resources automatically.

## Common arguments

- `template`: a numeric layout ID, default `1`. Valid choices depend on the [card type](templates.md).
- `skport_id`: the target's public SKPORT profile ID, as a string or integer.
- `role_id` and `server_id`: optional public account selectors passed through to skport-py.
- `token` and `role`: owner-account selectors supported by Profile, Character, and Live. Supply an owner token instead of a public ID. All Characters requires its owner token as the first argument.
- `details`: optional supplementary record pages for methods that expose it; defaults to `False`.

See skport-py's [SKPORT ID/privacy](https://mr-lord-rex.github.io/skport-py/#/guides/skport-id-and-privacy), [tokens](https://mr-lord-rex.github.io/skport-py/#/getting-started/account-tokens), and [owner accounts](https://mr-lord-rex.github.io/skport-py/#/guides/owner-accounts) documentation for account setup.

Every available method returns [RenderedCard](../guides/card-results.md). `model` is the source SDK data and `info` is described below.

## profile_card

```python
await cards.profile_card(skport_id, template=1, details=False)
await cards.profile_card(token=owner_token, role=role, template=2)
```

Creates a [profile showcase](../cards/profile.md). Templates: `1`, `2`, `3`. Returns `PlayerCard` with `CharacterListInfo` selectors. Also accepts public `role_id` and `server_id`.

## character_card

```python
await cards.character_card(
    skport_id, template=1, char_id=None, name=None, index=None,
    full=True, showcase_only=False, art=None, details=False,
)
```

Creates one [operator card](../cards/character.md). Templates: `1`, `2`, `3`, `4`. Supply one of `char_id`, `name`, or `index`; omission selects index 0. `full` requests full build data. `showcase_only` is a public selector. `art` accepts [custom artwork](../guides/artwork.md). Returns `CharacterBuild`; `info` is `None`. Also accepts public role selectors or owner `token`/`role`.

## all_characters_card

```python
await cards.all_characters_card(
    owner_token, template=1, role=None, full=True,
    character_ids=None, details=False,
)
```

Creates the authenticated owner's [collection board](../cards/roster.md). Templates: `1`, `2`. `character_ids` is an optional sequence of selected IDs. Returns `list[CharacterBuild]` with owner-scoped `CharacterListInfo`.

## live_card

```python
await cards.live_card(skport_id, template=1, details=False)
await cards.live_card(token=owner_token, role=role, template=2)
```

Creates the [resource/activity dashboard](../cards/live.md). Templates: `1`, `2`. Returns `LiveStatus` with `LiveInfo` and UTC deadlines. Also accepts public `role_id` and `server_id`.

## factory_card

```python
await cards.factory_card(skport_id, template=1)
```

Creates [factory and Dijiang](../cards/factory.md) status. Templates: `1`, `2`. Returns `FactoryState`; `info` is `None`. Also accepts public `role_id` and `server_id`.

## exploration_card

```python
await cards.exploration_card(skport_id, template=1)
```

Creates [exploration progress](../cards/exploration.md) for all supplied regions and areas. Templates: `1`, `2`. Returns `FactoryState`; `info` is `None`. Also accepts public `role_id` and `server_id`.

## monument_card

```python
await cards.monument_card(
    skport_id, template=1, event_id=None, details=False,
)
```

Creates a [Monument overview](../cards/monument.md). Templates: `1`, `2`. `event_id` optionally selects one supplied event. Returns `MonumentState` with `MonumentInfo`. Also accepts public `role_id` and `server_id`.

## monument_detailed_card

```python
await cards.monument_detailed_card(skport_id, template=1, event_id=None)
```

Creates a detailed Monument stage board. Templates: `1`, `2`. Omit `event_id` to select the active/latest supplied event. Returns `MonumentState` with selected-event `MonumentInfo`. Also accepts public `role_id` and `server_id`.

## contingency_contract_card

```python
await cards.contingency_contract_card(
    skport_id, template=1, contract_id=None, details=False,
)
```

Creates a [Contingency Contract overview](../cards/contingency-contract.md). Templates: `1`, `2`. `contract_id` selects one supplied contract; omission selects the current/first contract. Returns `ContractState` with `ContractInfo`. Also accepts public `role_id` and `server_id`.

## contingency_contract_detailed_card

```python
await cards.contingency_contract_detailed_card(
    skport_id, template=1, contract_id=None,
)
```

Creates the selected contract's battle/indicator board. Templates: `1`, `2`. Returns `ContractState` with selected-contract `ContractInfo`. Also accepts public `role_id` and `server_id`.

## compare_card

```python
await cards.compare_card(
    first_skport_id, second_skport_id, template=1,
    char_id=None, name=None, index=None, second_char_id=None,
    art=None, second_art=None, details=False,
)
```

Creates a [comparison](../cards/compare.md) for one operator across two players. Templates: `1`, `2`. Select the first operator by ID, name, or index. Without `second_char_id`, the second operator is selected by the first operator's localized name. Returns `(CharacterBuild, CharacterBuild)`; `info` is `None`.

Public role selectors are `role_id`/`server_id` for the first profile and `second_role_id`/`second_server_id` for the second.

## pulls_card and wiki_card

```python
await cards.pulls_card()
await cards.wiki_card()
```

Both are reserved methods that raise [CardNotImplementedError](../guides/errors.md) immediately. Optional source-data and template arguments are reserved for future implementations.

## Properties and caching

`cards.templates` returns numeric template choices keyed by method name without `_card`. `cards.cache_stats` reports render/image cache diagnostics. Call `await cards.clear_cache(renders=True, images=True, disk=True)` to clear card caches.

The older `Cards` and `EFCard` imports remain compatibility aliases for `EF_Cards`.
