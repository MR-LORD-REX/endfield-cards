# Examples

Install `endfield-cards`, then provide `SKPORT_TOKEN` and `SKPORT_ID` through your
environment. Follow the SKPort guides for
[account tokens](https://mr-lord-rex.github.io/skport-py/#/getting-started/account-tokens)
and [public IDs and privacy](https://mr-lord-rex.github.io/skport-py/#/guides/skport-id-and-privacy).

- `python examples/public_cards.py`: profile, factory and exploration cards.
- `python examples/character_and_compare.py`: an operator card and a comparison.
  Also set `SKPORT_COMPARE_ID` and `CHARACTER_NAME`; that operator must be exposed by both players.
- `python examples/owner_roster.py`: the token owner's complete roster, preserving all pages.

Run these commands from the repository root. Generated images are saved in `output/`;
the examples never save JSON. For accounts with multiple roles, pass the chosen SDK
role to owner methods as described in the [owner guide](https://mr-lord-rex.github.io/skport-py/#/guides/owner-accounts).

[`output/`](output/) contains 25 previews organized as `<card-type>/<template-number>.png`.
They use public player `2348675939926`; the roster and the second comparison build
use authenticated owner `1705883884575`. The two older pulls fixture previews are
preserved in `output/reference/pulls/`; pulls and wiki cards are currently unavailable.
