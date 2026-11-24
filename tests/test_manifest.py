"""Verify installed resource integrity and font selection without networking."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from PIL import Image

from endfield_cards.assets.fonts import FontManager
from endfield_cards.assets.manifest import Manifest
from endfield_cards.errors import AssetError


def test_all_bundled_resources_are_verified_and_images_decode() -> None:
    with Manifest() as manifest:
        assert manifest.watermark == "akef-cards • endfield-cards"
        for key in manifest.keys:
            path = manifest.path(key)
            if manifest.entries[key]["media_type"] == "image/png":
                with Image.open(path) as image:
                    image.load()
                    assert (image.width, image.height) == (
                        manifest.entries[key]["width"],
                        manifest.entries[key]["height"],
                    )


def test_semantic_names_and_sdk_aliases_refer_to_same_assets() -> None:
    manifest = Manifest()
    assert manifest.path("stat.1") == manifest.path("stat.MaxHp") == manifest.path("stat.hp")
    assert manifest.path("profession.ASSAULT").name == "striker.png"
    assert manifest.path("weapon.wand").name == "arts-unit.png"
    assert manifest.path("element.pulse").name == "electric.png"
    assert manifest.path("player.indie-hard").name == "monument.png"
    assert manifest.path("player.monument-event").name == "monument-detailed.png"
    assert manifest.path("player.crisis-contract").name == "contingency-contract.png"


def test_unknown_stat_has_no_misleading_fallback_icon() -> None:
    manifest = Manifest()
    for key in ("stat.13", "stat.10000", "stat.unrecognized"):
        with pytest.raises(AssetError) as error:
            manifest.path(key)
        assert error.value.code == "asset_not_found"


def _temporary_manifest(root: Path, path: str = "symbol.bin") -> None:
    payload = b"verified symbol"
    (root / "symbol.bin").write_bytes(payload)
    document = {
        "schema_version": 1,
        "watermark": "akef-cards • endfield-cards",
        "assets": {
            "test.symbol": {
                "path": path,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        },
    }
    (root / "manifest.json").write_text(json.dumps(document), encoding="utf-8")


def test_resource_mutation_after_first_read_is_detected(tmp_path: Path) -> None:
    _temporary_manifest(tmp_path)
    manifest = Manifest(tmp_path)
    assert manifest.path("test.symbol").read_bytes() == b"verified symbol"
    (tmp_path / "symbol.bin").write_bytes(b"corrupted resource")
    with pytest.raises(AssetError) as error:
        manifest.path("test.symbol")
    assert error.value.code == "asset_integrity"


@pytest.mark.parametrize("path", ["../outside.bin", "/outside.bin", "icons\\..\\outside.bin"])
def test_manifest_rejects_paths_outside_resource_root(tmp_path: Path, path: str) -> None:
    _temporary_manifest(tmp_path, path)
    with pytest.raises(AssetError) as error:
        Manifest(tmp_path).path("test.symbol")
    assert error.value.code == "asset_path_invalid"


def test_font_cache_is_bounded_and_script_selection_works() -> None:
    manager = FontManager(limit=2)
    first = manager.get(24, "bold", "en")
    assert manager.get(24, "bold", "en") is first
    for text, expected in [
        ("\u5e72\u5458", "zh-Hans"),
        ("\u30aa\u30da\u30ec\u30fc\u30bf\u30fc", "ja"),
        ("\uc624\ud37c\ub808\uc774\ud130", "ko"),
        ("\u6a94\u6848", "zh-Hant"),
        ("\u0e41\u0e1f\u0e49\u0e21", "th"),
    ]:
        font = manager.get(24, locale=expected, text=text)
        assert Path(font.path).name == f"noto-{expected}.ttf"
        assert font.getlength(text) > 0
        assert manager.cached_fonts <= 2
    manager.clear()
    assert manager.cached_fonts == 0


def test_script_fallback_works_for_a_foreign_name_in_english_card() -> None:
    manager = FontManager()
    assert Path(manager.get(22, locale="en", text="\uc544\ub378\ub9ac\uc544").path).name == "noto-ko.ttf"
    assert Path(manager.get(22, locale="en", text="\u30c6\u30b9\u30c8").path).name == "noto-ja.ttf"
    assert Path(manager.get(22, locale="en", text="\u6d4b\u8bd5").path).name == "noto-zh-Hans.ttf"
