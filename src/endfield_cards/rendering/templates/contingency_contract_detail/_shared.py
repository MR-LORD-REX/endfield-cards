"""Concise battle boards with source-backed teams, indicators and encounters."""

from __future__ import annotations

from collections.abc import Iterator
from math import ceil
from typing import Any

from PIL import Image, ImageDraw

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.templates.character.components import RARITY_COLORS
from endfield_cards.rendering.templates.contingency_contract import _shared as overview
from endfield_cards.utils.drawing import ELEMENT_COLORS, PageCanvas, art_url, element_key
from endfield_cards.utils.images import fitted, gradient_alpha, masked, shape_mask
from endfield_cards.utils.records import number
from endfield_cards.utils.time import display_time

WIDTH = 2000
PAD = 48
GAP = 24
RUNS_PER_PAGE = 4
INDICATORS_PER_BOARD = 42
Box = tuple[int, int, int, int]


def _selected(model: Any, contract_id: str | None = None) -> list[Any]:
    values = overview.contracts(model)
    if contract_id is not None:
        values = [item for item in values if item.id == str(contract_id)]
        if not values:
            raise DataValidationError(
                "Selected Contingency Contract is absent from this snapshot", code="contract_not_found"
            )
    return values[:1]


def ordered_runs(item: Any) -> list[Any]:
    """Rank observed scores first, with shorter known durations breaking ties."""
    return sorted(
        item.runs,
        key=lambda run: (
            run.score is None,
            -(run.score or 0),
            run.duration_seconds is None,
            run.duration_seconds if run.duration_seconds is not None else float("inf"),
        ),
    )


def _groups(item: Any, all_runs: bool) -> list[list[Any]]:
    runs = ordered_runs(item)
    if not all_runs:
        runs = runs[:RUNS_PER_PAGE]
    return [runs[start : start + RUNS_PER_PAGE] for start in range(0, len(runs), RUNS_PER_PAGE)] or [[]]


def urls(model: Any) -> set[str]:
    """Discover only images used on the default current-contract board."""
    links = []
    for item in _selected(model):
        links.append(image_url(item.poster))
        if item.medal is not None:
            links.append(image_url(item.medal.icon))
        links.extend(image_url(value.icon) for value in item.modifiers[:INDICATORS_PER_BOARD])
        links.extend(image_url(value.icon) for value in item.enemies[:8])
        for run in ordered_runs(item)[:RUNS_PER_PAGE]:
            links.extend(url for member in run.team[:4] for url in _portrait_urls(member))
            links.extend(image_url(member.element.icons) for member in run.team[:4] if not member.element.key)
            links.extend(
                image_url(member.profession.icons) for member in run.team[:4] if not member.profession.key
            )
    return {link for link in links if link}


def text(c: PageCanvas, x: int, y: int, value: object, width: int, *, size: int = 22, **options: Any) -> None:
    c.text(x, y, value, width=width, size=size, max_lines=options.pop("max_lines", 1), **options)


def _signal(c: PageCanvas) -> str:
    return c.accent if c.dark else "#946D00"


def _clock(value: float | None) -> str:
    if value is None:
        return "—"
    minutes, seconds = divmod(int(value), 60)
    return f"{minutes:02d}:{seconds:02d}"


def _portrait_urls(member: Any) -> tuple[str, ...]:
    """Use the preferred battle artwork, then its supplied avatar if unavailable."""
    return tuple(dict.fromkeys(url for url in (art_url(member), image_url(member.images.avatar)) if url))


def _meter(meter: Any) -> str:
    return " / ".join(
        number(getattr(meter, field)) if field in meter.model_fields_set else "—"
        for field in ("current", "maximum")
    )


def _header(c: PageCanvas, profile: Any = None) -> None:
    url = image_url(profile.avatar) if profile is not None else None
    source = c.assets.get(url) if url else None
    c.draw.ellipse((PAD, 32, PAD + 90, 122), fill=c.accent)
    if source is not None:
        tile = fitted(source, (82, 82), focus=(0.5, 0.3))
        face = masked(tile, shape_mask((82, 82), shape="circle"))
        c.image.alpha_composite(face, (PAD + 4, 36))
        face.close()
        tile.close()
    else:
        c.draw.ellipse((PAD + 4, 36, PAD + 86, 118), fill=c.panel_color)
        c.centered_text((PAD + 4, 40, PAD + 86, 112), c.context.owner.name[:1], size=44, bold=True)
    text(c, PAD + 116, 32, c.context.owner.name, 1110, size=46, bold=True)
    identity = f"UID {c.context.owner.game_uid}"
    if profile is not None:
        if profile.server_name:
            identity += " · " + profile.server_name
        if "authority_level" in profile.model_fields_set:
            identity += f" · Authority {profile.authority_level}"
    text(c, PAD + 118, 97, identity, 1110, size=21, fill=c.muted)
    c.icon("player.contingency-contract", WIDTH - 460, 47, 36, tint=_signal(c))
    text(c, WIDTH - 406, 50, "CONTRACT / BATTLE RECORDS", 360, size=22, bold=True)
    c.draw.line((PAD, 144, WIDTH - PAD, 144), fill=c.line)


def _banner(c: PageCanvas, item: Any) -> None:
    box = (PAD, 166, WIDTH - PAD, 410)
    overview.hero(c, item, box)
    name = item.name.removeprefix("Contingency Contract:").strip() or item.id or "Contract unavailable"
    text(c, PAD + 30, 185, name, 1560, size=47, bold=True, fill="#F4F5F7")
    stage = item.stage_name or "Stage unavailable"
    if item.stage_recommended_level is not None:
        stage += f" · Recommended Lv {item.stage_recommended_level}"
    text(c, PAD + 32, 289, stage, 1450, size=23, fill="#CDD3DC")
    values = [
        ("BEST SCORE", number(item.best_score) if "best_score" in item.model_fields_set else "—"),
        ("ATTEMPTS", number(item.attempts) if "attempts" in item.model_fields_set else "—"),
        *((meter.name.upper() or meter.key.upper(), _meter(meter)) for meter in item.missions[:3]),
    ]
    cell = min(302, 1520 // len(values))
    for index, (label, value) in enumerate(values):
        x = PAD + 32 + index * cell
        text(c, x, 333, label, cell - 16, size=15, fill="#BBC4CE", bold=True)
        if index == 0:
            c.icon("rarity.star", x, 366, 27, tint=c.accent)
        text(
            c,
            x + (36 if index == 0 else 0),
            359,
            value,
            cell - 45,
            size=35,
            bold=True,
            fill=c.accent if index == 0 else "#FFFFFF",
        )
    if item.medal is not None:
        url = image_url(item.medal.icon)
        source = c.assets.get(url) if url else None
        if source is not None:
            tile = fitted(source, (143, 143), contain=True)
            c.image.alpha_composite(tile, (WIDTH - PAD - 172, 207))
            tile.close()
        state = f"Medal Lv {item.medal.level}" if "level" in item.medal.model_fields_set else "Medal"
        if item.medal.plated:
            state += " · Plated"
        text(c, WIDTH - PAD - 194, 366, state, 170, size=16, fill="#CDD3DC")
    deadline = "Gameplay ends " + display_time(item.ends_at, c.context)
    deadline += " · Collection ends " + display_time(item.ends_at_collection, c.context)
    text(c, PAD, 427, deadline, WIDTH - PAD * 2, size=18, fill=c.muted)


def _semantic(c: PageCanvas, value: Any, prefix: str, x: int, y: int, size: int) -> None:
    if value.key and c.icon(
        f"{prefix}.{value.key}",
        x,
        y,
        size,
        tint=None if prefix == "element" else "#F4F5F7",
        preserve_color=prefix == "element",
    ):
        return
    key = image_url(value.icons)
    if key:
        c.icon(key, x, y, size, preserve_color=prefix == "element")


def _member(c: PageCanvas, member: Any, box: Box) -> None:
    x, y, right, bottom = box
    size = right - x, bottom - y
    color = ELEMENT_COLORS.get(element_key(member), "#586472")
    tile = Image.new("RGBA", size, color)
    source = None
    for url in _portrait_urls(member):
        source = c.assets.get(url)
        if source is not None:
            break
    if source is not None:
        portrait = fitted(source, size, focus=member.images.focal_point or (0.5, 0.12))
        tile.alpha_composite(portrait)
        portrait.close()
    else:
        d = ImageDraw.Draw(tile)
        d.ellipse((size[0] // 2 - 25, 52, size[0] // 2 + 25, 102), outline="#A5ADB8", width=2)
        d.arc((size[0] // 2 - 50, 87, size[0] // 2 + 50, 188), 185, 355, fill="#A5ADB8", width=2)
    shade = Image.new("RGBA", size, "#0D1218")
    shade.putalpha(gradient_alpha(size, start=0.33, end=1.0, maximum=246))
    tile.alpha_composite(shade)
    result = masked(tile, shape_mask(size, radius=11))
    c.image.alpha_composite(result, (x, y))
    result.close()
    shade.close()
    tile.close()
    for bx in (x + 10, x + 49):
        c.draw.ellipse((bx - 2, y + 9, bx + 31, y + 42), fill="#151A22")
    _semantic(c, member.element, "element", x + 10, y + 10, 30)
    _semantic(c, member.profession, "profession", x + 49, y + 10, 30)
    if member.potential is not None:
        if not c.icon(f"potential.{member.potential}", right - 41, y + 7, 36):
            text(c, right - 46, y + 10, f"P{member.potential}", 37, size=19, fill="#FFC800")
    text(
        c,
        x + 11,
        bottom - 67,
        member.name or member.character_id or "Operator unavailable",
        right - x - 22,
        size=23,
        bold=True,
        fill="#FFFFFF",
        max_lines=1,
    )
    bits = []
    if member.level is not None:
        bits.append(f"Lv {member.level}")
    if member.evolution is not None:
        bits.append(f"E{member.evolution}")
    text(
        c,
        x + 12,
        bottom - 35,
        " · ".join(bits) or "Level unavailable",
        right - x - 24,
        size=18,
        fill="#CCD2DC",
    )
    rarity = RARITY_COLORS.get(member.rarity, "#7C8794")
    c.draw.rounded_rectangle((x + 1, bottom - 5, right - 1, bottom), radius=2, fill=rarity)


def _battle(c: PageCanvas, run: Any, rank: int, box: Box) -> None:
    x, y, right, bottom = box
    c.panel(box)
    if rank == 1 and run.score is not None:
        c.draw.rounded_rectangle(box, radius=12, outline=c.accent if c.dark else "#DDB532", width=2)
    text(c, x + 20, y + 17, f"#{rank}", 74, size=33, bold=True, fill=_signal(c))
    c.icon("rarity.star", x + 87, y + 23, 29, tint=_signal(c))
    text(c, x + 128, y + 13, number(run.score), 207, size=43, bold=True, fill=_signal(c))
    c.icon("player.realtime", right - 286, y + 25, 23, tint=c.muted)
    timing = _clock(run.duration_seconds)
    if run.waves is not None:
        timing += f" · Wave {run.waves}"
    text(c, right - 247, y + 22, timing, 227, size=24, bold=True)
    state = (
        ("Cleared" if run.completed else "Failed")
        if "completed" in run.model_fields_set
        else "Result unavailable"
    )
    if run.completed_at is not None:
        state += " · " + display_time(run.completed_at, c.context)
    text(c, x + 22, y + 68, state, right - x - 44, size=17, fill=c.muted)
    if not run.team:
        c.draw.rounded_rectangle((x + 20, y + 111, right - 20, bottom - 20), radius=9, fill=c.background)
        c.centered_text((x + 35, y + 140, right - 35, bottom - 50), "Team unavailable", size=27, fill=c.muted)
        return
    gap = 12
    width = (right - x - 40 - gap * 3) // 4
    for index in range(4):
        px = x + 20 + index * (width + gap)
        tile = (px, y + 112, px + width, bottom - 20)
        if index < len(run.team):
            _member(c, run.team[index], tile)
        else:
            c.draw.rounded_rectangle(tile, radius=11, fill=c.background, outline=c.line)
    if len(run.team) > 4:
        text(c, right - 197, y + 69, f"+{len(run.team) - 4} operators", 175, size=15, fill=c.muted)


def _indicators(c: PageCanvas, item: Any, box: Box, *, large: bool) -> None:
    x, y, right, bottom = box
    c.panel(box)
    c.icon("player.contingency-contract", x + 19, y + 17, 27, tint=_signal(c))
    text(c, x + 59, y + 19, "INDICATORS", right - x - 80, size=22, bold=True)
    limit = INDICATORS_PER_BOARD if large else 8
    values = item.modifiers[:limit]
    observed = [value for value in item.modifiers if "is_unlocked" in value.model_fields_set]
    unlocked = sum(value.is_unlocked for value in observed)
    note = f"{len(item.modifiers)} supplied"
    if observed:
        note += f" · {unlocked} unlocked"
    text(c, x + 21, y + 52, note, right - x - 42, size=16, fill=c.muted)
    if not values:
        text(c, x + 22, y + 108, "Indicator data unavailable", right - x - 44, size=25, fill=c.muted)
        return
    columns = 6 if large else 4
    row_h = 76 if large else 70
    cell_w = (right - x - 32) // columns
    for index, value in enumerate(values):
        row, column = divmod(index, columns)
        px, py = x + 16 + column * cell_w, y + 84 + row * row_h
        url = image_url(value.icon)
        source = c.assets.get(url) if url else None
        # White game indicator glyphs need a dark surface in both themes.
        c.draw.rounded_rectangle((px, py, px + 45, py + 48), radius=8, fill="#242931")
        if source is not None:
            tile = fitted(source, (43, 43), contain=True)
            c.image.alpha_composite(tile, (px + 1, py + 3))
            tile.close()
        else:
            c.icon("player.contingency-contract", px + 4, py + 8, 31, tint="#D8DDE5")
        text(
            c,
            px + 53,
            py + 2,
            value.name or value.id or "Indicator",
            cell_w - 63,
            size=18,
            bold=True,
            max_lines=2,
        )
        bits = []
        if "score" in value.model_fields_set:
            bits.append(f"Score {value.score}")
        if "is_unlocked" in value.model_fields_set:
            bits.append("Unlocked" if value.is_unlocked else "Locked")
        text(c, px + 54, py + 49, " · ".join(bits) or "State unavailable", cell_w - 64, size=14, fill=c.muted)
    if len(item.modifiers) > len(values):
        text(
            c,
            x + 21,
            bottom - 24,
            f"+{len(item.modifiers) - len(values)} indicators in source data",
            right - x - 42,
            size=15,
            fill=c.muted,
        )


def _encounter(c: PageCanvas, item: Any, box: Box, *, wide: bool) -> None:
    x, y, right, bottom = box
    c.panel(box)
    c.icon("player.monument-detailed", x + 18, y + 14, 29, preserve_color=True)
    text(c, x + 59, y + 20, "ENCOUNTER", right - x - 80, size=22, bold=True)
    values = item.enemies[:8]
    if not values:
        text(c, x + 24, y + 85, "Enemy data unavailable", right - x - 48, size=24, fill=c.muted)
        return
    step = (right - x - 32) // len(values)
    size = min(84 if wide else 64, step - 9)
    for index, value in enumerate(values):
        px = x + 16 + index * step
        url = image_url(value.icon)
        source = c.assets.get(url) if url else None
        if source is not None:
            tile = fitted(source, (size, size), contain=True)
            c.image.alpha_composite(tile, (px + (step - size) // 2, y + 61))
            tile.close()
        else:
            c.icon("player.monument-detailed", px + (step - size) // 2, y + 61, size, preserve_color=True)
        text(
            c,
            px + 3,
            y + 69 + size,
            value.name or value.id or "Enemy",
            step - 6,
            size=18 if wide else 15,
            bold=True,
            max_lines=2,
        )
        if value.level is not None:
            text(c, px + 3, bottom - 30, f"Lv {value.level}", step - 6, size=15, fill=c.muted)
    if len(item.enemies) > len(values):
        text(
            c,
            right - 196,
            y + 24,
            f"+{len(item.enemies) - len(values)} in source",
            174,
            size=14,
            fill=c.muted,
        )


def _draw(
    item: Any,
    runs: list[Any],
    context: Any,
    *,
    dark: bool,
    assets: Any,
    profile: Any,
    page: int,
    pages: int,
    offset: int,
) -> Image.Image:
    rows = ceil(len(runs) / 2)
    indicator_rows = ceil(min(len(item.modifiers), INDICATORS_PER_BOARD) / 6)
    if runs:
        body_bottom = 505 + rows * 370 + max(0, rows - 1) * GAP
        height = body_bottom + 24 + 266 + 100
    else:
        grid_h = max(
            212, 105 + indicator_rows * 76 + (28 if len(item.modifiers) > INDICATORS_PER_BOARD else 0)
        )
        body_bottom = 504 + grid_h
        height = body_bottom + 24 + 218 + 100
    c = PageCanvas(
        "Contingency Contract detailed",
        context,
        dark=dark,
        size=(WIDTH, height),
        assets=assets,
        header=False,
    )
    _header(c, profile)
    _banner(c, item)
    if runs:
        text(c, PAD, 470, "BEST BATTLES", 385, size=24, bold=True)
        description = f"Best {len(runs)} of {len(item.runs)} by score · Shorter time breaks ties"
        if pages > 1:
            description = (
                f"Records {offset + 1}–{offset + len(runs)} of {len(item.runs)} · Ordered by score, then time"
            )
        text(c, PAD + 238, 475, description, WIDTH - PAD * 2 - 238, size=18, fill=c.muted)
        cell_w = (WIDTH - PAD * 2 - GAP) // 2
        for index, run in enumerate(runs):
            row, col = divmod(index, 2)
            x, y = PAD + col * (cell_w + GAP), 505 + row * (370 + GAP)
            _battle(c, run, offset + index + 1, (x, y, x + cell_w, y + 370))
        mid = WIDTH // 2
        _indicators(c, item, (PAD, body_bottom + 24, mid - 12, body_bottom + 290), large=False)
        _encounter(c, item, (mid + 12, body_bottom + 24, WIDTH - PAD, body_bottom + 290), wide=False)
    else:
        note = "No recorded battles" if "runs" in item.model_fields_set else "Battle records unavailable"
        text(c, PAD, 473, note, WIDTH - PAD * 2, size=23, fill=c.muted)
        _indicators(c, item, (PAD, 504, WIDTH - PAD, body_bottom), large=True)
        _encounter(c, item, (PAD, body_bottom + 24, WIDTH - PAD, body_bottom + 242), wide=True)
    if item.rules:
        preview = " ".join(item.rules[:240].split()) + ("…" if len(item.rules) > 240 else "")
        text(c, PAD + 4, height - 99, preview, WIDTH - PAD * 2 - 8, size=17, fill=c.muted)
    return c.finish(page, pages)


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: Any = None,
    profile: Any = None,
    contract_id: str | None = None,
    all_runs: bool = False,
    **options: Any,
) -> Iterator[Image.Image]:
    """Render the selected current contract; optional all_runs streams four battles per page."""
    selected = _selected(model, contract_id)
    validate_owner(model, context)
    if profile is not None:
        validate_owner(profile, context)
    if not selected:
        c = PageCanvas(
            "Contingency Contract detailed",
            context,
            dark=variant == "dark",
            size=(WIDTH, 790),
            assets=assets,
            header=False,
        )
        _header(c, profile)
        c.panel((PAD, 175, WIDTH - PAD, 650))
        c.icon("player.contingency-contract", WIDTH // 2 - 32, 265, 64, tint=_signal(c))
        c.centered_text(
            (PAD + 50, 383, WIDTH - PAD - 50, 453), "No Contingency Contract supplied", size=42, fill=c.muted
        )
        yield c.finish()
        return
    item = selected[0]
    groups = _groups(item, all_runs)
    for page, runs in enumerate(groups, 1):
        yield _draw(
            item,
            runs,
            context,
            dark=variant == "dark",
            assets=assets,
            profile=profile,
            page=page,
            pages=len(groups),
            offset=(page - 1) * RUNS_PER_PAGE,
        )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    """Collect the current-contract board or explicitly requested all-run pages."""
    return list(iter_render(model, context, **options))
