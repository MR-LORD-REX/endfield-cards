"""Fetch two builds of the same character and render one concise comparison."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path[:0] = [str(ROOT / "src"), str(WORKSPACE / "skport-py/src")]

from render_character import output_identity, verify_selection  # noqa: E402
from render_profile import load_tokens  # noqa: E402
from skport import ClientConfig, ImageSource, Language, SkportClient  # noqa: E402
from skport.games.endfield.models import CharacterBuild, PlayerCard  # noqa: E402

from endfield_cards import Artwork, CacheConfig, Cards, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for  # noqa: E402
from endfield_cards.rendering.templates.compare import validate_pair  # noqa: E402


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--variant", choices=("field", "dossier", "terminal", "portrait"), default="field")
    result.add_argument("--first-skport-id", help="Public SKPort target for the left build")
    result.add_argument("--second-skport-id", help="Public SKPort target for the right build")
    result.add_argument("--name", help="Exact localized character name shared by both builds")
    result.add_argument("--first-character-id", help="Opaque character ID belonging to the first target")
    result.add_argument("--second-character-id", help="Opaque character ID belonging to the second target")
    result.add_argument("--first-snapshot", type=Path, help="Explicit first CharacterBuild JSON snapshot")
    result.add_argument("--second-snapshot", type=Path, help="Explicit second CharacterBuild JSON snapshot")
    result.add_argument("--token-file", type=Path, help="Configured token file or ACCOUNT_TOKEN capture")
    result.add_argument("--locale", choices=("en", "ja", "ko", "zh-Hans", "zh-Hant"))
    result.add_argument("--timezone", default="Asia/Kolkata")
    result.add_argument("--assets-dir", type=Path, help="Optional canonical SDK data cache")
    result.add_argument("--format", choices=("JPEG", "PNG", "WEBP"), default="JPEG")
    result.add_argument("--quality", type=int, default=90)
    result.add_argument("--first-art", type=Path, help="Independent local artwork for the first build")
    result.add_argument("--second-art", type=Path, help="Independent local artwork for the second build")
    for side in ("first", "second"):
        result.add_argument(f"--{side}-fit", choices=("cover", "contain"), default="cover")
        result.add_argument(f"--{side}-focus", type=float, nargs=2, metavar=("X", "Y"), default=(0.5, 0.35))
    result.add_argument("--output-dir", type=Path, default=ROOT / "local/compare-review")
    result.add_argument("--fetch-only", action="store_true", help="Save current models without drawing")
    result.add_argument("--details", action="store_true", help="Explicitly export supplementary build pages")
    return result


def selection_for(arguments: argparse.Namespace, side: str) -> argparse.Namespace:
    selection = argparse.Namespace(
        skport_id=getattr(arguments, f"{side}_skport_id"),
        character_id=getattr(arguments, f"{side}_character_id"),
        name=arguments.name,
        snapshot=getattr(arguments, f"{side}_snapshot"),
    )
    if selection.name and selection.character_id:
        raise ValueError(f"Choose --name or --{side}-character-id for the {side} build")
    if selection.snapshot is None and (
        not selection.skport_id or not (selection.name or selection.character_id)
    ):
        raise ValueError(f"The {side} live build requires its SKPort target and a character selector")
    return selection


async def fetch_character(sdk: SkportClient, selection: argparse.Namespace) -> CharacterBuild:
    selector = {"char_id": selection.character_id} if selection.character_id else {"name": selection.name}
    response = await sdk.endfield.character(skport_id=selection.skport_id, full=True, **selector)
    if not isinstance(response, CharacterBuild):
        raise TypeError("The SDK did not return a normalized CharacterBuild")
    model = response
    if model.owner is None or not model.owner.name.strip():
        profile = await sdk.endfield.card(skport_id=selection.skport_id)
        if not isinstance(profile, PlayerCard):
            raise TypeError("The SDK did not return a normalized PlayerCard for owner identity")
        if model.owner is not None and model.owner.game_uid != profile.player.game_uid:
            raise ValueError("Character and profile have different game owners")
        model = model.model_copy(update={"owner": profile.player}, deep=True)
    verify_selection(model, selection)
    return model


def output_pair(first: CharacterBuild, second: CharacterBuild) -> tuple[str, str, str]:
    """Include both targets because opaque character IDs can match across owners."""
    validate_pair(first, second)
    first_owner, canonical = output_identity(first)
    second_owner, _ = output_identity(second)
    return first_owner, second_owner, canonical


def model_report(model: CharacterBuild, mode: str, fetched_at: str | None) -> dict[str, Any]:
    return {
        "source_mode": mode,
        "fetched_at": fetched_at,
        "skport_id": model.owner.skport_id if model.owner else None,
        "game_uid": model.owner.game_uid if model.owner else None,
        "owner_name": model.owner.name if model.owner else None,
        "character": model.name,
        "canonical_character": model.identity.str_id,
        "character_id": model.identity.skport_id,
        "locale": model.locale,
        "calculation_state": str(model.calculation_state),
        "asset_revision": model.asset_revision,
        "statistics": len(model.stats.values) if model.stats else 0,
        "skills": len(model.skills),
        "talents": len(model.talents.nodes),
        "equipment": len(model.equipment),
        "issues": sorted({issue.code for issue in model.issues}),
    }


async def main(argv: list[str] | None = None) -> dict[str, Any]:
    arguments = parser().parse_args(argv)
    logging.getLogger("skport").setLevel(logging.CRITICAL)
    selections = [selection_for(arguments, side) for side in ("first", "second")]
    sdk: SkportClient | None = None
    models: list[CharacterBuild] = []
    reports: list[dict[str, Any]] = []
    try:
        if any(selection.snapshot is None for selection in selections):
            sdk = SkportClient(
                tokens=load_tokens(arguments.token_file),
                config=ClientConfig(
                    lang=Language(arguments.locale or "en"),
                    icon_source=ImageSource.ENKA,
                    assets_dir=arguments.assets_dir or WORKSPACE / "skport-py/local/fixtures/enka-cache",
                    assets_offline=False,
                    assets_auto_update=False,
                    calculate_stats=True,
                    cache=False,
                    max_attempts=2,
                    timeout=25,
                ),
            )
            await sdk.warm()
        for selection in selections:
            fetched_at = None
            if selection.snapshot is not None:
                model = CharacterBuild.model_validate_json(selection.snapshot.read_text(encoding="utf-8"))
                verify_selection(model, selection)
                mode = "saved-snapshot"
            else:
                if sdk is None:
                    raise RuntimeError("A live comparison requires an SDK client")
                model = await fetch_character(sdk, selection)
                fetched_at = datetime.now(UTC).isoformat()
                mode = "live-api"
            models.append(model)
            reports.append(model_report(model, mode, fetched_at))
        first, second = models
        first_owner, second_owner, canonical = output_pair(first, second)
        output = arguments.output_dir.expanduser().resolve() / first_owner / second_owner / canonical
        output.mkdir(parents=True, exist_ok=True)
        for side, model, report in zip(("first", "second"), models, reports, strict=True):
            if report["source_mode"] == "live-api":
                (output / f"{side}-character.json").write_text(
                    model.model_dump_json(indent=2), encoding="utf-8"
                )
        report = {"first": reports[0], "second": reports[1], "canonical_character": canonical}
        if arguments.fetch_only:
            (output / "fetch-report.json").write_text(
                json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            print(json.dumps(report, indent=2, ensure_ascii=True))
            return report
        locale = arguments.locale or first.locale
        contexts = [
            replace(context_for(model, locale=locale), display_timezone=arguments.timezone)
            for model in models
        ]
        artworks = [
            Artwork(
                getattr(arguments, f"{side}_art"),
                fit=getattr(arguments, f"{side}_fit"),
                focal_point=tuple(getattr(arguments, f"{side}_focus")),
            )
            if getattr(arguments, f"{side}_art") is not None
            else None
            for side in ("first", "second")
        ]
        config = CardsConfig(locale=locale, cache=CacheConfig(directory=ROOT / "local/image-cache"))
        async with Cards(config=config, skport=sdk) as cards:
            results = await cards.render_compare(
                first,
                second,
                context=contexts[0],
                second_context=contexts[1],
                variant=arguments.variant,
                art=artworks[0],
                second_art=artworks[1],
                details=arguments.details,
                output=OutputConfig(format=arguments.format, quality=arguments.quality),
            )
        if not results or (not arguments.details and len(results) != 1):
            raise ValueError("Comparison review requires one concise image unless --details is explicit")
        extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[arguments.format]
        destination = results[0].save(output / f"compare-{arguments.variant}.{extension}")
        extra = [
            str(result.save(output / "details" / f"compare-{arguments.variant}-{index:02}.{extension}"))
            for index, result in enumerate(results[1:], start=2)
        ]
        report.update(
            {
                "variant": arguments.variant,
                "display_timezone": arguments.timezone,
                "first_custom_art": artworks[0] is not None,
                "second_custom_art": artworks[1] is not None,
                "details": arguments.details,
                "images": len(results),
                "width": results[0].width,
                "height": results[0].height,
                "bytes": len(results[0].data),
                "image": str(destination),
                "detail_images": extra,
                "issues": sorted(
                    {issue.code for result in results for issue in result.issues}
                    | {code for model_report in reports for code in model_report["issues"]}
                ),
            }
        )
        (output / f"compare-{arguments.variant}.report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(json.dumps(report, indent=2, ensure_ascii=True))
        return report
    finally:
        if sdk is not None:
            await sdk.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        raise SystemExit(f"Comparison review failed: {type(exc).__name__}") from None
