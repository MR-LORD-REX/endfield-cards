"""Bounded font selection for industrial Latin typography and localized data."""

from __future__ import annotations

from collections import OrderedDict
from threading import RLock

from PIL import ImageFont

from endfield_cards.assets.manifest import Manifest
from endfield_cards.errors import AssetError


def _script_locale(text: str, locale: str) -> str | None:
    if any("\uac00" <= character <= "\ud7af" or "\u1100" <= character <= "\u11ff" for character in text):
        return "ko"
    if any("\u3040" <= character <= "\u30ff" for character in text):
        return "ja"
    if any("\u0e00" <= character <= "\u0e7f" for character in text):
        return "th"
    if any(
        "\u3400" <= character <= "\u9fff" or "\U00020000" <= character <= "\U0003134f" for character in text
    ):
        return locale if locale in {"ja", "ko", "zh-Hans", "zh-Hant"} else "zh-Hans"
    if any("\u2150" <= character <= "\u21ff" for character in text):
        return locale if locale in {"ja", "ko", "zh-Hans", "zh-Hant"} else "zh-Hans"
    return locale if locale in {"ja", "ko", "zh-Hans", "zh-Hant", "th"} else None


class FontManager:
    """Load immutable font faces on demand in a thread-safe, bounded LRU."""

    def __init__(self, limit: int = 64, *, manifest: Manifest | None = None) -> None:
        if not isinstance(limit, int) or limit < 1:
            raise ValueError("Font cache limit must be a positive integer")
        self.limit = limit
        self._manifest = manifest
        self._fonts: OrderedDict[tuple[str, int], ImageFont.FreeTypeFont] = OrderedDict()
        self._lock = RLock()

    def get(
        self,
        size: int,
        weight: str = "regular",
        locale: str = "en",
        text: str | None = None,
        *,
        family: str = "barlow",
    ) -> ImageFont.FreeTypeFont:
        """Select a font using locale and the script of supplied text.

        Noto faces cover each supported East Asian script and Latin labels. The
        source supplies one Noto weight, so bold requests use that actual face.
        """
        if not isinstance(size, int) or isinstance(size, bool) or not 1 <= size <= 512:
            raise ValueError("Font size must be an integer between 1 and 512")
        normalized = {
            "zh-cn": "zh-Hans",
            "zh-tw": "zh-Hant",
            "zh-hans": "zh-Hans",
            "zh-hant": "zh-Hant",
            "jp": "ja",
            "kr": "ko",
        }.get(locale.lower(), locale)
        script = _script_locale(text or "", normalized)
        weight = {"semi-bold": "semibold", "semi_bold": "semibold", "normal": "regular"}.get(weight, weight)
        if weight not in {"regular", "medium", "semibold", "bold"}:
            raise ValueError("Unknown font weight")
        if family not in {"barlow", "fira"}:
            raise ValueError("Unknown Latin font family")
        if script is None and text and any("\u0370" <= character <= "\u03ff" for character in text):
            family = "fira"
        key = f"font.noto.{script}" if script else f"font.{family}.{weight}"
        cache_key = (key, size)
        with self._lock:
            if cache_key in self._fonts:
                self._fonts.move_to_end(cache_key)
                return self._fonts[cache_key]
            if self._manifest is None:
                self._manifest = Manifest()
            try:
                font = ImageFont.truetype(str(self._manifest.path(key)), size)
            except OSError as exc:
                raise AssetError("Bundled font cannot be loaded", code="font_load_failed") from exc
            self._fonts[cache_key] = font
            while len(self._fonts) > self.limit:
                self._fonts.popitem(last=False)
            return font

    def clear(self) -> None:
        """Release cached font objects without altering caller-owned images."""
        with self._lock:
            self._fonts.clear()

    @property
    def cached_fonts(self) -> int:
        with self._lock:
            return len(self._fonts)
