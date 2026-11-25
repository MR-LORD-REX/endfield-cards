"""Render every implemented numeric template to a PNG gallery without JSON exports."""

from __future__ import annotations

import argparse
import asyncio
import io
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT.parent / "skport-py/src")]

from render_live_roster import load_account_token, verify_owner_roster  # noqa: E402
from skport import ClientConfig, ImageSource, SkportClient  # noqa: E402

from endfield_cards import TEMPLATES, CacheConfig, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for  # noqa: E402
from endfield_cards.client import _style  # noqa: E402
from endfield_cards.models import CardResult  # noqa: E402
from endfield_cards.rendering import RenderEngine  # noqa: E402

FAMILIES = {
    "all_characters": "roster",
    "live": "activity",
    "monument_detailed": "monument_detail",
    "contingency_contract_detailed": "contingency_contract_detail",
}
IMPLEMENTED = tuple(name for name in TEMPLATES if name not in {"pulls", "wiki"})


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--skport-id", default="2348675939926")
    result.add_argument("--character-name", default="Zhuang Fangyi")
    result.add_argument("--compare-skport-id", help="Compare against this target; default is the token owner")
    result.add_argument("--env-file", type=Path, default=ROOT / ".env")
    result.add_argument("--token-file", type=Path)
    result.add_argument("--role", help="Explicit authenticated owner role for the complete roster")
    result.add_argument("--assets-dir", type=Path, default=ROOT / ".sk_assets")
    result.add_argument("--output-dir", type=Path, default=ROOT / "examples/output")
    result.add_argument("--family", choices=("all", *IMPLEMENTED), default="all")
    return result


def save_preview(pages: list[CardResult], destination: Path) -> tuple[int, int]:
    """Preserve every returned page in a single numbered image, stacking when needed."""
    if not pages:
        raise ValueError("A card template returned no pages")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if len(pages) == 1:
        pages[0].save(destination)
        return pages[0].width, pages[0].height
    width = max(page.width for page in pages)
    gap = 20
    height = sum(page.height for page in pages) + gap * (len(pages) - 1)
    combined = Image.new("RGB", (width, height), (20, 24, 29))
    try:
        y = 0
        for page in pages:
            with Image.open(io.BytesIO(page.data)) as decoded:
                combined.paste(decoded.convert("RGB"), ((width - decoded.width) // 2, y))
            y += page.height + gap
        combined.save(destination, format="PNG")
    finally:
        combined.close()
    return width, height


async def fetch(label: str, request: Any) -> Any:
    started = perf_counter()
    print(f"Fetching {label}...", flush=True)
    value = await asyncio.wait_for(request, timeout=180)
    print(f"Fetched {label} in {perf_counter() - started:.1f}s", flush=True)
    return value


async def main(argv: list[str] | None = None) -> None:
    args = parser().parse_args(argv)
    logging.getLogger("skport").setLevel(logging.CRITICAL)
    token = load_account_token(args)
    settings = ClientConfig(
        icon_source=ImageSource.ENKA,
        assets_dir=args.assets_dir,
        assets_offline=True,
        assets_auto_update=False,
        calculate_stats=True,
        cache=True,
        max_attempts=2,
        timeout=25,
    )
    output = args.output_dir.expanduser().resolve()
    selected = IMPLEMENTED if args.family == "all" else (args.family,)
    config = CardsConfig(
        cache=CacheConfig(directory=ROOT / ".cache/images"),
        output=OutputConfig(format="PNG"),
    )
    async with SkportClient(tokens=[token], config=settings) as sdk:
        await fetch("SKPort session", sdk.warm())
        await fetch("canonical assets", sdk.assets.ensure())
        profile = await fetch("target profile", sdk.endfield.card(skport_id=args.skport_id))
        owner = await fetch(
            "authenticated full owner roster", sdk.endfield.owned_card(token=token, role=args.role)
        )
        verify_owner_roster(owner)
        first = await fetch(
            f"target operator {args.character_name}",
            sdk.endfield.character(skport_id=args.skport_id, name=args.character_name, full=True),
        )
        compare_id = args.compare_skport_id or owner.player.skport_id
        if compare_id == owner.player.skport_id:
            request = sdk.endfield.owned_character(
                token=token, role=args.role, name=args.character_name, full=True
            )
        else:
            request = sdk.endfield.character(skport_id=compare_id, name=args.character_name, full=True)
        second = await fetch(f"comparison operator from {compare_id}", request)
        models = {"profile": profile, "character": first, "roster": owner}
        for family, method in (
            ("activity", "activity"),
            ("factory", "factory"),
            ("monument", "monument"),
            ("contingency_contract", "contract"),
        ):
            models[family] = await fetch(family, getattr(sdk.endfield, method)(skport_id=args.skport_id))
        models["exploration"] = models["factory"]
        models["monument_detail"] = models["monument"]
        models["contingency_contract_detail"] = models["contingency_contract"]
        print(
            f"Target live data: {profile.player.skport_id}; all_characters authenticated owner: {owner.player.skport_id}",
            flush=True,
        )
        print(
            f"Generating PNGs in {output}; fetched {datetime.now(UTC).isoformat()}; no JSON exports",
            flush=True,
        )
        count = 0
        async with RenderEngine(config=config) as renderer:
            for public_family in selected:
                family = FAMILIES.get(public_family, public_family)
                for template in TEMPLATES[public_family]:
                    started = perf_counter()
                    print(f"Rendering {public_family}/{template}.png...", flush=True)
                    variant = _style(public_family, template)
                    if public_family == "compare":
                        request = renderer.render_compare(
                            first, second, variant=variant, output=config.output, details=False
                        )
                    else:
                        model = models[family]
                        options: dict[str, Any] = {"details": False}
                        if family in {
                            "activity",
                            "factory",
                            "exploration",
                            "monument",
                            "monument_detail",
                            "contingency_contract",
                            "contingency_contract_detail",
                        }:
                            options["profile"] = profile
                        request = renderer.render(
                            family,
                            model,
                            variant=variant,
                            context=context_for(model),
                            output=config.output,
                            **options,
                        )
                    pages = await asyncio.wait_for(request, timeout=180)
                    path = output / public_family / f"{template}.png"
                    width, height = await asyncio.to_thread(save_preview, pages, path)
                    issues = sorted({issue.code for page in pages for issue in page.issues})
                    print(
                        f"Saved {public_family}/{template}.png: {width}x{height}, {len(pages)} page(s), {perf_counter() - started:.1f}s, issues={issues}",
                        flush=True,
                    )
                    count += 1
        print(f"Finished: {count} numbered PNGs; pulls and wiki templates remain unimplemented", flush=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        # Exception bodies can contain network inputs; print only the safe type/code.
        print(f"Render failed: {type(error).__name__} (code={getattr(error, 'code', None)})", flush=True)
        raise SystemExit(1) from None
