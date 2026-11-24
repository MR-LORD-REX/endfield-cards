"""Render detailed-card previews from local snapshots and verified cached images only.

Expired cache payloads may be reused for visual review after size/hash validation.
The cache is read-only and this tool never authenticates or downloads an image.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sys
import time
from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT.parent / "skport-py/src")]

from PIL import Image  # noqa: E402
from skport.games.endfield.models import ContractState, MonumentState, PlayerCard  # noqa: E402

from endfield_cards import CacheConfig, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for, validate_owner  # noqa: E402
from endfield_cards.assets.store import AssetStore  # noqa: E402
from endfield_cards.cache import cache_key  # noqa: E402
from endfield_cards.errors import AssetError, CardError  # noqa: E402
from endfield_cards.rendering import RenderEngine  # noqa: E402
from endfield_cards.utils.selection import default_monument_event_index  # noqa: E402

FAMILIES = {
    "monument": ("monument.json", MonumentState, "monument_detail", "monument-detailed"),
    "contract": (
        "contingency-contract.json",
        ContractState,
        "contingency_contract_detail",
        "contingency-contract-detailed",
    ),
}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("owner_id", nargs="?", help="Directory name under local/family-review")
    result.add_argument("--snapshot-dir", type=Path, help="Directory containing normalized endgame snapshots")
    result.add_argument("--profile-snapshot", type=Path, help="Optional matching normalized PlayerCard")
    result.add_argument("--family", choices=("monument", "contract", "both"), default="both")
    result.add_argument(
        "--template",
        type=int,
        choices=(1, 2),
        action="append",
        help="Repeat to select templates; default: both",
    )
    result.add_argument("--event-id", help="Monument event ID; default: active or latest supplied event")
    result.add_argument("--contract-id", help="Contract ID; default: current or first source contract")
    result.add_argument("--all-runs", action="store_true", help="Export all Contract runs in bounded pages")
    result.add_argument(
        "--cache-dir", type=Path, action="append", help="Read-only image cache; default: local/image-cache"
    )
    result.add_argument("--locale", choices=("en", "ja", "ko", "zh-Hans", "zh-Hant"), default="en")
    result.add_argument("--timezone", default="UTC")
    result.add_argument("--quality", type=int, default=90)
    result.add_argument("--output-dir", type=Path, default=ROOT / "local/detail-previews")
    return result


def image_groups(value: Any) -> Iterator[tuple[str, ...]]:
    """Keep URLs for the same normalized ImageLinks together for provider fallback."""
    if isinstance(value, dict):
        if "url" in value and ("skport" in value or "enka" in value):
            urls = tuple(
                dict.fromkeys(
                    item
                    for item in value.values()
                    if isinstance(item, str) and item.startswith(("https://", "http://"))
                )
            )
            if urls:
                yield urls
        else:
            for item in value.values():
                yield from image_groups(item)
    elif isinstance(value, list):
        for item in value:
            yield from image_groups(item)


def cached_payload(url: str, directories: list[Path], max_bytes: int) -> tuple[bytes | None, int]:
    """Read checked source bytes without altering mtime, expiry or cache contents."""
    key = cache_key("image-source-v1", url)
    name = cache_key("disk-source-v1", key) + ".cache"
    invalid = 0
    for directory in directories:
        path = directory / name
        try:
            with path.open("rb") as stream:
                metadata = json.loads(stream.readline(2048))
                size = metadata.get("bytes")
                if metadata.get("version") != 1 or metadata.get("key") != key:
                    raise ValueError("cache key/version mismatch")
                if type(size) is not int or not 0 < size <= max_bytes:
                    raise ValueError("cache payload exceeds the byte limit")
                data = stream.read(max_bytes + 1)
            if len(data) != size or hashlib.sha256(data).hexdigest() != metadata.get("sha256"):
                raise ValueError("cache payload checksum/size mismatch")
            return data, invalid
        except FileNotFoundError:
            continue
        except (OSError, ValueError, TypeError, AttributeError):
            invalid += 1
    return None, invalid


def local_sources(
    models: list[Any], directories: list[Path], max_bytes: int
) -> tuple[dict[str, bytes], dict[str, int]]:
    groups = [group for model in models for group in image_groups(model.model_dump(mode="json"))]
    unique = dict.fromkeys(url for group in groups for url in group)
    checked = {}
    invalid = 0
    for url in unique:
        data, failures = cached_payload(url, directories, max_bytes)
        checked[url] = data
        invalid += failures
    sources = {url: data for url, data in checked.items() if data is not None}
    exact = len(sources)
    for group in groups:
        fallback = next((sources[url] for url in group if url in sources), None)
        if fallback is not None:
            for url in group:
                sources.setdefault(url, fallback)
    return sources, {
        "source_urls": len(unique),
        "exact_cached_urls": exact,
        "available_urls_with_provider_fallback": len(sources),
        "invalid_cache_entries": invalid,
    }


class OfflineAssets(AssetStore):
    """Keep bundled icons and bounded image decoding; never access HTTP or disk-cache writes."""

    def __init__(self, sources: dict[str, bytes], config: CardsConfig) -> None:
        super().__init__(config.cache, config.download)
        self.sources = sources
        self.used: set[str] = set()
        self.missing: set[str] = set()

    async def get(self, url: str, *, retain: bool = True) -> Image.Image:
        self._assert_open()
        data = self.sources.get(url)
        if data is None:
            self.missing.add(url)
            raise AssetError(
                "Image is unavailable in the offline preview cache", code="offline_image_missing"
            )
        self.used.add(url)
        key = cache_key("offline-preview-v1", hashlib.sha256(data).hexdigest())
        cached = self._memory.get(key) if retain else None
        if cached is not None:
            return cached
        image = await self._decode(data)
        if retain:
            self._memory.put(key, image)
        return image


def snapshot_directory(arguments: argparse.Namespace) -> Path:
    if arguments.snapshot_dir is not None:
        return arguments.snapshot_dir.expanduser().resolve()
    if arguments.owner_id is not None:
        return ROOT / "local/family-review" / arguments.owner_id
    required = tuple(FAMILIES) if arguments.family == "both" else (arguments.family,)
    candidates = sorted(
        directory
        for directory in (ROOT / "local/family-review").glob("*")
        if directory.is_dir() and all((directory / FAMILIES[family][0]).is_file() for family in required)
    )
    if not candidates:
        raise ValueError("No local endgame snapshots found; pass --snapshot-dir")
    return candidates[0]


def matching_profile(arguments: argparse.Namespace, directory: Path, model: Any) -> PlayerCard | None:
    if arguments.profile_snapshot is not None:
        candidates = [arguments.profile_snapshot.expanduser().resolve()]
    else:
        owner_id = str(model.player.skport_id or directory.name)
        candidates = [
            directory / "profile.json",
            directory / "roster.json",
            ROOT / f"local/profile-review/profile-{owner_id}.json",
            ROOT / f"design-data/profile-{owner_id}.json",
        ]
    for path in candidates:
        if not path.is_file():
            if arguments.profile_snapshot is not None:
                raise ValueError("The supplied profile snapshot does not exist")
            continue
        profile = PlayerCard.model_validate_json(path.read_text(encoding="utf-8"))
        validate_owner(profile, context_for(model))
        if (
            profile.player.server_id
            and model.player.server_id
            and profile.player.server_id != model.player.server_id
        ):
            raise ValueError("Profile and endgame snapshot have different servers")
        return profile
    return None


async def main(argv: list[str] | None = None) -> dict[str, Any]:
    arguments = parser().parse_args(argv)
    directory = snapshot_directory(arguments)
    selected = tuple(FAMILIES) if arguments.family == "both" else (arguments.family,)
    models = {}
    for family in selected:
        filename, cls, _, _ = FAMILIES[family]
        path = directory / filename
        if not path.is_file():
            raise ValueError(f"Missing normalized snapshot: {path}")
        models[family] = cls.model_validate_json(path.read_text(encoding="utf-8"))
    first = next(iter(models.values()))
    profile = matching_profile(arguments, directory, first)
    for model in models.values():
        validate_owner(model, context_for(first))
    owner_id = re.sub(r"[^A-Za-z0-9_-]", "-", str(first.player.skport_id or first.player.game_uid))
    output = arguments.output_dir.expanduser().resolve() / owner_id
    config = CardsConfig(
        locale=arguments.locale,
        display_timezone=arguments.timezone,
        output=OutputConfig(format="JPEG", quality=arguments.quality),
        cache=CacheConfig(directory=ROOT / "local/image-cache"),
    )
    cached_models = [*models.values(), *([profile] if profile is not None else [])]
    sources, cache_report = await asyncio.to_thread(
        local_sources,
        cached_models,
        arguments.cache_dir or [ROOT / "local/image-cache"],
        config.download.max_bytes,
    )
    report: dict[str, Any] = {
        "source_directory": str(directory),
        "owner_id": owner_id,
        "offline": True,
        "cache": cache_report,
        "images": [],
    }
    async with (
        OfflineAssets(sources, config) as assets,
        RenderEngine(config=config, asset_store=assets) as engine,
    ):
        for family, model in models.items():
            filename, _, render_family, label = FAMILIES[family]
            options: dict[str, Any] = {"profile": profile} if profile is not None else {}
            if family == "monument":
                index = default_monument_event_index(model.events)
                event = model.events[index] if index is not None else None
                options["event_id"] = (
                    arguments.event_id if arguments.event_id is not None else event.id if event else None
                )
            else:
                current = model.current or (model.contracts[0] if model.contracts else None)
                options["contract_id"] = (
                    arguments.contract_id
                    if arguments.contract_id is not None
                    else current.id
                    if current
                    else None
                )
                options["all_runs"] = arguments.all_runs
            context = replace(
                context_for(model, locale=config.locale), display_timezone=config.display_timezone
            )
            for template in arguments.template or (1, 2):
                started = time.perf_counter()
                pages = await engine.render(
                    render_family,
                    model,
                    context=context,
                    variant="light" if template == 1 else "dark",
                    output=config.output,
                    **options,
                )
                duration = time.perf_counter() - started
                for page in pages:
                    suffix = f"-page-{page.page}" if len(pages) > 1 else ""
                    destination = page.save(output / f"{label}-{template}{suffix}.jpg")
                    entry = {
                        "family": render_family,
                        "template": template,
                        "image": str(destination),
                        "page": page.page,
                        "pages": len(pages),
                        "width": page.width,
                        "height": page.height,
                        "bytes": len(page.data),
                        "render_seconds": round(duration, 3),
                        "selected_id": options.get("event_id", options.get("contract_id")),
                        "issues": sorted({issue.code for issue in page.issues}),
                    }
                    report["images"].append(entry)
                    (output / f"{label}-{template}{suffix}.report.json").write_text(
                        json.dumps(entry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
                    )
            output.mkdir(parents=True, exist_ok=True)
            (output / f"{label}.source.json").write_text(model.model_dump_json(indent=2), encoding="utf-8")
        report["cache"].update({"used_urls": len(assets.used), "missing_urls": len(assets.missing)})
    (output / "endgame-details.report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
    except (CardError, ValueError, OSError) as error:
        raise SystemExit(str(error)) from None
    print(
        f"Saved {len(result['images'])} offline detailed-card images under {Path(result['images'][0]['image']).parent}"
    )
