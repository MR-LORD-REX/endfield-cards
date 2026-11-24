"""Fetch and render one profile variant for an explicit SKPort target."""

from __future__ import annotations

import argparse
import asyncio
import getpass
import json
import logging
import os
import re
import sys
from dataclasses import replace
from datetime import UTC, datetime
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path[:0] = [str(ROOT / "src"), str(WORKSPACE / "skport-py/src")]

from skport import ClientConfig, ImageSource, SkportClient  # noqa: E402
from skport.games.endfield.models import PlayerCard  # noqa: E402

from endfield_cards import CacheConfig, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for  # noqa: E402
from endfield_cards.rendering import RenderEngine  # noqa: E402


def token_from_file(path: Path) -> str:
    """Read a configured token/capture; never include its contents in errors."""
    text = path.expanduser().read_text(encoding="utf-8").strip()
    match = re.search(r"(?im)^cookie:\s*(.+)$", text)
    if match:
        cookie = SimpleCookie()
        cookie.load(match.group(1))
        if "ACCOUNT_TOKEN" in cookie and cookie["ACCOUNT_TOKEN"].value:
            return cookie["ACCOUNT_TOKEN"].value
    try:
        document = json.loads(text)
    except json.JSONDecodeError:
        document = None
    if isinstance(document, dict):
        value = document.get("data", {}).get("content") if isinstance(document.get("data"), dict) else None
        if isinstance(value, str) and value.strip():
            return value.strip()
        raise ValueError("The configured token file has no account token")
    if text and not any(character.isspace() for character in text) and len(text) < 4096:
        return text
    raise ValueError("The configured token file has no account token")


def load_tokens(token_file: Path | None) -> list[str]:
    """Resolve explicit file/environment input before using a hidden terminal prompt."""
    if token_file is not None:
        return [token_from_file(token_file)]
    for key in ("SKPORT_TOKEN", "SKPORT_LIVE_TOKEN"):
        token = os.environ.get(key, "").strip()
        if token:
            return [token]
    raw = os.environ.get("SKPORT_TOKENS", "").strip()
    if raw:
        try:
            values = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError("SKPORT_TOKENS must contain a JSON list of account tokens") from None
        if (
            not isinstance(values, list)
            or not values
            or any(not isinstance(value, str) or not value.strip() for value in values)
        ):
            raise ValueError("SKPORT_TOKENS must contain a nonempty JSON list of account tokens")
        return [value.strip() for value in values]
    if not sys.stdin.isatty():
        raise ValueError("Live rendering requires SKPORT_TOKEN, SKPORT_TOKENS or an explicit --token-file")
    token = getpass.getpass("SKPort account token: ").strip()
    if not token:
        raise ValueError("An account token is required for a live profile request")
    return [token]


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--variant", choices=("overview", "operations", "identity"), default="overview")
    result.add_argument("--skport-id", help="Public SKPort target; required for a live API request")
    result.add_argument(
        "--snapshot", type=Path, help="Explicitly render a previously fetched PlayerCard JSON"
    )
    result.add_argument("--token-file", type=Path, help="Configured account token or ACCOUNT_TOKEN capture")
    result.add_argument("--locale", choices=("en", "ja", "ko", "zh-Hans", "zh-Hant"))
    result.add_argument(
        "--timezone", default="Asia/Kolkata", help="Timezone for the supplied snapshot timestamp"
    )
    result.add_argument("--format", choices=("JPEG", "PNG", "WEBP"), default="JPEG")
    result.add_argument("--quality", type=int, default=90)
    result.add_argument("--assets-dir", type=Path, help="Optional SDK canonical data cache")
    result.add_argument("--output-dir", type=Path, default=ROOT / "local/profile-review")
    return result


def output_identity(model: PlayerCard) -> str:
    """Keep user-supplied model IDs within one output-directory component."""
    identity = str(model.player.skport_id)
    if re.fullmatch(r"[A-Za-z0-9_-]{1,80}", identity) is None:
        raise ValueError("The profile social ID cannot be used as an output-directory name")
    return identity


async def main() -> None:
    arguments = parser().parse_args()
    logging.getLogger("skport").setLevel(logging.CRITICAL)
    if arguments.snapshot is None and not arguments.skport_id:
        raise ValueError("Supply --skport-id for a live request, or --snapshot for a saved model")
    fetched_at = None
    sdk: SkportClient | None = None
    mode = "saved-snapshot" if arguments.snapshot is not None else "live-api"
    try:
        if arguments.snapshot is not None:
            model = PlayerCard.model_validate_json(arguments.snapshot.read_text(encoding="utf-8"))
            if arguments.skport_id is not None and str(arguments.skport_id) != model.player.skport_id:
                raise ValueError("The requested target does not match the supplied snapshot")
        else:
            cached_assets = arguments.assets_dir or WORKSPACE / "skport-py/local/fixtures/enka-cache"
            sdk = SkportClient(
                tokens=load_tokens(arguments.token_file),
                config=ClientConfig(
                    lang=arguments.locale or "en",
                    icon_source=ImageSource.ENKA,
                    assets_dir=cached_assets,
                    assets_offline=cached_assets.exists(),
                    calculate_stats=False,
                    cache=False,
                    max_attempts=2,
                    timeout=25,
                ),
            )
            await sdk.warm()
            response = await sdk.endfield.card(skport_id=arguments.skport_id)
            if not isinstance(response, PlayerCard):
                raise TypeError("The SDK did not return a normalized PlayerCard")
            model = response
            fetched_at = datetime.now(UTC).isoformat()
            identity = output_identity(model)
            snapshots = ROOT / "local/profile-review"
            snapshots.mkdir(parents=True, exist_ok=True)
            (snapshots / f"profile-{identity}.json").write_text(
                model.model_dump_json(indent=2), encoding="utf-8"
            )
        locale = arguments.locale or model.locale
        context = replace(context_for(model, locale=locale), display_timezone=arguments.timezone)
        config = CardsConfig(locale=locale, cache=CacheConfig(directory=ROOT / "local/image-cache"))
        async with RenderEngine(config=config, skport=sdk) as cards:
            results = await cards.render_profile(
                model,
                context=context,
                variant=arguments.variant,
                output=OutputConfig(format=arguments.format, quality=arguments.quality),
            )
        if len(results) != 1:
            raise ValueError(
                "This review tool requires one concise profile image; use a public showcase snapshot"
            )
        output = arguments.output_dir.expanduser().resolve() / output_identity(model)
        output.mkdir(parents=True, exist_ok=True)
        extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[arguments.format]
        destination = results[0].save(output / f"profile-{arguments.variant}.{extension}")
        report: dict[str, Any] = {
            "source_mode": mode,
            "fetched_at": fetched_at,
            "skport_id": model.player.skport_id,
            "game_uid": model.player.game_uid,
            "name": model.player.name,
            "source_scope": model.source_scope,
            "snapshot_at": model.snapshot_at.isoformat() if model.snapshot_at else None,
            "variant": arguments.variant,
            "locale": locale,
            "display_timezone": arguments.timezone,
            "images": 1,
            "characters": len(model.characters),
            "medals": len(model.medals),
            "regions": len(model.regions),
            "bytes": len(results[0].data),
            "width": results[0].width,
            "height": results[0].height,
            "issues": sorted({issue.code for issue in results[0].issues}),
            "image": str(destination),
        }
        (output / f"profile-{arguments.variant}.report.json").write_text(
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
        raise SystemExit(f"Profile render failed: {type(exc).__name__}") from None
