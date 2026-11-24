"""Fetch an authenticated owner's roster and live state, then render concise cards."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import sys
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path[:0] = [str(ROOT / "src"), str(WORKSPACE / "skport-py/src")]

from render_profile import output_identity, token_from_file  # noqa: E402
from skport import ClientConfig, ImageSource, Language, SkportClient  # noqa: E402
from skport.games.endfield.clean.progress import build_live_status  # noqa: E402
from skport.games.endfield.models import LiveStatus, PlayerCard  # noqa: E402

from endfield_cards import CacheConfig, Cards, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for  # noqa: E402


def token_from_env_file(path: Path) -> str:
    """Read TOKEN as a literal dotenv value; never execute or expand the file."""
    content = path.expanduser().read_text(encoding="utf-8-sig")
    for line in content.splitlines():
        match = re.match(r"^\s*(?:export\s+)?TOKEN\s*=\s*(.*?)\s*$", line)
        if match is None:
            continue
        value = match.group(1)
        if value.startswith(("'", '"')):
            quote = value[0]
            end = value.find(quote, 1)
            if end < 0 or (value[end + 1 :].strip() and not value[end + 1 :].lstrip().startswith("#")):
                raise ValueError("The configured environment file has an invalid TOKEN value")
            value = value[1:end]
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
        if value and len(value) < 4096 and not any(character.isspace() for character in value):
            return value
        raise ValueError("The configured environment file has an invalid TOKEN value")
    raise ValueError("The configured environment file has no TOKEN value")


def load_account_token(arguments: argparse.Namespace) -> str:
    if arguments.token_file is not None:
        return token_from_file(arguments.token_file)
    if arguments.env_file != ROOT / ".env":
        return token_from_env_file(arguments.env_file)
    token = os.environ.get("TOKEN", "").strip()
    if token:
        if len(token) >= 4096 or any(character.isspace() for character in token):
            raise ValueError("TOKEN must be a nonempty account token")
        return token
    return token_from_env_file(arguments.env_file)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--family", choices=("live", "roster", "both"), default="both")
    result.add_argument("--variant", choices=("light", "dark"), default="light")
    result.add_argument("--env-file", type=Path, default=ROOT / ".env", help="Literal TOKEN dotenv file")
    result.add_argument("--token-file", type=Path, help="Explicit account token or ACCOUNT_TOKEN capture")
    result.add_argument("--role", help="Explicit role bound to the authenticated owner")
    result.add_argument("--roster-snapshot", type=Path, help="Previously fetched owner PlayerCard JSON")
    result.add_argument("--live-snapshot", type=Path, help="Previously fetched LiveStatus JSON")
    result.add_argument("--locale", choices=("en", "ja", "ko", "zh-Hans", "zh-Hant"))
    result.add_argument("--timezone", default="UTC")
    result.add_argument("--assets-dir", type=Path, help="Optional canonical SDK cache")
    result.add_argument("--format", choices=("JPEG", "PNG", "WEBP"), default="JPEG")
    result.add_argument("--quality", type=int, default=90)
    result.add_argument("--output-dir", type=Path, default=ROOT / "local/family-review")
    result.add_argument("--fetch-only", action="store_true", help="Save normalized snapshots without drawing")
    return result


def verify_owner_roster(model: PlayerCard) -> None:
    if model.source_scope != "owner":
        raise ValueError("All Characters requires an explicit owner roster snapshot")
    context_for(model)
    output_identity(model)
    for character in model.characters:
        if character.owner is not None and (
            character.owner.game_uid != model.player.game_uid
            or character.owner.skport_id != model.player.skport_id
        ):
            raise ValueError("A supplied roster character belongs to a different owner")


def model_report(model: PlayerCard | LiveStatus, source_mode: str, fetched_at: str | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_mode": source_mode,
        "fetched_at": fetched_at,
        "skport_id": model.player.skport_id,
        "game_uid": model.player.game_uid,
        "owner_name": model.player.name,
        "server_time": model.server_time.isoformat() if model.server_time else None,
    }
    if isinstance(model, PlayerCard):
        result.update(
            source_scope=model.source_scope,
            roster_complete=model.roster_complete,
            characters=len(model.characters),
            reported_owned_characters=model.counts.characters,
            weapons=sum(character.weapon is not None for character in model.characters),
            asset_revision=model.asset_revision,
            issues=sorted(
                {issue.code for issue in model.issues}
                | {issue.code for character in model.characters for issue in character.issues}
            ),
        )
    else:
        result["meters"] = [
            key
            for key in ("sanity", "daily", "weekly", "battle_pass", "credits")
            if getattr(model, key) is not None
        ]
    return result


async def main(argv: list[str] | None = None) -> dict[str, Any]:
    arguments = parser().parse_args(argv)
    logging.getLogger("skport").setLevel(logging.CRITICAL)
    selected = ("roster", "live") if arguments.family == "both" else (arguments.family,)
    models: dict[str, Any] = {}
    reports: dict[str, Any] = {}
    supplied = (*selected, "roster") if "roster" not in selected and arguments.roster_snapshot else selected
    for family in supplied:
        path = getattr(arguments, f"{family}_snapshot")
        if path is not None:
            model_type = PlayerCard if family == "roster" else LiveStatus
            model = model_type.model_validate_json(path.read_text(encoding="utf-8"))
            if isinstance(model, PlayerCard):
                verify_owner_roster(model)
            else:
                context_for(model)
            models[family] = model
            reports[family] = model_report(model, "saved-snapshot", None)
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
            # The owner snapshot contains all returned builds; no per-character
            # fanout is needed for this roster's progression and weapon display.
            response = await sdk.endfield.owned_card(token=token, role=arguments.role)
            if not isinstance(response, PlayerCard):
                raise TypeError("The SDK did not return a normalized owner PlayerCard")
            verify_owner_roster(response)
            fetched_at = datetime.now(UTC).isoformat()
            if "roster" not in models:
                models["roster"] = response
                reports["roster"] = model_report(response, "live-owner-api", fetched_at)
            if "live" in selected and "live" not in models:
                # LiveStatus is normalized from the explicit owner endpoint so
                # private activity data is not replaced by a public showcase.
                raw = await sdk.endfield.owned_card(token=token, role=arguments.role, raw=True)
                if not isinstance(raw, dict):
                    raise TypeError("The SDK did not return an owner live snapshot")
                live = build_live_status(raw, response.player, ImageSource.ENKA).model_copy(
                    update={"source_scope": "owner"}
                )
                models["live"] = live
                reports["live"] = model_report(live, "live-owner-api", datetime.now(UTC).isoformat())
        owners = {(model.player.skport_id, model.player.game_uid) for model in models.values()}
        servers = {model.player.server_id for model in models.values() if model.player.server_id is not None}
        if len(owners) != 1 or len(servers) > 1:
            raise ValueError("Live and roster snapshots must belong to the same owner")
        first = next(iter(models.values()))
        identity = output_identity(first)
        output = arguments.output_dir.expanduser().resolve() / identity
        output.mkdir(parents=True, exist_ok=True)
        for family, model in models.items():
            if reports[family]["source_mode"] == "live-owner-api":
                (output / f"{family}.json").write_text(model.model_dump_json(indent=2), encoding="utf-8")
        report: dict[str, Any] = {"sources": reports, "images": []}
        if not arguments.fetch_only:
            locale = arguments.locale or getattr(first, "locale", "en")
            config = CardsConfig(locale=locale, cache=CacheConfig(directory=ROOT / "local/image-cache"))
            async with Cards(config=config, skport=sdk) as cards:
                for family in selected:
                    model = models[family]
                    context = replace(context_for(model, locale=locale), display_timezone=arguments.timezone)
                    if family == "live" and "roster" in models:
                        context = replace(context, source_scope=models["roster"].source_scope)
                    if family == "live":
                        context = replace(context, display_timezone="UTC")
                    results = await cards.render(
                        "activity" if family == "live" else "roster",
                        model,
                        context=context,
                        variant=arguments.variant,
                        output=OutputConfig(format=arguments.format, quality=arguments.quality),
                        **({"profile": models["roster"]} if family == "live" and "roster" in models else {}),
                    )
                    if len(results) != 1:
                        raise ValueError("This family review requires one concise image per requested card")
                    extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[arguments.format]
                    destination = results[0].save(output / f"{family}-{arguments.variant}.{extension}")
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
                    (output / f"{family}-{arguments.variant}.report.json").write_text(
                        json.dumps({"source": reports[family], **entry}, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )
        (
            output
            / (
                "fetch-report.json"
                if arguments.fetch_only
                else f"{arguments.family}-{arguments.variant}.report.json"
            )
        ).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(report, indent=2, ensure_ascii=True))
        return report
    finally:
        if sdk is not None:
            await sdk.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        raise SystemExit(f"Live/roster review failed: {type(exc).__name__}") from None
