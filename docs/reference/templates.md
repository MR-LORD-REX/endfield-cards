# Template numbers

Select a template using an integer. Each card type has its own stable numbering; a number does not select a different player's character or a game asset.

```python
result = await cards.character_card(skport_id, name="Zhuang Fangyi", template=3)
```

## Available templates

- [Profile](../cards/profile.md): `1`, `2`, `3`.
- [Character](../cards/character.md): `1`, `2`, `3`, `4`.
- [Compare](../cards/compare.md): `1`, `2`.
- [All Characters](../cards/roster.md): `1`, `2`.
- [Live](../cards/live.md): `1`, `2`.
- [Factory](../cards/factory.md): `1`, `2`.
- [Exploration](../cards/exploration.md): `1`, `2`.
- [Monument overview and detailed](../cards/monument.md): `1`, `2` for each method.
- [Contingency Contract overview and detailed](../cards/contingency-contract.md): `1`, `2` for each method.

Pulls and Wiki are [unavailable](../guides/errors.md). Their reserved template numbers do not make the methods renderable.

## Discover templates

```python
print(cards.templates["profile"])
# (1, 2, 3)

from endfield_cards import TEMPLATES
print(TEMPLATES["character"])
# (1, 2, 3, 4)
```

The catalog uses method names without `_card`. Invalid numbers raise before SDK requests or image downloads.
