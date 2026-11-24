"""Fetch and render one concise character style for an explicit SKPort target."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import re
import sys
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path[:0] = [str(ROOT / "src"), str(WORKSPACE / "skport-py/src")]

from render_profile import load_tokens  # noqa: E402
from skport import ClientConfig, ImageSource, SkportClient  # noqa: E402
from skport.games.endfield.models import CharacterBuild, PlayerCard  # noqa: E402

from endfield_cards import Artwork, CacheConfig, Cards, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for  # noqa: E402
from endfield_cards.assets.store import AssetStore  # noqa: E402


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--variant", choices=("field", "dossier", "terminal", "portrait"), default="dossier")
    result.add_argument("--skport-id", help="Public SKPort target; required for a live request")
    selection = result.add_mutually_exclusive_group()
    selection.add_argument("--name", help="Exact localized character name from the public profile")
    selection.add_argument("--character-id", help="Opaque SKPort character ID")
    result.add_argument(
        "--snapshot", type=Path, help="Explicitly render a previously fetched CharacterBuild JSON"
    )
    result.add_argument("--token-file", type=Path, help="Configured token file or ACCOUNT_TOKEN capture")
    result.add_argument("--locale", choices=("en", "ja", "ko", "zh-Hans", "zh-Hant"))
    result.add_argument("--timezone", default="Asia/Kolkata")
    result.add_argument("--assets-dir", type=Path, help="Optional canonical SDK data cache")
    result.add_argument("--format", choices=("JPEG", "PNG", "WEBP"), default="JPEG")
    result.add_argument("--quality", type=int, default=90)
    result.add_argument("--art", type=Path, help="Explicit local custom artwork")
    result.add_argument("--fit", choices=("cover", "contain"), default="cover")
    result.add_argument("--focus", type=float, nargs=2, metavar=("X", "Y"), default=(0.5, 0.35))
    result.add_argument("--output-dir", type=Path, default=ROOT / "local/character-review")
    result.add_argument(
        "--fetch-only", action="store_true", help="Fetch current calculated model without drawing"
    )
    result.add_argument(
        "--inspect-art", action="store_true", help="Include source artwork dimensions and alpha bounds"
    )
    return result


def directory_component(value: str, label: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_-]{1,100}", value) is None:
        raise ValueError(f"The {label} cannot be used as an output-directory component")
    return value


def output_identity(model: CharacterBuild) -> tuple[str, str]:
    if model.owner is None:
        raise ValueError("Character review requires the SDK owner identity")
    owner = directory_component(model.owner.skport_id, "owner ID")
    character = directory_component(model.identity.str_id or model.identity.skport_id, "character ID")
    return owner, character


def verify_selection(model: CharacterBuild, arguments: argparse.Namespace) -> None:
    if arguments.skport_id is not None and (
        model.owner is None or str(arguments.skport_id) != model.owner.skport_id
    ):
        raise ValueError("The requested owner does not match the supplied character snapshot")
    if arguments.name is not None and arguments.name.strip().casefold() != model.name.casefold():
        raise ValueError("The requested name does not match the supplied character snapshot")
    if arguments.character_id is not None and arguments.character_id != model.identity.skport_id:
        raise ValueError("The requested character ID does not match the supplied character snapshot")


async def artwork_metadata(model: CharacterBuild) -> dict[str, Any]:
    result: dict[str, Any] = {}
    async with AssetStore(cache=CacheConfig(directory=ROOT / "local/image-cache")) as store:
        for key in ("splash", "half_body", "portrait", "avatar"):
            links = getattr(model.images, key)
            if not links.url:
                result[key] = {"available": False}
                continue
            try:
                pixels = await store.get(links.url)
                result[key] = {
                    "available": True,
                    "url": links.url,
                    "width": pixels.width,
                    "height": pixels.height,
                    "mode": pixels.mode,
                    "alpha_bounds": pixels.getchannel("A").getbbox(),
                    "alpha_extrema": pixels.getchannel("A").getextrema(),
                }
                pixels.close()
            except Exception as exc:
                result[key] = {"available": True, "url": links.url, "error_type": type(exc).__name__}
    return result


async def main() -> None:
    arguments = parser().parse_args()
    logging.getLogger("skport").setLevel(logging.CRITICAL)
    if arguments.snapshot is None and (
        not arguments.skport_id or not (arguments.name or arguments.character_id)
    ):
        raise ValueError("Supply --skport-id and exactly one of --name/--character-id, or use --snapshot")
    fetched_at = None
    sdk: SkportClient | None = None
    mode = "saved-snapshot" if arguments.snapshot is not None else "live-api"
    try:
        if arguments.snapshot is not None:
            model = CharacterBuild.model_validate_json(arguments.snapshot.read_text(encoding="utf-8"))
            verify_selection(model, arguments)
        else:
            cached_assets = arguments.assets_dir or WORKSPACE / "skport-py/local/fixtures/enka-cache"
            sdk = SkportClient(
                tokens=load_tokens(arguments.token_file),
                config=ClientConfig(
                    lang=arguments.locale or "en",
                    icon_source=ImageSource.ENKA,
                    assets_dir=cached_assets,
                    assets_offline=False,
                    assets_auto_update=False,
                    calculate_stats=True,
                    cache=False,
                    max_attempts=2,
                    timeout=25,
                ),
            )
            await sdk.warm()
            selector = (
                {"char_id": arguments.character_id} if arguments.character_id else {"name": arguments.name}
            )
            response = await sdk.endfield.character(skport_id=arguments.skport_id, full=True, **selector)
            if not isinstance(response, CharacterBuild):
                raise TypeError("The SDK did not return a normalized CharacterBuild")
            model = response
            if model.owner is None or not model.owner.name.strip():
                profile = await sdk.endfield.card(skport_id=arguments.skport_id)
                if not isinstance(profile, PlayerCard):
                    raise TypeError("The SDK did not return a normalized PlayerCard for owner identity")
                if model.owner is not None and model.owner.game_uid != profile.player.game_uid:
                    raise ValueError("Character and profile have different game owners")
                model = model.model_copy(update={"owner": profile.player}, deep=True)
            fetched_at = datetime.now(UTC).isoformat()
            verify_selection(model, arguments)
        owner, character = output_identity(model)
        output = arguments.output_dir.expanduser().resolve() / owner / character
        output.mkdir(parents=True, exist_ok=True)
        if mode == "live-api":
            (output / "character.json").write_text(model.model_dump_json(indent=2), encoding="utf-8")
        report: dict[str, Any] = {
            "source_mode": mode,
            "fetched_at": fetched_at,
            "skport_id": model.owner.skport_id if model.owner else None,
            "game_uid": model.owner.game_uid if model.owner else None,
            "owner_name": model.owner.name if model.owner else None,
            "character": model.name,
            "canonical_character": model.identity.str_id,
            "character_id": model.identity.skport_id,
            "locale": arguments.locale or model.locale,
            "calculation_state": str(model.calculation_state),
            "asset_revision": model.asset_revision,
            "statistics": len(model.stats.values) if model.stats else 0,
            "skills": len(model.skills),
            "talents": len(model.talents.nodes),
            "equipment": len(model.equipment),
            "issues": sorted({issue.code for issue in model.issues}),
        }
        if arguments.inspect_art:
            report["artwork"] = await artwork_metadata(model)
        if arguments.fetch_only:
            (output / "fetch-report.json").write_text(
                json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            print(json.dumps(report, indent=2, ensure_ascii=True))
            return
        locale = arguments.locale or model.locale
        context = replace(context_for(model, locale=locale), display_timezone=arguments.timezone)
        artwork = (
            Artwork(arguments.art, fit=arguments.fit, focal_point=tuple(arguments.focus))
            if arguments.art
            else None
        )
        config = CardsConfig(locale=locale, cache=CacheConfig(directory=ROOT / "local/image-cache"))
        async with Cards(config=config, skport=sdk) as cards:
            results = await cards.render_character(
                model,
                context=context,
                variant=arguments.variant,
                art=artwork,
                output=OutputConfig(format=arguments.format, quality=arguments.quality),
            )
        if len(results) != 1:
            raise ValueError("Character review requires one concise image")
        extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[arguments.format]
        destination = results[0].save(output / f"character-{arguments.variant}.{extension}")
        report.update(
            {
                "variant": arguments.variant,
                "display_timezone": arguments.timezone,
                "custom_art": arguments.art is not None,
                "images": 1,
                "width": results[0].width,
                "height": results[0].height,
                "bytes": len(results[0].data),
                "image": str(destination),
                "issues": sorted(set(report["issues"]) | {issue.code for issue in results[0].issues}),
            }
        )
        (output / f"character-{arguments.variant}.report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(json.dumps(report, ensure_ascii=True, indent=2))
    finally:
        if sdk is not None:
            await sdk.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        raise SystemExit(f"Character review failed: {type(exc).__name__}") from None
