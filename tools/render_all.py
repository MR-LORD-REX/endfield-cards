"""Render every implemented numeric template to a PNG gallery without JSON exports."""

from __future__ import annotations

import argparse
import asyncio
import io
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from time import perf_counter
from typing import Any

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT.parent / "skport-py/src")]

from render_live_roster import load_account_token, verify_owner_roster  # noqa: E402
from skport import ClientConfig, ImageSource, SkportClient  # noqa: E402
from skport.assets.images import enka_item_image  # noqa: E402
from skport.games.endfield.clean.common import image_links, timestamp  # noqa: E402
from skport.games.endfield.models import (  # noqa: E402
    ImageLinks,
    ItemSummary,
    PlayerIdentity,
    PullHistory,
    PullRecord,
    PullTotals,
)

from endfield_cards import CacheConfig, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.adapters.skport import context_for  # noqa: E402
from endfield_cards.assets.fonts import FontManager  # noqa: E402
from endfield_cards.client import TEMPLATES, _style  # noqa: E402
from endfield_cards.models import CardResult  # noqa: E402
from endfield_cards.rendering import RenderEngine  # noqa: E402

FAMILIES = {
    "all_characters": "roster",
    "live": "activity",
    "monument_detailed": "monument_detail",
    "contingency_contract_detailed": "contingency_contract_detail",
}
IMPLEMENTED = tuple(name for name in TEMPLATES if name != "wiki")
FIXTURE = ROOT.parent / "akef-cards/tests/data/pulls.json"
FIXTURE_LABEL = "REFERENCE FIXTURE / AKEF PULLS SAMPLE"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--skport-id", default="2348675939926")
    result.add_argument("--character-name", default="Zhuang Fangyi")
    result.add_argument("--compare-skport-id", help="Compare against this target; default is the token owner")
    result.add_argument("--env-file", type=Path, default=ROOT / ".env")
    result.add_argument("--token-file", type=Path)
    result.add_argument("--role", help="Explicit authenticated owner role for the complete roster")
    result.add_argument("--assets-dir", type=Path, default=ROOT / ".sk_assets")
    result.add_argument("--output-dir", type=Path, default=ROOT / "local")
    result.add_argument("--family", choices=("all", *IMPLEMENTED), default="all")
    return result


def fixture_history(path: Path, weapon_icons: dict[str, ImageLinks]) -> PullHistory:
    """Normalize six genuine character draws and three weapon draws from the reference."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    chars = [
        record
        for group in raw["chars"].values()
        for record in group
        if record.get("kind") == "draw" and record.get("charId")
    ]
    weapons = [record for record in raw["weapons"] if record.get("kind") == "draw" and record.get("weaponId")]

    def newest(row: dict[str, Any]) -> int:
        return int(row.get("gachaTs") or 0)

    sample = sorted(chars, key=newest, reverse=True)[:6]
    sample.extend(sorted(weapons, key=newest, reverse=True)[:3])
    records = []
    for row in sorted(sample, key=newest, reverse=True):
        item_id = row.get("charId") or row["weaponId"]
        icon = (
            image_links(enka=f"charremoteicon/icon_{item_id}.png", preferred=ImageSource.ENKA)
            if row.get("charId")
            else weapon_icons.get(item_id, ImageLinks())
        )
        records.append(
            PullRecord(
                id=f"{row['poolId']}:{row['seqId']}",
                sequence_id=str(row["seqId"]),
                kind=str(row.get("kind") or ""),
                item=ItemSummary(id=item_id, name=row["nameText"], rarity=row["rarity"], icon=icon),
                banner_id=row["poolId"],
                banner_name=row["poolName"],
                rarity=row["rarity"],
                pulled_at=timestamp(row["gachaTs"], milliseconds=True),
                is_free=bool(row.get("isFree", False)),
            )
        )
    observed = [record.pulled_at for record in records if record.pulled_at is not None]
    return PullHistory(
        player=PlayerIdentity(
            skport_id="reference-fixture", game_uid="REFERENCE FIXTURE", name="AKEF sample"
        ),
        records=records,
        totals=PullTotals(
            character_draws=sum(bool(row.get("charId")) for row in sample),
            weapon_draws=sum(bool(row.get("weaponId")) for row in sample),
            free_draws=sum(record.is_free for record in records),
            six_star_draws=sum(record.rarity == 6 for record in records),
        ),
        from_time=min(observed) if observed else None,
        to_time=max(observed) if observed else None,
        complete_history=False,
    )


def save_preview(pages: list[CardResult], destination: Path, *, fixture: bool = False) -> tuple[int, int]:
    """Preserve every returned page in a single numbered image, stacking when needed."""
    if not pages:
        raise ValueError("A card template returned no pages")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if len(pages) == 1 and not fixture:
        pages[0].save(destination)
        return pages[0].width, pages[0].height
    width = max(page.width for page in pages)
    label_height = 100 if fixture else 0
    gap = 20
    height = label_height + sum(page.height for page in pages) + gap * (len(pages) - 1)
    combined = Image.new("RGB", (width, height), (20, 24, 29))
    try:
        if fixture:
            draw = ImageDraw.Draw(combined)
            fonts = FontManager()
            draw.text((32, 18), FIXTURE_LABEL, font=fonts.get(30, weight="semibold"), fill="#f2d168")
            draw.text(
                (32, 58),
                "akef-cards/tests/data/pulls.json / 9 supplied records / sample totals only",
                font=fonts.get(20, weight="medium"),
                fill="#eeeeef",
            )
        y = label_height
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
        snapshot = sdk.assets.current
        weapon_icons = (
            {
                PurePosixPath(entry["Icon"]).stem: ImageLinks(
                    enka=enka_item_image(entry["Icon"]), preferred=ImageSource.ENKA
                )
                for entry in snapshot["weapons"].values()
                if entry.get("Icon")
            }
            if snapshot is not None
            else {}
        )
        models["pulls"] = fixture_history(FIXTURE, weapon_icons)
        print(
            f"Target live data: {profile.player.skport_id}; all_characters authenticated owner: {owner.player.skport_id}",
            flush=True,
        )
        print(
            f"Pulls: reference fixture {FIXTURE}; {len(models['pulls'].records)} observed sample records",
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
                    width, height = await asyncio.to_thread(
                        save_preview, pages, path, fixture=family == "pulls"
                    )
                    issues = sorted({issue.code for page in pages for issue in page.issues})
                    print(
                        f"Saved {public_family}/{template}.png: {width}x{height}, {len(pages)} page(s), {perf_counter() - started:.1f}s, issues={issues}",
                        flush=True,
                    )
                    count += 1
        print(f"Finished: {count} numbered PNGs; wiki templates remain unimplemented", flush=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        # Exception bodies can contain network inputs; print only the safe type/code.
        print(f"Render failed: {type(error).__name__} (code={getattr(error, 'code', None)})", flush=True)
        raise SystemExit(1) from None
