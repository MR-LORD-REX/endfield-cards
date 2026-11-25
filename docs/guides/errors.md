# Errors and unavailable cards

Card methods raise typed errors when a request cannot be completed. All library errors derive from `CardError` and expose a stable `.code`.

```python
from endfield_cards import CardError

try:
    result = await cards.profile_card(skport_id, template=1)
except CardError as error:
    print(error.code)
```

## Common errors

- `UnsupportedVariantError` (`unsupported_variant`): the template number is invalid for that card.
- `DataValidationError` (`invalid_data`): target or selector arguments are invalid.
- `OwnerMismatchError` (`owner_mismatch`): supplied owner identities disagree.
- `FetchError` (`fetch_failed`): the SDK could not fetch the requested data. The original exception is available as `__cause__`.
- `DownloadError` (`download_failed`): a required image download failed.
- `EncodingError` (`encoding_failed`): output encoding or the configured byte limit failed.
- `ResourceClosedError` (`resource_closed`): the cards client is already closed.

Individual error classes are available from `endfield_cards.errors`. Optional missing artwork can be reported in `result.cards[n].issues` while the card uses a fallback. SDK source-data issues remain in `result.model`.

For token problems, profile visibility, and SDK retries, follow [skport-py's error guide](https://mr-lord-rex.github.io/skport-py/#/guides/errors-and-retries).

## Pulls and Wiki

`pulls_card()` and `wiki_card()` currently raise `CardNotImplementedError` before fetching data, downloading images, or rendering. It is also a standard Python `NotImplementedError`; its `.code` is `"not_implemented"`.

```python
from endfield_cards import CardNotImplementedError

try:
    await cards.pulls_card()
except CardNotImplementedError:
    print("Pulls cards are not available yet")
```

`await cards.wiki_card()` raises the same error. Use skport-py directly for supported [pull-history data](https://mr-lord-rex.github.io/skport-py/#/reference/endfield).
