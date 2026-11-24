"""Fetch Monument and Contingency Contract data through an injected SKPort client."""

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

from render_live_roster import load_account_token, verify_owner_roster  # noqa: E402
from render_profile import output_identity  # noqa: E402
from skport import ClientConfig, ImageSource, Language, SkportClient  # noqa: E402
from skport.games.endfield.clean.endgame import build_contract_report, build_monument_report  # noqa: E402
from skport.games.endfield.models import ContractState, MonumentState, PlayerCard  # noqa: E402

from endfield_cards import CacheConfig, Cards, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for  # noqa: E402

FAMILIES = ("monument", "contingency_contract")
FILENAMES = {"monument": "monument", "contingency_contract": "contingency-contract"}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--family", choices=(*FAMILIES, "both"), default="both")
    result.add_argument("--variant", choices=("light", "dark"), default="light")
    result.add_argument("--env-file", type=Path, default=ROOT / ".env")
    result.add_argument("--token-file", type=Path)
    result.add_argument("--role", help="Explicit role of the authenticated owner")
    result.add_argument("--monument-snapshot", type=Path)
    result.add_argument("--contract-snapshot", type=Path)
    result.add_argument("--profile-snapshot", type=Path, help="Verified PlayerCard for the owner header")
    result.add_argument("--locale", choices=("en", "ja", "ko", "zh-Hans", "zh-Hant"))
    result.add_argument("--assets-dir", type=Path)
    result.add_argument("--timezone", default="UTC")
    result.add_argument("--format", choices=("JPEG", "PNG", "WEBP"), default="JPEG")
    result.add_argument("--quality", type=int, default=90)
    result.add_argument("--output-dir", type=Path, default=ROOT / "local/family-review")
    result.add_argument("--fetch-only", action="store_true")
    return result


def verify_models(models: dict[str, Any]) -> None:
    owners = set()
    servers = set()
    for model in models.values():
        context_for(model)
        output_identity(model)
        owners.add((model.player.skport_id, model.player.game_uid))
        if model.player.server_id is not None:
            servers.add(model.player.server_id)
    if len(owners) != 1 or len(servers) > 1:
        raise ValueError("Endgame snapshots must have the same owner and server")


def model_report(model: Any, source_mode: str, fetched_at: str | None) -> dict[str, Any]:
    result = {
        "source_mode": source_mode,
        "fetched_at": fetched_at,
        "owner_name": model.player.name,
        "game_uid": model.player.game_uid,
        "skport_id": model.player.skport_id,
        "snapshot_at": model.snapshot_at.isoformat() if model.snapshot_at else None,
        "issues": sorted({issue.code for issue in model.issues}),
    }
    if isinstance(model, MonumentState):
        result["events"] = [
            {
                "index": index,
                "id": event.id,
                "name": event.name,
                "stages": [
                    {
                        "index": stage_index,
                        "id": stage.id,
                        "name": stage.name,
                        "normal_id": stage.normal_id,
                        "hard_id": stage.hard_id,
                    }
                    for stage_index, stage in enumerate(event.stages)
                ],
            }
            for index, event in enumerate(model.events)
        ]
    else:
        contracts = [model.current] if model.current is not None else []
        contracts.extend(
            item for item in model.contracts if all(item.id != existing.id for existing in contracts)
        )
        result["contracts"] = [
            {
                "index": index,
                "id": item.id,
                "name": item.name,
                "runs": len(item.runs),
                "modifiers": len(item.modifiers),
                "enemies": len(item.enemies),
                "missions": len(item.missions),
                "stage_id": getattr(item, "stage_id", None),
                "stage_name": getattr(item, "stage_name", None),
                "stage_recommended_level": getattr(item, "stage_recommended_level", None),
            }
            for index, item in enumerate(contracts)
        ]
    return result


async def fetch_model(sdk: SkportClient, family: str, profile: PlayerCard) -> MonumentState | ContractState:
    """Resolve the verified owner, read the SDK endpoint once, and normalize through the SDK."""
    target = await sdk.endfield.resolve(profile.player.skport_id, server_id=profile.player.server_id)
    if family == "monument":
        raw = await sdk.endfield.raw.indie_hard(target)
        return build_monument_report(raw, profile.player, ImageSource.ENKA, roster=profile.characters)
    raw = await sdk.endfield.raw.crisis_contract(target)
    return build_contract_report(raw, profile.player, ImageSource.ENKA, roster=profile.characters)


async def main(argv: list[str] | None = None) -> dict[str, Any]:
    arguments = parser().parse_args(argv)
    logging.getLogger("skport").setLevel(logging.CRITICAL)
    selected = FAMILIES if arguments.family == "both" else (arguments.family,)
    models: dict[str, Any] = {}
    reports: dict[str, Any] = {}
    profile = None
    if arguments.profile_snapshot is not None:
        profile = PlayerCard.model_validate_json(arguments.profile_snapshot.read_text(encoding="utf-8"))
        context_for(profile)
        output_identity(profile)
    for family in selected:
        path = arguments.monument_snapshot if family == "monument" else arguments.contract_snapshot
        if path is not None:
            cls = MonumentState if family == "monument" else ContractState
            models[family] = cls.model_validate_json(path.read_text(encoding="utf-8"))
            reports[family] = model_report(models[family], "saved-snapshot", None)
    if models:
        verify_models({**models, **({"profile": profile} if profile is not None else {})})
    sdk: SkportClient | None = None
    try:
        if any(family not in models for family in selected):
            token = load_account_token(arguments)
            sdk = SkportClient(
                tokens=[token],
                config=ClientConfig(
                    lang=Language(arguments.locale or "en"),
                    icon_source=ImageSource.ENKA,
                    assets_dir=arguments.assets_dir or WORKSPACE / "skport-py/local/fixtures/enka-cache",
                    assets_offline=False,
                    assets_auto_update=False,
                    calculate_stats=False,
                    cache=False,
                    max_attempts=2,
                    timeout=25,
                ),
            )
            await sdk.warm()
            response = await sdk.endfield.owned_card(token=token, role=arguments.role)
            if not isinstance(response, PlayerCard):
                raise TypeError("The SDK did not return a normalized owner PlayerCard")
            profile = response
            verify_owner_roster(profile)
            verify_models({**models, "profile": profile})
            target = profile.player.skport_id
            for family in selected:
                if family in models:
                    continue
                model = await fetch_model(sdk, family, profile)
                cls = MonumentState if family == "monument" else ContractState
                if not isinstance(model, cls):
                    raise TypeError("The SDK did not return a normalized endgame model")
                if model.player.game_uid != profile.player.game_uid or model.player.skport_id != target:
                    raise ValueError("Endgame response has a different owner")
                models[family] = model
                reports[family] = model_report(model, "live-sdk-api", datetime.now(UTC).isoformat())
        verify_models({**models, **({"profile": profile} if profile is not None else {})})
        first = next(iter(models.values()))
        output = arguments.output_dir.expanduser().resolve() / output_identity(first)
        output.mkdir(parents=True, exist_ok=True)
        report: dict[str, Any] = {"sources": reports, "images": []}
        for family, model in models.items():
            if reports[family]["source_mode"] == "live-sdk-api":
                (output / f"{FILENAMES[family]}.json").write_text(
                    model.model_dump_json(indent=2), encoding="utf-8"
                )
        if not arguments.fetch_only:
            config = CardsConfig(
                locale=arguments.locale or "en", cache=CacheConfig(directory=ROOT / "local/image-cache")
            )
            async with Cards(config=config, skport=sdk) as cards:
                for family in selected:
                    model = models[family]
                    context = replace(
                        context_for(model, locale=config.locale), display_timezone=arguments.timezone
                    )
                    results = await cards.render(
                        family,
                        model,
                        context=context,
                        variant=arguments.variant,
                        output=OutputConfig(format=arguments.format, quality=arguments.quality),
                        **({"profile": profile} if profile is not None else {}),
                    )
                    if len(results) != 1:
                        raise ValueError("This showcase review requires one image per requested card")
                    extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[arguments.format]
                    destination = results[0].save(
                        output / f"{FILENAMES[family]}-{arguments.variant}.{extension}"
                    )
                    entry = {
                        "family": family,
                        "variant": arguments.variant,
                        "image": str(destination),
                        "width": results[0].width,
                        "height": results[0].height,
                        "bytes": len(results[0].data),
                        "issues": sorted({issue.code for issue in results[0].issues}),
                    }
                    report["images"].append(entry)
                    (output / f"{FILENAMES[family]}-{arguments.variant}.report.json").write_text(
                        json.dumps({"source": reports[family], **entry}, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )
        (
            output
            / (
                "endgame-fetch.report.json"
                if arguments.fetch_only
                else f"endgame-{arguments.variant}.report.json"
            )
        ).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        summary = {
            family: {
                "owner": model.player.name,
                "skport_id": model.player.skport_id,
                "events": len(model.events) if isinstance(model, MonumentState) else None,
                "stages": sum(len(event.stages) for event in model.events)
                if isinstance(model, MonumentState)
                else None,
                "contracts": len(reports[family]["contracts"]) if isinstance(model, ContractState) else None,
                "issues": reports[family]["issues"],
            }
            for family, model in models.items()
        }
        print(json.dumps({"sources": summary, "images": report["images"]}, indent=2, ensure_ascii=True))
        return report
    finally:
        if sdk is not None:
            await sdk.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        raise SystemExit(f"Endgame review failed: {type(exc).__name__}") from None
