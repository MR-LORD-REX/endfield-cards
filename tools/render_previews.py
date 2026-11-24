"""Render one concise preview per style from the existing private SDK snapshots."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT.parent / "skport-py" / "src"))

from skport.games.endfield.models import CharacterBuild, PlayerCard  # noqa: E402

from endfield_cards import Artwork, CacheConfig, CardsConfig, OutputConfig  # noqa: E402
from endfield_cards.rendering import RenderEngine  # noqa: E402

_LEGACY_PREVIEW = re.compile(
    r"(?:character-(?:field|dossier|terminal|portrait)|profile-(?:overview|operations|identity))"
    r"-(?:\d{2}|review)\.jpg"
)


def clean_legacy_previews() -> int:
    """Remove only stale numbered/review exports inside the exact generated directory."""
    intended = (ROOT / "local" / "previews").absolute()
    if not intended.exists():
        return 0
    output = intended.resolve()
    if output != intended or not output.is_relative_to(ROOT.resolve()):
        raise RuntimeError("Generated preview directory resolves outside its intended location")
    removed = 0
    for candidate in output.iterdir():
        if not _LEGACY_PREVIEW.fullmatch(candidate.name):
            continue
        resolved = candidate.resolve()
        if resolved.parent != output or candidate.is_symlink() or not candidate.is_file():
            raise RuntimeError("Generated preview candidate resolves outside the intended directory")
        candidate.unlink()
        removed += 1
    return removed


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offline", action="store_true", help="Use local art and omit optional remote images"
    )
    parser.add_argument(
        "--all", action="store_true", help="Render one image for each profile and character style"
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Explicitly export optional appendices to local/detail-previews",
    )
    parser.add_argument(
        "--clean-legacy", action="store_true", help="Remove stale generated numbered/review previews and exit"
    )
    args = parser.parse_args()
    removed = clean_legacy_previews()
    if args.clean_legacy:
        print(json.dumps({"removed_legacy_previews": removed}))
        return
    source = ROOT / "design-data"
    if not source.exists():
        source = ROOT / "local" / "design-data"
    character = CharacterBuild.model_validate_json(
        (source / "character-1705883884575.json").read_text(encoding="utf-8")
    )
    profile = PlayerCard.model_validate_json(
        (source / "profile-1705883884575.json").read_text(encoding="utf-8")
    )
    output = ROOT / "local" / "previews"
    output.mkdir(parents=True, exist_ok=True)
    details_output = ROOT / "local" / "detail-previews"
    config = CardsConfig(cache=CacheConfig(directory=ROOT / "local" / "image-cache"))
    report = []
    async with RenderEngine(config=config, url_policy=(lambda url: False) if args.offline else None) as cards:
        art_path = source / "assets" / "zhuang-half-body.webp"
        artwork = Artwork(art_path, fit="contain") if art_path.exists() and args.offline else None
        for family, model in (("character", character), ("profile", profile)):
            styles = (
                cards.variants[family]
                if args.all
                else (("field",) if family == "character" else ("overview",))
            )
            for variant in styles:
                start = perf_counter()
                kwargs = {
                    "variant": variant,
                    "details": args.details,
                    "output": OutputConfig(format="JPEG", quality=90),
                }
                if family == "character":
                    kwargs["art"] = artwork
                pages = await cards.render(family, model, **kwargs)
                if not pages or (not args.details and len(pages) != 1):
                    raise RuntimeError(f"{family}/{variant} preview should produce exactly one concise image")
                destination = pages[0].save(output / f"{family}-{variant}.jpg")
                if args.details:
                    details_output.mkdir(parents=True, exist_ok=True)
                    for page in pages[1:]:
                        page.save(details_output / f"{family}-{variant}-{page.page:02d}.jpg")
                report.append(
                    {
                        "family": family,
                        "variant": variant,
                        "file": destination.name,
                        "images": 1,
                        "optional_detail_pages": len(pages) - 1 if args.details else 0,
                        "seconds": round(perf_counter() - start, 3),
                        "bytes": len(pages[0].data),
                        "issues": sorted({i.code for p in pages for i in p.issues}),
                    }
                )
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"removed_legacy_previews": removed, "previews": report}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
