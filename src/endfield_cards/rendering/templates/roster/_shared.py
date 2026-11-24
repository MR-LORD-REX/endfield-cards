"""Source-backed roster components and planning for a concise full collection."""

from __future__ import annotations

import math
from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.templates.character import components as parts
from endfield_cards.utils.blending import element_colour
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import composite_fitted
from endfield_cards.utils.records import Record, iter_records, record_page_count

WIDTH = 2400
PAD = 36
GAP = 18
COLUMNS = 3
ROW_HEIGHT = 186
ROW_STEP = ROW_HEIGHT + 14
TOP = 254
PER_PAGE = 72
TILE_WIDTH = (WIDTH - PAD * 2 - GAP * (COLUMNS - 1)) // COLUMNS
SLOTS = tuple(parts.SLOT_NAMES)


def _characters(model: Any) -> list[Any]:
    return list(model.characters if hasattr(model, "characters") else model)


def selected_characters(model: Any, character_ids: Any = None) -> list[Any]:
    characters = _characters(model)
    if len({item.identity.skport_id for item in characters}) != len(characters):
        raise DataValidationError(
            "Roster contains duplicate character identities", code="duplicate_character"
        )
    if character_ids is not None:
        wanted = {str(value) for value in character_ids}
        characters = [
            item for item in characters if item.identity.skport_id in wanted or item.identity.str_id in wanted
        ]
    return characters


def page_groups(characters: list[Any]) -> list[list[Any]]:
    return [characters[index : index + PER_PAGE] for index in range(0, len(characters), PER_PAGE)] or [[]]


def page_size(count: int) -> tuple[int, int]:
    return WIDTH, max(650, TOP + max(1, math.ceil(count / COLUMNS)) * ROW_STEP + 91)


def portrait_url(model: Any) -> str | None:
    return image_url(model.images.avatar) or image_url(model.images.portrait)


def urls(model: Any) -> set[str]:
    result = {url for links in (getattr(model, "avatar", None),) if (url := image_url(links))}
    for character in _characters(model):
        links = [
            character.images.avatar,
            character.images.portrait,
            character.profession.icons,
            character.element.icons,
        ]
        links.extend(skill.icon for skill in character.skills[:4])
        links.extend(piece.icon for piece in character.equipment)
        if character.weapon is not None:
            links.append(character.weapon.images)
            if character.weapon.gem is not None:
                links.extend((character.weapon.gem.icon, character.weapon.gem.base_icon))
        result.update(url for item in links if (url := image_url(item)))
    return result


def text(c: PageCanvas, x: int, y: int, value: object, width: int, *, size: int = 20, **options: Any) -> None:
    c.text(x, y, value, width=width, size=size, max_lines=options.pop("max_lines", 1), **options)


def scope_caption(model: Any, context: Any, total: int, *, selected: bool = False) -> str:
    scope = (
        "Owned roster"
        if context.source_scope == "owner"
        else "Public showcase"
        if context.source_scope == "public"
        else "Supplied roster"
    )
    if selected:
        return scope + f" · {total} selected"
    caption = scope + f" · {total} characters"
    if getattr(model, "roster_complete", None) is True:
        caption += " · Complete"
    elif getattr(model, "roster_complete", None) is False:
        caption += " · Partial"
    return caption


def owner_meta(model: Any, context: Any) -> str:
    values = [f"UID {context.owner.game_uid}"]
    if getattr(model, "server_name", None):
        values.append(model.server_name)
    if "authority_level" in getattr(model, "model_fields_set", set()):
        values.append(f"Authority {model.authority_level}")
    return " · ".join(values)


def roster_counts(characters: list[Any]) -> list[tuple[str, str]]:
    capped = sum(item.level >= item.max_level for item in characters)
    skills = [skill for item in characters for skill in item.skills if skill.max_level > 0]
    skill_count = (
        f"{sum(skill.level >= skill.max_level for skill in skills)}/{len(skills)}" if skills else "—"
    )
    return [
        ("CHARACTERS", str(len(characters))),
        ("LEVEL CAPPED", str(capped)),
        ("SKILLS AT CAP", skill_count),
    ]


def draw_avatar(c: PageCanvas, model: Any, box: tuple[int, int, int, int], *, clipped: bool = False) -> None:
    x, y, right, bottom = box
    url = image_url(getattr(model, "avatar", None))
    source = c.assets.get(url) if url else None
    if clipped:
        c.draw.polygon(
            (
                (x - 4, y - 4),
                (right - 15, y - 4),
                (right + 4, y + 15),
                (right + 4, bottom + 4),
                (x - 4, bottom + 4),
            ),
            fill=c.accent,
        )
    else:
        c.draw.ellipse((x - 4, y - 4, right + 4, bottom + 4), fill=c.accent)
    if source is not None:
        composite_fitted(c.image, source, box, shape="clipped" if clipped else "circle", cut=18)
    else:
        c.draw.rectangle(box, fill=c.panel_color)
        text(c, x + 20, y + 20, c.context.owner.name[:1], right - x - 30, size=48, bold=True)


def draw_portrait(
    c: PageCanvas, model: Any, box: tuple[int, int, int, int], *, clipped: bool = False
) -> None:
    x, y, right, bottom = box
    url = portrait_url(model)
    source = c.assets.get(url) if url else None
    if source is not None:
        composite_fitted(
            c.image,
            source,
            box,
            shape="clipped" if clipped else "rounded",
            cut=18,
            radius=10,
            focus=(0.5, 0.21),
        )
    else:
        c.draw.rounded_rectangle(box, radius=10, fill="#313742")
        text(c, x + 12, y + 60, c.t("Unavailable"), right - x - 24, size=14, fill="#C1C6D0")
    rare = parts.RARITY_COLORS.get(model.rarity, c.muted)
    c.draw.line((x + 6, bottom - 3, right - 6, bottom - 3), fill=rare, width=4)
    c.draw.ellipse(
        (right - 26, bottom - 26, right + 2, bottom + 2),
        fill=element_colour(model),
        outline=c.panel_color,
        width=2,
    )
    element = image_url(model.element.icons)
    if element is None:
        stat = parts.ELEMENT_STAT.get(parts.element_key(model))
        element = f"stat.{stat}" if stat is not None else f"element.{model.element.key}"
    c.icon(element, right - 21, bottom - 21, 17, tint="#FFFFFF")


def draw_operator(c: PageCanvas, model: Any, x: int, y: int, width: int) -> None:
    text(c, x, y, model.name or model.identity.skport_id, width, size=26, bold=True)
    parts._stars(c, model.rarity, x + 1, y + 36, 12)
    badge_x = x + 119
    c.icon(
        image_url(model.profession.icons) or f"profession.{model.profession.key}",
        badge_x,
        y + 35,
        20,
        tint=c.muted,
    )
    text(
        c,
        badge_x + 27,
        y + 35,
        model.profession.name or model.profession.key,
        width - 146,
        size=14,
        fill=c.muted,
    )
    text(
        c,
        x,
        y + 65,
        f"Lv {model.level}/{model.max_level} · E{model.evolution} · P{model.potential}",
        width,
        size=20,
        bold=True,
    )
    bar_y = y + 95
    c.draw.rounded_rectangle((x, bar_y, x + width - 8, bar_y + 4), radius=2, fill=c.line)
    ratio = min(1.0, max(0.0, model.level / model.max_level)) if model.max_level else 0.0
    if ratio:
        c.draw.rounded_rectangle((x, bar_y, x + int((width - 8) * ratio), bar_y + 4), radius=2, fill=c.accent)


def draw_skills(c: PageCanvas, model: Any, x: int, y: int, width: int) -> None:
    skills = model.skills[:4]
    if not skills:
        text(c, x, y + 9, "Skills · " + c.t("Unavailable"), width, size=15, fill=c.muted)
    else:
        for index, skill in enumerate(skills):
            px = x + index * 66
            parts._item(c, skill.icon, (px, y, px + 24, y + 24))
            text(c, px + 29, y + 3, f"{skill.level}/{skill.max_level}", 36, size=13, bold=True)
    nodes = model.talents.nodes
    talent = (
        f"Talents {model.talents.unlocked_count}/{len(nodes)}" if nodes else "Talents · " + c.t("Unavailable")
    )
    if len(model.skills) > 4:
        talent += f" · +{len(model.skills) - 4} skills"
    text(c, x, y + 31, talent, width, size=14, fill=c.muted)


def draw_loadout(c: PageCanvas, model: Any, x: int, y: int, width: int) -> None:
    weapon = model.weapon
    if weapon is not None:
        parts._item(c, weapon.images, (x, y + 1, x + 46, y + 47), weapon.rarity)
        text(c, x + 57, y, weapon.name or weapon.id, width - 57, size=21, bold=True)
        text(
            c,
            x + 57,
            y + 30,
            f"Lv {weapon.level} · B{weapon.breakthrough} · R{weapon.refinement}",
            width - 57,
            size=15,
            fill=c.muted,
        )
        if weapon.gem is not None:
            gem = weapon.gem
            parts._essence_icon(c, gem, (x, y + 57, x + 21, y + 78))
            text(c, x + 30, y + 58, gem.name, width - 30, size=14, fill=c.accent if c.dark else "#916900")
        else:
            text(c, x, y + 59, "Essence · " + c.t("Unavailable"), width, size=14, fill=c.muted)
    else:
        text(c, x, y + 5, "Weapon · " + c.t("Unavailable"), width, size=19, fill=c.muted)
    equipment = {str(piece.slot): piece for piece in model.equipment}
    cell = width // 4
    for index, slot in enumerate(SLOTS):
        piece = equipment.get(slot)
        px, py = x + index * cell, y + 87
        text(c, px, py, parts.SLOT_NAMES[slot], cell - 6, size=11, fill=c.muted)
        if piece is None:
            c.draw.rounded_rectangle((px, py + 19, px + 35, py + 54), radius=7, outline=c.line)
            c.draw.line((px + 11, py + 36, px + 24, py + 36), fill=c.muted)
            text(c, px + 10, py + 59, "—", cell - 16, size=14, fill=c.muted)
        else:
            parts._item(c, piece.icon, (px, py + 19, px + 35, py + 54), piece.rarity)
            enhanced = str(piece.enhance_count) + (
                f"/{piece.max_enhance}" if piece.max_enhance is not None else ""
            )
            text(c, px, py + 59, enhanced, cell - 6, size=13, bold=True)


def details_records(characters: list[Any]) -> list[Record]:
    return [
        Record(
            "Character identity",
            [
                item.name or item.identity.skport_id,
                f"Character ID: {item.identity.skport_id}",
                item.profession.name or item.profession.key,
            ],
        )
        for item in characters
    ]


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: Any = None,
    details: bool = False,
    character_ids: Any = None,
    **options: Any,
) -> Iterator[Image.Image]:
    characters = selected_characters(model, character_ids)
    groups = page_groups(characters)
    records = details_records(characters) if details else []
    total = len(groups) + (record_page_count(context, records) if records else 0)
    if variant == "dark":
        from .dark import render_page
    else:
        from .light import render_page
    for page, group in enumerate(groups, 1):
        yield render_page(
            model,
            context,
            assets=assets,
            characters=group,
            all_characters=characters,
            selected=character_ids is not None,
            page=page,
            pages=total,
        )
    if records:
        yield from iter_records(
            "ROSTER DETAILS",
            context,
            records,
            variant=variant,
            assets=assets,
            page_offset=len(groups),
            total_pages=total,
        )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
