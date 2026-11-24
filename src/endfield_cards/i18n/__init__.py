"""Central semantic labels, locale aliases and deterministic fallback."""

import json
from functools import lru_cache
from importlib.resources import files

LOCALES = ("en", "ja", "ko", "zh-Hans", "zh-Hant")
_ALIASES = {
    "en-us": "en",
    "en-gb": "en",
    "jp": "ja",
    "ja-jp": "ja",
    "kr": "ko",
    "ko-kr": "ko",
    "zh-cn": "zh-Hans",
    "zh-sg": "zh-Hans",
    "zh-tw": "zh-Hant",
    "zh-hk": "zh-Hant",
    "zh-hans": "zh-Hans",
    "zh-hant": "zh-Hant",
    "cn": "zh-Hans",
    "tw": "zh-Hant",
}


def normalize_locale(locale: str) -> str:
    key = str(locale).strip().replace("_", "-").lower()
    result = _ALIASES.get(key, key)
    if result not in LOCALES:
        raise ValueError(f"unsupported locale {locale!r}; choose one of {LOCALES}")
    return result


@lru_cache(maxsize=5)
def catalog(locale: str) -> dict[str, str]:
    path = files(__package__).joinpath("locales", f"{normalize_locale(locale)}.json")
    return json.loads(path.read_text(encoding="utf-8"))


def t(key: str, locale: str = "en", **values: object) -> str:
    english = catalog("en")
    canonical = next((name for name in english if name.casefold() == key.casefold()), key)
    text = catalog(locale).get(canonical, english.get(canonical, key))
    return text.format(**values) if values else text
