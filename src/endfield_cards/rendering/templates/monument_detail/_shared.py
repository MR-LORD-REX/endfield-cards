"""Concise Monument event boards with observed stage records and portrait teams."""

from __future__ import annotations

from collections.abc import Iterator
from math import ceil
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.templates.monument._shared import draw_art, draw_medal
from endfield_cards.utils.drawing import ELEMENT_COLORS, PageCanvas, element_key
from endfield_cards.utils.images import composite_fitted
from endfield_cards.utils.records import duration
from endfield_cards.utils.selection import default_monument_event_index, observed_stage_clear
from endfield_cards.utils.time import display_time

WIDTH = 1600
PAD = 36
GAP = 20
STAGE_HEIGHT = 346
PER_PAGE = 6
HARD = "#DA786A"


def text(c: PageCanvas, x: int, y: int, value: object, width: int, **options: Any) -> None:
    c.text(x, y, value, width=width, max_lines=options.pop("max_lines", 1), **options)


def _events(model: Any, event_id: str | None = None) -> list[Any]:
    entries = list(model.events) if hasattr(model, "events") else [model]
    identifiers = [event.id for event in entries if event.id]
    if len(set(identifiers)) != len(identifiers):
        raise DataValidationError("Monument contains duplicate event identities", code="duplicate_event")
    if event_id is not None:
        entries = [event for event in entries if event.id == str(event_id)]
        if not entries:
            raise DataValidationError(
                "Selected Monument event is absent from this snapshot", code="event_not_found"
            )
    elif entries:
        selected = default_monument_event_index(entries)
        entries = [entries[selected]] if selected is not None else []
    for event in entries:
        identifiers = [stage.id for stage in event.stages if stage.id]
        if len(set(identifiers)) != len(identifiers):
            raise DataValidationError("Monument contains duplicate stage identities", code="duplicate_stage")
    return entries


def urls(model: Any) -> set[str]:
    links = []
    for event in _events(model):
        links.append(image_url(event.poster))
        if event.medal is not None:
            links.append(image_url(event.medal.icon))
        for stage in event.stages:
            links.extend(image_url(enemy.icon) for enemy in stage.enemies)
            for run in (stage.normal, stage.hard):
                if run is not None:
                    for member in run.team:
                        links.extend(image_url(getattr(member.images, key)) for key in ("portrait", "avatar"))
                        links.extend((image_url(member.element.icons), image_url(member.profession.icons)))
    return {link for link in links if link}


def cleared(stage: Any, difficulty: str) -> bool | None:
    """Defaults are unknown; an explicit stage flag or completed run is observed."""
    return observed_stage_clear(stage, difficulty)


def clear_count(event: Any, difficulty: str) -> str:
    states = [cleared(stage, difficulty) for stage in event.stages]
    known = sum(state is not None for state in states)
    count = sum(state is True for state in states)
    return f"{count}/{len(states)}" + (f" · {len(states) - known} unknown" if known < len(states) else "")


def selected_run(stage: Any) -> tuple[str, Any]:
    for difficulty in ("hard", "normal"):
        run = getattr(stage, difficulty)
        if run is not None and cleared(stage, difficulty) is True:
            return difficulty, run
    for difficulty in ("normal", "hard"):
        if (run := getattr(stage, difficulty)) is not None:
            return difficulty, run
    return "normal", None


def draw_header(c: PageCanvas, profile: Any = None) -> None:
    c.icon("player.monument", PAD, 26, 31, tint=c.accent if c.dark else "#946B00")
    text(c, PAD + 45, 24, "ENDFIELD / MONUMENT", 850, size=20, bold=True)
    text(c, 1210, 28, "EVENT · STAGE RECORDS", 350, size=15, fill=c.muted)
    source = image_url(profile.avatar) if profile is not None else None
    pixels = c.assets.get(source) if source else None
    c.draw.ellipse((PAD, 68, PAD + 58, 126), fill=c.accent)
    if pixels is not None:
        composite_fitted(c.image, pixels, (PAD + 3, 71, PAD + 55, 123), shape="circle")
    else:
        c.centered_text(
            (PAD + 4, 72, PAD + 54, 120), c.context.owner.name[:1], size=25, bold=True, fill="#171C24"
        )
    text(c, PAD + 75, 62, c.context.owner.name, 920, size=32, bold=True)
    identity = f"UID {c.context.owner.game_uid}"
    if profile is not None and profile.server_name:
        identity += " · " + profile.server_name
    if profile is not None and "authority_level" in profile.model_fields_set:
        identity += f" · Authority {profile.authority_level}"
    text(c, PAD + 77, 101, identity, 1000, size=16, fill=c.muted)


def draw_banner(c: PageCanvas, event: Any, *, dark: bool) -> None:
    if dark:
        draw_art(c, event, (PAD, 151, 680, 387), clipped=True)
        c.panel((700, 151, WIDTH - PAD, 387))
        tx, ty, tw = 728, 175, 665
        c.icon("player.monument-detailed", 727, 175, 34, preserve_color=True)
        text(c, 775, 179, "MONUMENT EVENT", 450, size=15, fill=c.muted, bold=True)
        text(c, tx, ty + 52, event.name or "Unnamed event", tw, size=42, bold=True)
        text(c, tx, ty + 117, "Normal " + clear_count(event, "normal"), tw - 105, size=19)
        text(c, tx, ty + 151, "Hard " + clear_count(event, "hard"), tw - 105, size=19, fill=HARD)
        draw_medal(c, event, (1444, 265, 1540, 367))
    else:
        draw_art(c, event, (PAD, 151, WIDTH - PAD, 387))
        c.scrim((PAD, 273, WIDTH - PAD, 387), alpha=219)
        text(c, PAD + 24, 279, event.name or "Unnamed event", 1230, size=42, fill="#FFFFFF", bold=True)
        text(
            c,
            PAD + 26,
            337,
            f"Normal {clear_count(event, 'normal')}   ·   Hard {clear_count(event, 'hard')}",
            1210,
            size=19,
            fill="#E5E8EE",
        )
        draw_medal(c, event, (1444, 265, 1540, 367))
    hard = sum(cleared(stage, "hard") is True for stage in event.stages)
    if event.is_active or hard:
        label = "ACTIVE" if event.is_active else f"HARD {hard}/{len(event.stages)}"
        c.draw.rounded_rectangle(
            (PAD + 18, 170, PAD + 128, 201), radius=7, fill=c.accent if event.is_active else HARD
        )
        text(
            c, PAD + 30, 175, label, 88, size=14, bold=True, fill="#171C24" if event.is_active else "#FFFFFF"
        )


def draw_rules(c: PageCanvas, event: Any) -> int:
    y = 409
    if event.ends_at is not None or event.starts_at is not None:
        c.icon("player.activity", PAD, y + 1, 22, tint=c.muted)
        label = (
            ("Ends " + display_time(event.ends_at, c.context))
            if event.ends_at
            else "Starts " + display_time(event.starts_at, c.context)
        )
        text(c, PAD + 32, y, label, WIDTH - PAD * 2 - 32, size=15, fill=c.muted)
        y += 31
    if event.rules:
        c.icon("player.monument-detailed", PAD, y + 1, 23, preserve_color=True)
        text(c, PAD + 34, y, "RULES", 90, size=14, bold=True, fill=c.muted)
        text(
            c,
            PAD + 129,
            y,
            compact_rules(event.rules),
            WIDTH - PAD * 2 - 135,
            size=17,
            max_lines=2,
            fill=c.muted,
        )
        y += 55
    return y + 20


def compact_rules(rules: list[str]) -> str:
    """Choose two source mechanics and bound text before costly glyph measurement."""
    mechanics = [rule for rule in rules if rule.lstrip().startswith(("-", "•"))]
    selected = (mechanics or rules)[:2]
    snippets = []
    for rule in selected:
        plain = " ".join(rule.lstrip("-• \t\n")[:180].split())
        if len(rule.lstrip("-• \t\n")) > 180:
            plain += "…"
        snippets.append(plain)
    if len(rules) > len(selected):
        snippets.append(f"+{len(rules) - len(selected)} more")
    return " · ".join(snippets)


def draw_member(c: PageCanvas, member: Any, box: tuple[int, int, int, int]) -> None:
    x, y, right, bottom = box
    color = ELEMENT_COLORS.get(element_key(member), "#9CA6B5") if member is not None else c.line
    c.draw.rounded_rectangle(box, radius=10, fill="#252C36")
    if member is None:
        c.centered_text((x, y, right, bottom), "—", size=27, fill="#AAB3BF")
        return
    pixels = None
    for links in (member.images.portrait, member.images.avatar):
        source = image_url(links)
        if source and (pixels := c.assets.get(source)) is not None:
            break
    if pixels is not None:
        composite_fitted(c.image, pixels, box, radius=10, focus=member.images.focal_point or (0.5, 0.2))
    else:
        c.centered_text((x, y + 28, right, bottom - 40), member.name[:1] or "?", size=40, fill=color)
    c.scrim((x, bottom - 48, right, bottom), alpha=224)
    text(
        c,
        x + 8,
        bottom - 43,
        member.name or member.character_id or "Unknown operator",
        right - x - 16,
        size=17,
        bold=True,
        fill="#F6F7F9",
    )
    progression = [f"Lv {member.level}" if member.level is not None else "Lv —"]
    if member.evolution is not None:
        progression.append(f"E{member.evolution}")
    if member.potential is not None:
        progression.append(f"P{member.potential}")
    text(c, x + 9, bottom - 21, " · ".join(progression), right - x - 18, size=12, fill="#CDD3DC")
    c.draw.line((x + 3, bottom - 2, right - 3, bottom - 2), fill=color, width=4)
    if member.element.key or image_url(member.element.icons):
        c.draw.ellipse((x + 5, y + 5, x + 30, y + 30), fill=color)
        local = c.icon(f"element.{element_key(member)}", x + 9, y + 9, 17, tint="#FFFFFF")
        if not local and (source := image_url(member.element.icons)):
            c.icon(source, x + 9, y + 9, 17, tint="#FFFFFF")
    if member.profession.key or image_url(member.profession.icons):
        c.draw.rounded_rectangle((right - 31, y + 5, right - 5, y + 31), radius=5, fill="#1A202B")
        local = c.icon(f"profession.{member.profession.key}", right - 27, y + 9, 18, tint="#E8EDF4")
        if not local and (source := image_url(member.profession.icons)):
            c.icon(source, right - 27, y + 9, 18, tint="#E8EDF4")


def draw_record(c: PageCanvas, stage: Any, difficulty: str, x: int, y: int, width: int) -> None:
    state, run = cleared(stage, difficulty), getattr(stage, difficulty)
    color = HARD if difficulty == "hard" else c.fg
    label = "Hard" if difficulty == "hard" else "Normal"
    c.icon(
        "player.monument-detailed" if difficulty == "hard" else "player.monument",
        x,
        y,
        22,
        tint=None if difficulty == "hard" else color,
        preserve_color=difficulty == "hard",
    )
    text(c, x + 30, y, label.upper(), 100, size=14, fill=color, bold=True)
    status = "Cleared" if state is True else "Not cleared" if state is False else "Unknown"
    text(c, x + 138, y - 1, status, 130, size=15, fill=color if state else c.muted)
    timing = duration(run.duration_seconds) if run is not None and run.duration_seconds is not None else "—"
    text(c, x + width - 119, y - 2, timing, 118, size=20, bold=True, fill=color if state else c.muted)


def team_signature(run: Any) -> tuple[tuple[Any, ...], ...]:
    return tuple(
        (
            member.character_id or member.name,
            member.template_id,
            member.level,
            member.evolution,
            member.potential,
            member.rarity,
        )
        for member in run.team
    )


def draw_stage(c: PageCanvas, stage: Any, index: int, box: tuple[int, int, int, int]) -> None:
    x, y, right, bottom = box
    width = right - x
    hard_clear = cleared(stage, "hard") is True
    c.draw.rounded_rectangle(
        box, radius=13, fill=c.panel_color, outline=HARD if hard_clear else c.line, width=2
    )
    c.draw.rounded_rectangle((x + 17, y + 16, x + 73, y + 72), radius=9, fill="#2B333E")
    enemy = stage.enemies[0] if stage.enemies else None
    source = image_url(enemy.icon) if enemy is not None else None
    pixels = c.assets.get(source) if source else None
    if pixels is not None:
        composite_fitted(c.image, pixels, (x + 20, y + 19, x + 70, y + 69), contain=True, radius=8)
    else:
        c.icon("player.monument-detailed", x + 28, y + 27, 34, preserve_color=True)
    text(
        c,
        x + 89,
        y + 16,
        f"{index:02d}  {stage.name or stage.id or 'Unnamed stage'}",
        width - 120,
        size=22,
        bold=True,
    )
    level = (
        f"Recommended Lv {stage.recommended_level}"
        if stage.recommended_level is not None
        else "Recommended Lv —"
    )
    text(c, x + 91, y + 47, level, width - 125, size=14, fill=c.muted)
    c.draw.line((x + 18, y + 85, right - 18, y + 85), fill=c.line)
    draw_record(c, stage, "normal", x + 19, y + 98, width - 38)
    draw_record(c, stage, "hard", x + 19, y + 129, width - 38)
    difficulty, run = selected_run(stage)
    tag = ("HARD" if difficulty == "hard" else "NORMAL") + (
        " CLEAR TEAM" if cleared(stage, difficulty) is True else " RECORDED TEAM"
    )
    text(
        c,
        x + 20,
        y + 165,
        tag if run is not None else "TEAM NOT SUPPLIED",
        width - 40,
        size=13,
        bold=True,
        fill=HARD if difficulty == "hard" else c.muted,
    )
    team = run.team if run is not None else []
    team_width = (width - 40 - 30) // 4
    for position in range(4):
        tx = x + 20 + position * (team_width + 10)
        draw_member(
            c, team[position] if position < len(team) else None, (tx, y + 188, tx + team_width, y + 302)
        )
    alternate = getattr(stage, "normal" if difficulty == "hard" else "hard")
    if (
        alternate is not None
        and alternate.team
        and (run is None or team_signature(alternate) != team_signature(run))
    ):
        alt_label = "NORMAL" if difficulty == "hard" else "HARD"
        names = " · ".join(member.name or member.character_id for member in alternate.team)
        text(c, x + 20, y + 315, f"{alt_label} TEAM  {names}", width - 40, size=13, fill=c.muted)
    elif run is not None and run.completed_at is not None:
        date = display_time(run.completed_at, c.context)
        if alternate is not None and alternate.completed_at is not None:
            date = f"{difficulty.title()} {date} · {'Normal' if difficulty == 'hard' else 'Hard'} {display_time(alternate.completed_at, c.context)}"
        text(c, x + 20, y + 315, date, width - 40, size=13, fill=c.muted)
    elif len(team) > 4:
        text(c, x + 20, y + 315, f"+{len(team) - 4} other participants", width - 40, size=13, fill=c.muted)


def page_height(event: Any, count: int) -> int:
    top = (
        429
        + (31 if event.ends_at is not None or event.starts_at is not None else 0)
        + (55 if event.rules else 0)
    )
    return max(1100, top + max(1, ceil(count / 2)) * (STAGE_HEIGHT + GAP) - GAP + 86)


def render_page(
    event: Any,
    context: Any,
    stages: list[Any],
    *,
    offset: int = 0,
    variant: str = "light",
    assets: Any = None,
    profile: Any = None,
    page: int = 1,
    pages: int = 1,
) -> Image.Image:
    c = PageCanvas(
        "Monument detailed",
        context,
        dark=variant == "dark",
        size=(WIDTH, page_height(event, len(stages))),
        assets=assets,
        header=False,
    )
    draw_header(c, profile)
    draw_banner(c, event, dark=variant == "dark")
    top = draw_rules(c, event)
    if not stages:
        c.panel((PAD, top, WIDTH - PAD, top + 125))
        c.icon("player.monument-detailed", PAD + 23, top + 30, 40, preserve_color=True)
        text(c, PAD + 84, top + 35, "No stage records supplied", WIDTH - PAD * 2 - 110, size=23, fill=c.muted)
    width = (WIDTH - PAD * 2 - GAP) // 2
    for index, stage in enumerate(stages):
        row, column = divmod(index, 2)
        x, y = PAD + column * (width + GAP), top + row * (STAGE_HEIGHT + GAP)
        draw_stage(c, stage, offset + index + 1, (x, y, x + width, y + STAGE_HEIGHT))
    return c.finish(page=page, pages=pages)


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: dict | None = None,
    profile: Any = None,
    event_id: str | None = None,
    **options: Any,
) -> Iterator[Image.Image]:
    validate_owner(model, context)
    if profile is not None:
        validate_owner(profile, context)
    entries = _events(model, event_id)
    planned = [
        (event, offset, event.stages[offset : offset + PER_PAGE])
        for event in entries
        for offset in range(0, max(1, len(event.stages)), PER_PAGE)
    ]
    if not planned:
        c = PageCanvas(
            "Monument detailed",
            context,
            dark=variant == "dark",
            size=(WIDTH, 760),
            assets=assets,
            header=False,
        )
        draw_header(c, profile)
        c.panel((PAD, 161, WIDTH - PAD, 330))
        text(c, PAD + 26, 214, "No Monument events supplied", WIDTH - PAD * 2 - 52, size=29, fill=c.muted)
        yield c.finish()
        return
    for page, (event, offset, stages) in enumerate(planned, 1):
        yield render_page(
            event,
            context,
            stages,
            offset=offset,
            variant=variant,
            assets=assets,
            profile=profile,
            page=page,
            pages=len(planned),
        )


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
