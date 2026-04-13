"""
Asset resolver: loads static JSON asset files and fetches missing weapon/suit
details from the endfieldtools API, caching them locally.

Asset folder layout expected:
    assets/
    ├── weapons/           ← per-weapon detail JSONs  (wpn_sword_0006.json)
    ├── equips/            ← per-suit detail JSONs    (suit_fire_natr01.json)
    ├── characters.json
    ├── equipments.json
    ├── suits.json
    ├── weapons.json
    ├── other.json
    ├── prop_id_to_name.json
    └── prop_name_to_id.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

import aiohttp

logger = logging.getLogger(__name__)

ENKA_BASE = "https://enka.network"
ENDFIELDTOOLS_BASE = "https://endfieldtools.dev/localdb/optimized"

# Attribute key names used in weapon blackboards → prop IDs
_WPN_KEY_TO_PROP: dict[str, int] = {
    "wisd": 41,
    "agi":  40,
    "str":  39,
    "will": 42,
    "atk":   2,
}


class AssetResolver:
    """
    Loads all static asset JSONs at construction time.
    Provides sync lookups for characters / equips / suits / weapons,
    and async helpers for fetching + caching missing weapon / suit details.
    """

    def __init__(self, assets_path: Path | str, session: aiohttp.ClientSession) -> None:
        self.assets_path = Path(__file__).parent / "assets"
        self.session = session
        self._load_all()

    # ------------------------------------------------------------------
    # Initialisation helpers
    # ------------------------------------------------------------------

    def _load_json(self, filename: str) -> dict:
        path = self.assets_path / filename
        if not path.exists():
            logger.warning("Asset file not found: %s", path)
            return {}
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    def _load_all(self) -> None:
        self.characters:       dict = self._load_json("characters.json")
        self.equipments:       dict = self._load_json("equipments.json")
        self.suits:            dict = self._load_json("suits.json")
        self.weapons:          dict = self._load_json("weapons.json")
        self.other:            dict = self._load_json("other.json")
        self.prop_id_to_name:  dict = self._load_json("prop_id_to_name.json")
        self.prop_name_to_id:  dict = self._load_json("prop_name_to_id.json")

        # Reverse map: str_id (e.g. "chr_0016_laevat") → template_id string key ("23")
        self._str_id_map: dict[str, str] = {
            meta["str_id"]: tid
            for tid, meta in self.characters.items()
            if "str_id" in meta
        }

    # ------------------------------------------------------------------
    # Sync lookups
    # ------------------------------------------------------------------

    def get_character(self, template_id: int | str) -> Optional[dict]:
        """Look up character metadata by numeric template ID."""
        return self.characters.get(str(template_id))

    def get_character_by_str_id(self, str_id: str) -> Optional[dict]:
        """Look up character metadata by string ID (e.g. 'chr_0016_laevat')."""
        tid = self._str_id_map.get(str_id)
        return self.characters.get(tid) if tid else None

    def get_template_id(self, str_id: str) -> int:
        """Return numeric template ID for a given str_id, or 0 if unknown."""
        tid = self._str_id_map.get(str_id)
        return int(tid) if tid else 0

    def get_equipment(self, template_id: int | str) -> Optional[dict]:
        return self.equipments.get(str(template_id))

    def get_suit_basic(self, suit_id: str) -> Optional[dict]:
        """Return the minimal suit entry from suits.json (icon, skill_id, name_hash)."""
        return self.suits.get(suit_id)

    def get_prop_name(self, prop_id: int) -> str:
        return self.prop_id_to_name.get(str(prop_id), f"prop_{prop_id}")

    def get_break_to_ascension(self) -> dict[str, int]:
        return self.other.get("break_to_ascension", {})

    # ------------------------------------------------------------------
    # URL helpers
    # ------------------------------------------------------------------

    def icon_url(self, path: str) -> str:
        """Prepend ENKA_BASE to a relative asset path. Passes full URLs through."""
        if not path:
            return ""
        if path.startswith("http"):
            return path
        return f"{ENKA_BASE}{path}"

    def char_remote_icon_url(self, str_id: str) -> str:
        return f"{ENKA_BASE}/ui/ef/charremoteicon/icon_{str_id}.png"

    def attr_icon_url(self, attr_key: str) -> str:
        """Return the attribute icon URL for a given key name (e.g. 'wisd')."""
        return f"{ENKA_BASE}/ui/ef/attributeicon/{attr_key.capitalize()}.png"

    # ------------------------------------------------------------------
    # Async remote fetchers (with local cache)
    # ------------------------------------------------------------------

    async def get_weapon_detail(self, weapon_id: str) -> Optional[dict]:
        """
        Return full weapon detail JSON.
        Checks assets/weapons/{weapon_id}.json first; fetches from endfieldtools
        and caches locally if absent.
        weapon_id is the slug/ID like "wpn_sword_0006".
        """
        cache_path = self.assets_path / "weapons" / f"{weapon_id}.json"
        if cache_path.exists():
            with open(cache_path, encoding="utf-8") as fh:
                return json.load(fh)

        url = f"{ENDFIELDTOOLS_BASE}/weapons/details/{weapon_id}.json"
        return await self._fetch_and_cache(url, cache_path)

    async def get_suit_detail(self, suit_id: str) -> Optional[dict]:
        """
        Return full suit detail JSON.
        Checks assets/equips/{suit_id}.json first; fetches from endfieldtools
        and caches locally if absent.
        """
        cache_path = self.assets_path / "equips" / f"{suit_id}.json"
        if cache_path.exists():
            with open(cache_path, encoding="utf-8") as fh:
                return json.load(fh)

        url = f"{ENDFIELDTOOLS_BASE}/equipment/suits/details/{suit_id}.json"
        return await self._fetch_and_cache(url, cache_path)

    async def _fetch_and_cache(self, url: str, cache_path: Path) -> Optional[dict]:
        """Fetch JSON from URL; on success write to cache_path. Returns None on failure."""
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    logger.warning("Remote fetch failed (%d): %s", resp.status, url)
                    return None
                data: dict = await resp.json(content_type=None)

            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)

            logger.info("Cached remote asset → %s", cache_path)
            return data

        except Exception as exc:
            logger.error("Failed to fetch %s: %s", url, exc)
            return None
