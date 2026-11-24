"""Promote audited symbols and fonts into installable, verified package resources.

Run from any directory: python cards/tools/promote_assets.py
The optional development dependency resvg-py rasterizes the original player SVGs.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageFont

PROJECT = Path(__file__).resolve().parents[1]
WORKSPACE = PROJECT.parent
DEFAULT_DESTINATION = PROJECT / "src/endfield_cards/assets/resources"

PLAYER_NAMES = {
    "crisis-contract": "contingency-contract",
    "indie-hard": "monument",
    "indie-dg007": "monument-detailed",
    "realtime": "activity",
    "spaceship": "factory",
    "room-manufacture": "room-manufacturing",
    "war-echoes": "war-echoes",
    "sanity-icon": "sanity",
    "sanity": "sanity-background",
}
PROFESSION_NAMES = {"assault": "striker"}
ELEMENT_NAMES = {"cryst": "cryo", "fire": "heat", "natural": "nature", "pulse": "electric"}
WEAPON_NAMES = {"claymores": "greatsword", "wand": "arts-unit", "pistol": "handcannon", "lance": "polearm"}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def promote(destination: Path = DEFAULT_DESTINATION) -> dict[str, Any]:
    """Validate each selected input and write a deterministic semantic manifest."""
    catalog = json.loads((PROJECT / "assets/catalog.json").read_text(encoding="utf-8"))
    records = {record["path"]: record for record in catalog["assets"]}
    sources = {source["name"]: source for source in catalog["sources"]}
    player_manifest = json.loads(
        (PROJECT / "assets/staging/endfield-discord-bot/manifest.json").read_text(encoding="utf-8")
    )
    source_notice = PROJECT / "assets/staging/endfield-discord-bot/UPSTREAM-SOURCES.md"
    records[source_notice.relative_to(PROJECT).as_posix()] = {
        **player_manifest["upstream_sources"],
        "source_path": "src/assets/player/SOURCES.md",
        "source_url": player_manifest["upstream_sources"]["url"],
        "source_checkout": "endfield-discord-bot",
        "source_checkout_commit": player_manifest["revision"],
        "bytes": source_notice.stat().st_size,
    }
    entries: dict[str, dict[str, Any]] = {}
    aliases: dict[str, str] = {}
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)

    def add(
        key: str,
        source: Path,
        relative: str,
        *,
        original_path: str | None = None,
        data: bytes | None = None,
        transformation: str | None = None,
    ) -> None:
        original = source.read_bytes()
        original_path = original_path or source.relative_to(PROJECT).as_posix()
        record = records.get(original_path, {})
        source_checkout = record.get("source_checkout", "akef-cards")
        digest = _sha(original)
        if record and (record["sha256"] != digest or record["bytes"] != len(original)):
            raise ValueError(f"Source catalog checksum mismatch: {original_path}")
        payload = original if data is None else data
        target = destination / relative
        if not target.resolve().is_relative_to(destination):
            raise ValueError("Destination escapes the resources directory")
        target.parent.mkdir(parents=True, exist_ok=True)
        metadata: dict[str, Any] = {
            "path": relative,
            "sha256": _sha(payload),
            "bytes": len(payload),
            "source_path": record.get("source_path", original_path),
            "staging_path": original_path,
            "source_sha256": digest,
            "source_bytes": len(original),
            "source_checkout": source_checkout,
            "source_revision": record.get(
                "source_checkout_commit", sources[source_checkout]["checkout_commit"]
            ),
            "source_url": record.get("source_url"),
            "asset_terms": record.get("redistribution_status", "See preserved source license notices"),
        }
        if transformation:
            metadata["transformation"] = transformation
        if relative.endswith(".png"):
            with Image.open(io.BytesIO(payload)) as image:
                image.load()
                metadata.update(
                    media_type="image/png", width=image.width, height=image.height, mode=image.mode
                )
                if image.width * image.height > 24_000_000:
                    raise ValueError(f"Resource exceeds decoded pixel budget: {relative}")
        elif relative.endswith(".ttf"):
            ImageFont.truetype(io.BytesIO(payload), 16)
            metadata["media_type"] = "font/ttf"
        elif relative.endswith(".svg"):
            metadata["media_type"] = "image/svg+xml"
        else:
            metadata["media_type"] = "text/plain"
        if not target.exists() or target.read_bytes() != payload:
            target.write_bytes(payload)
        entries[key] = metadata

    groups = catalog["groups"]
    for stat_id, spec in groups["stats"].items():
        if not spec.get("path"):
            continue
        name = spec["key"].replace("_", "-")
        key = f"stat.{spec['key']}"
        add(key, PROJECT / spec["path"], f"icons/stats/{name}.png")
        aliases[f"stat.{stat_id}"] = key
        aliases[f"stat.{Path(spec['path']).stem}"] = key
        for wire_key in spec["wire_keys"]:
            aliases[f"stat.{wire_key}"] = key

    for group, prefix, folder, renames in (
        ("professions", "profession", "professions", PROFESSION_NAMES),
        ("elements", "element", "elements", ELEMENT_NAMES),
        ("weapon_types", "weapon", "weapons", WEAPON_NAMES),
        ("potential", "potential", "potential", {}),
        ("rarity", "rarity", "rarity", {}),
    ):
        for name, spec in groups[group].items():
            canonical = renames.get(name, name)
            if group == "potential":
                canonical = name.removeprefix("pote-")
            key = f"{prefix}.{canonical}"
            add(key, PROJECT / spec["path"], f"icons/{folder}/{canonical}.png")
            for alias in (name, name.upper(), spec.get("wire_key")):
                if alias and f"{prefix}.{alias}" != key:
                    aliases[f"{prefix}.{alias}"] = key
    aliases.update(
        {
            f"element.{name}": f"element.{ELEMENT_NAMES.get(target, target)}"
            for name, target in groups["element_aliases"].items()
        }
    )

    for name, spec in groups["general"].items():
        canonical = PLAYER_NAMES.get(name, name)
        source = PROJECT / spec["path"]
        key = f"player.{canonical}"
        if source.suffix == ".svg":
            try:
                import resvg_py
            except ImportError as exc:
                raise RuntimeError("SVG asset promotion requires: pip install resvg-py==0.5.0") from exc
            svg = source.read_text(encoding="utf-8")
            rendered = resvg_py.svg_to_bytes(svg_string=svg, width=192, height=192, skip_system_fonts=True)
            add(
                key,
                source,
                f"icons/player/{canonical}.png",
                data=rendered,
                transformation="Original SVG rasterized at 192x192 by resvg-py 0.5.0; geometry unchanged",
            )
            add(f"source.player.{canonical}", source, f"sources/player/{canonical}.svg")
        else:
            add(key, source, f"icons/player/{canonical}.png")
        if name != canonical:
            aliases[f"player.{name}"] = key
    aliases["player.monument-event"] = "player.monument-detailed"
    aliases["player.contract"] = "player.contingency-contract"

    for name, spec in groups["fonts"].items():
        family = "barlow" if name.startswith("barlow-") else "fira"
        weight = name.removeprefix("barlow-").removeprefix("fira-sans-").replace("semi-bold", "semibold")
        add(f"font.{family}.{weight}", PROJECT / spec["path"], f"fonts/{family}-{weight}.ttf")

    for locale, filename in {
        "ja": "NotoSansJP.ttf",
        "ko": "NotoSansKR.ttf",
        "zh-Hans": "NotoSansSC.ttf",
        "zh-Hant": "NotoSansTC.ttf",
        "th": "NotoSansThai.ttf",
    }.items():
        source = WORKSPACE / "akef-cards/akef_cards/fonts" / filename
        add(
            f"font.noto.{locale}",
            source,
            f"fonts/noto-{locale}.ttf",
            original_path=f"../akef-cards/akef_cards/fonts/{filename}",
        )

    for name, spec in groups["notices"].items():
        add(f"license.{name}", PROJECT / spec["path"], f"licenses/{name}.txt")
    add(
        "license.noto.ofl",
        WORKSPACE / "akef-cards/akef_cards/fonts/OFL-Noto.txt",
        "licenses/noto-ofl.txt",
        original_path="../akef-cards/akef_cards/fonts/OFL-Noto.txt",
    )
    add(
        "license.player.sources",
        PROJECT / "assets/staging/endfield-discord-bot/UPSTREAM-SOURCES.md",
        "licenses/player-sources.md",
    )
    manifest = {
        "schema_version": 1,
        "description": "Installable semantic symbols and licensed fonts; source provenance retained",
        "sources": catalog["sources"],
        "assets": dict(sorted(entries.items())),
        "aliases": dict(sorted((key, value) for key, value in aliases.items() if key not in entries)),
        "missing_stat_glyphs": [stat_id for stat_id, spec in groups["stats"].items() if not spec.get("path")],
        "watermark": "akef-cards • endfield-cards",
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    args = parser.parse_args()
    manifest = promote(args.destination)
    total = sum(entry["bytes"] for entry in manifest["assets"].values())
    print(
        f"Promoted {len(manifest['assets'])} resources, {len(manifest['aliases'])} aliases, {total:,} bytes"
    )


if __name__ == "__main__":
    main()
