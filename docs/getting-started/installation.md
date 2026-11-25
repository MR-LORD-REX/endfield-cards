# Installation

Requires Python 3.11 or newer.

```console
python -m pip install endfield-cards
```

Pillow, aiohttp, timezone data, and skport-py are installed as dependencies. To include prerelease versions, use `python -m pip install --pre endfield-cards`.

## Prepare authentication and a target

Follow the skport-py guides for your [account token](https://mr-lord-rex.github.io/skport-py/#/getting-started/account-tokens) and the target's [SKPORT ID and profile privacy](https://mr-lord-rex.github.io/skport-py/#/guides/skport-id-and-privacy).

The examples read `SKPORT_TOKEN` and `SKPORT_ID` from environment variables. `EF_Cards` itself receives an explicit SDK or API and does not read credentials from the environment.

Continue with the [quickstart](quickstart.md).
