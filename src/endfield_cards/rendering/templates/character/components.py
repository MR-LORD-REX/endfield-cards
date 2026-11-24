"""Observed character data rendered in bounded AKEF-style component boxes."""

from __future__ import annotations

import math
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageOps
from skport.games.endfield.models import StatUnit, StatValue, format_percent

from endfield_cards.adapters.skport import image_url
from endfield_cards.utils.drawing import ELEMENT_COLORS, PageCanvas, element_key
from endfield_cards.utils.images import fitted, masked, shape_mask

RARITY_COLORS = {6: "#F18A43", 5: "#E7B947", 4: "#A17CDF", 3: "#68A4D6"}
CORE_IDS = (1, 2, 3, 39, 40, 41, 42)
STAT_NAMES = {
    1: "HP",
    2: "ATK",
    3: "DEF",
    9: "Crit Rate",
    10: "Crit DMG",
    17: "Basic ATK DMG",
    26: "Stagger DMG",
    28: "Ultimate DMG",
    29: "Treatment",
    30: "Healing Received",
    32: "Battle Skill DMG",
    33: "Combo Skill DMG",
    39: "STR",
    40: "AGI",
    41: "INT",
    42: "WILL",
    44: "Ult Gain",
    50: "Physical DMG",
    51: "Heat DMG",
    52: "Electric DMG",
    53: "Cryo DMG",
    54: "Nature DMG",
    55: "Ether DMG",
    61: "Staggered Target DMG",
    87: "Arts Intensity",
}
ELEMENT_STAT = {
    "physical": 50,
    "fire": 51,
    "heat": 51,
    "pulse": 52,
    "electric": 52,
    "cryst": 53,
    "cryo": 53,
    "natural": 54,
    "nature": 54,
    "ether": 55,
}
SLOT_NAMES = {"body": "Armor", "arms": "Gloves", "accessory1": "Kit 1", "accessory2": "Kit 2"}
Box = tuple[int, int, int, int]


def stats_rows(model: Any) -> list[StatValue]:
    """Select only supplied properties, with AKEF's six meaningful bonus slots."""
    if model.stats is None:
        return []
    values = model.stats.values
    own = ELEMENT_STAT.get(element_key(model))
    priority = [9, 10, 44, 30, own, 29, 87, 26, 17, 32, 33, 28, 50, 51, 52, 53, 54, 55, 61]
    bonuses = []
    for key in dict.fromkeys(priority):
        if key is None or key not in values:
            continue
        stat = values[key]
        if key not in {9, 10, 44, 30} and abs(stat.value) <= 1e-6:
            continue
        bonuses.append(stat)
        if len(bonuses) == 6:
            break
    return [values[key] for key in CORE_IDS if key in values] + bonuses


def display_value(stat: Any) -> str:
    """Retain declared units; comma-group only observed integral scalar values."""
    if stat.unit in {StatUnit.FLAT, StatUnit.NUMBER} and float(stat.value).is_integer():
        return f"{stat.value:,.0f}"
    return stat.display


def _text(
    c: PageCanvas,
    x: int,
    y: int,
    value: object,
    width: int,
    *,
    size: int = 20,
    bold: bool = False,
    muted: bool = False,
    lines: int = 1,
    color: str | None = None,
) -> None:
    c.text(
        x,
        y,
        value,
        size=max(12, size),
        bold=bold,
        fill=color or (c.muted if muted else c.fg),
        width=max(1, width),
        max_lines=lines,
    )


def _title(c: PageCanvas, box: Box, name: str) -> int:
    x, y, right, _ = box
    c.draw.rectangle((x + 12, y + 10, x + 16, y + 29), fill=c.accent)
    _text(c, x + 26, y + 5, c.t(name), right - x - 40, size=19, bold=True)
    return y + 34


def _stat_label(stat: Any) -> str:
    return STAT_NAMES.get(stat.id, stat.name)


def _role(model: Any, stat: Any) -> str:
    if stat.is_main or model.stats.main_attribute == stat.id:
        return "Main"
    if stat.is_sub or model.stats.sub_attribute == stat.id:
        return "Sub"
    return ""


def _role_tag(c: PageCanvas, x: int, y: int, role: str) -> None:
    c.draw.rounded_rectangle((x, y, x + 46, y + 18), radius=5, fill=c.accent if role == "Main" else "#303642")
    _text(c, x + 5, y, c.t(role), 38, size=12, bold=True, color="#171C24" if role == "Main" else "#F3F4F7")


def _stat_icon(c: PageCanvas, stat: Any, x: int, y: int, size: int, color: str | None = None) -> int:
    url = image_url(stat.icon)
    key = url or f"stat.{stat.id}"
    return size + 7 if c.icon(key, x, y, size, tint=color or c.muted) else 0


def _pips(
    c: PageCanvas,
    x: int,
    y: int,
    value: int,
    maximum: int,
    width: int,
    *,
    height: int = 5,
    color: str | None = None,
) -> None:
    """Bound the graphic; numeric source level/max remains separately visible."""
    if maximum <= 0 or width <= 0:
        return
    count = min(maximum, 18)
    gap = 3
    pip_width = max(2, (width - gap * (count - 1)) // count)
    filled = int(round(count * min(1.0, max(0.0, value / maximum))))
    for index in range(count):
        px = x + index * (pip_width + gap)
        c.draw.rounded_rectangle(
            (px, y, px + pip_width, y + height),
            radius=2,
            fill=(color or c.accent) if index < filled else c.line,
        )


def _stars(c: PageCanvas, rarity: int, x: int, y: int, size: int = 14) -> None:
    color = RARITY_COLORS.get(rarity, c.muted)
    for index in range(rarity):
        c.icon("rarity.star", x + index * (size + 3), y, size, tint=color)


def _source(c: PageCanvas, links: Any) -> Image.Image | None:
    url = image_url(links)
    return c.assets.get(url) if url else None


def _item(c: PageCanvas, links: Any, box: Box, rarity: int = 0) -> None:
    x, y, right, bottom = box
    width, height = right - x, bottom - y
    tile = Image.new("RGBA", (width, height), "#2D333D")
    draw = ImageDraw.Draw(tile)
    top = (45, 51, 61)
    rare = ImageColor.getrgb(RARITY_COLORS.get(rarity, "#697280"))
    low = tuple(int(a + (b - a) * 0.44) for a, b in zip(top, rare, strict=True))
    for yy in range(height):
        blend = (yy / max(1, height - 1)) ** 1.8
        draw.line(
            (0, yy, width, yy), fill=tuple(int(a + (b - a) * blend) for a, b in zip(top, low, strict=True))
        )
    source = _source(c, links)
    if source is not None:
        pixels = source.convert("RGBA")
        bounds = pixels.getchannel("A").point(lambda a: 255 if a > 16 else 0).getbbox()
        if bounds:
            pixels = pixels.crop(bounds)
        glyph = ImageOps.contain(pixels, (max(1, width - 10), max(1, height - 10)), Image.Resampling.LANCZOS)
        tile.alpha_composite(glyph, ((width - glyph.width) // 2, (height - glyph.height) // 2))
    c.image.alpha_composite(masked(tile, shape_mask(tile.size, radius=9)), (x, y))


def draw_stats(c: PageCanvas, model: Any, box: Box, *, layout: str = "rows", dense: bool = False) -> None:
    """Draw observed headline values, attributes and a bounded bonus summary."""
    x, y, right, bottom = box
    c.panel(box)
    top = _title(c, box, "Statistics")
    rows = stats_rows(model)
    if not rows:
        _text(c, x + 18, top + 18, c.t("Unavailable"), right - x - 36, muted=True)
        return
    values = model.stats.values
    width, body_height = right - x - 32, bottom - top - 14
    bonuses = [stat for stat in rows if stat.id not in CORE_IDS]
    if layout == "columns":
        major_h, attr_h = int(body_height * 0.29), int(body_height * 0.28)
        for index, key in enumerate((1, 2, 3)):
            px, cell = x + 16 + index * width // 3, width // 3 - 14
            stat = values.get(key)
            if stat is None:
                _text(c, px, top + 4, STAT_NAMES[key], cell, size=16, muted=True)
                _text(c, px, top + 27, "—", cell, size=42, bold=True)
                continue
            offset = _stat_icon(c, stat, px, top + 2, 20)
            _text(c, px + offset, top + 1, STAT_NAMES[key], cell - offset, size=16, muted=True)
            _text(c, px, top + 27, display_value(stat), cell, size=min(54, major_h - 30), bold=True)
        attribute_y = top + major_h
        peak = max((values[key].value for key in (39, 40, 41, 42) if key in values), default=1) or 1
        for index, key in enumerate((39, 40, 41, 42)):
            px, cell = x + 16 + index * width // 4, width // 4 - 12
            stat = values.get(key)
            if stat is None:
                continue
            role = _role(model, stat)
            color = c.accent if role == "Main" else c.fg if role == "Sub" else c.muted
            offset = _stat_icon(c, stat, px, attribute_y + 9, min(30, cell // 3), color)
            _text(c, px + offset, attribute_y, STAT_NAMES[key], cell - offset, size=15, color=color)
            _text(
                c,
                px + offset,
                attribute_y + 24,
                display_value(stat),
                cell - offset,
                size=min(35, attr_h - 47),
                bold=True,
            )
            if role:
                _role_tag(c, px + cell - 46, attribute_y - 1, role)
            bar_y = attribute_y + attr_h - 5
            c.draw.rectangle((px, bar_y, px + cell, bar_y + 3), fill=c.line)
            c.draw.rectangle(
                (px, bar_y, px + int(cell * min(1, max(0, stat.value / peak))), bar_y + 3), fill=color
            )
        extras_top = attribute_y + attr_h + 9
        step = max(24, (bottom - extras_top - 10) // max(1, math.ceil(len(bonuses) / 2)))
        for index, stat in enumerate(bonuses):
            row, col = divmod(index, 2)
            px, py = x + 16 + col * (width // 2 + 4), extras_top + row * step
            cell = width // 2 - 12
            offset = _stat_icon(c, stat, px, py + 2, 18)
            _text(c, px + offset, py, _stat_label(stat), int(cell * 0.68) - offset, size=17, muted=True)
            _text(c, px + int(cell * 0.70), py - 1, display_value(stat), int(cell * 0.30), size=20, bold=True)
            c.draw.line((px, py + step - 6, px + cell, py + step - 6), fill=c.line)
        return
    main_h = min(59, int(body_height * 0.31) // 3)
    for key in (1, 2, 3):
        stat = values.get(key)
        py = top + (key - 1) * main_h
        if stat is None:
            _text(c, x + 18, py + 10, STAT_NAMES[key], width, size=16, muted=True)
            _text(c, right - 62, py + 8, "—", 43, size=26, bold=True)
            continue
        offset = _stat_icon(c, stat, x + 17, py + 11, 20)
        _text(c, x + 17 + offset, py + 8, STAT_NAMES[key], width // 2 - offset, size=18, muted=True)
        _text(
            c,
            x + 16 + int(width * 0.49),
            py + 1,
            display_value(stat),
            int(width * 0.51),
            size=min(37, main_h - 12),
            bold=True,
        )
        c.draw.line((x + 17, py + main_h - 4, right - 17, py + main_h - 4), fill=c.line)
    attribute_top = top + 3 * main_h + 10
    attr_h = min(60, int(body_height * 0.26) // 2)
    for index, key in enumerate((39, 40, 41, 42)):
        stat = values.get(key)
        if stat is None:
            continue
        row, col = divmod(index, 2)
        px, py = x + 17 + col * (width // 2 + 4), attribute_top + row * attr_h
        cell = width // 2 - 10
        role = _role(model, stat)
        color = c.accent if role == "Main" else c.fg if role == "Sub" else c.muted
        offset = _stat_icon(c, stat, px, py + 6, 24, color)
        _text(c, px + offset, py + 1, STAT_NAMES[key], cell - offset, size=14, color=color)
        _text(c, px + offset, py + 22, display_value(stat), cell - offset, size=26, bold=True)
        if role:
            _role_tag(c, px + cell - 47, py, role)
    extras_top = attribute_top + 2 * attr_h + 7
    step = max(23, (bottom - extras_top - 12) // max(1, len(bonuses)))
    for index, stat in enumerate(bonuses):
        py = extras_top + index * step
        offset = _stat_icon(c, stat, x + 17, py + 1, 18)
        _text(
            c,
            x + 17 + offset,
            py,
            _stat_label(stat),
            int(width * 0.71) - offset,
            size=15 if dense else 17,
            muted=True,
        )
        _text(
            c,
            x + 17 + int(width * 0.72),
            py - 1,
            display_value(stat),
            int(width * 0.28) - 3,
            size=18 if dense else 20,
            bold=True,
        )


def draw_skills(c: PageCanvas, model: Any, box: Box, *, columns: int = 4) -> None:
    x, y, right, bottom = box
    c.panel(box)
    top = _title(c, box, "Skills")
    skills = model.skills[:4]
    if not skills:
        _text(c, x + 18, top + 8, c.t("Unavailable"), right - x - 36, muted=True)
        return
    columns = max(1, min(columns, len(skills)))
    rows = math.ceil(len(skills) / columns)
    row_height = (bottom - top - (rows - 1) * 7) // rows
    width = (right - x - 30) // columns
    for index, skill in enumerate(skills):
        row, column = divmod(index, columns)
        px = x + 15 + column * width
        skill_top = top + row * (row_height + 7)
        row_bottom = skill_top + row_height
        icon_size = min(42, row_height - 26)
        _item(c, skill.icon, (px, skill_top, px + icon_size, skill_top + icon_size), 0)
        # White skill glyphs sit on a slate surface in both light and dark layouts.
        _text(
            c,
            px + icon_size + 9,
            skill_top - 2,
            skill.name or skill.key,
            width - icon_size - 17,
            size=16,
            bold=True,
            lines=2,
        )
        _text(c, px, row_bottom - 25, f"{skill.level}/{skill.max_level}", icon_size + 7, size=14, bold=True)
        _pips(
            c,
            px + icon_size + 9,
            row_bottom - 15,
            skill.level,
            skill.max_level,
            width - icon_size - 17,
            height=5,
        )


def draw_talents(c: PageCanvas, model: Any, box: Box) -> None:
    x, y, right, bottom = box
    c.panel(box)
    top = _title(c, box, "Talents")
    nodes = model.talents.nodes
    _text(c, right - 90, y + 7, f"{model.talents.unlocked_count}/{len(nodes)}", 75, size=17, bold=True)
    if not nodes:
        _text(c, x + 18, top + 6, c.t("Unavailable"), right - x - 36, muted=True, size=16)
        return
    groups = [
        (kind, [node for node in nodes if node.kind == kind]) for kind in ("attribute", "combat", "base")
    ]
    remainder = [node for node in nodes if node.kind not in {"attribute", "combat", "base"}]
    if remainder:
        groups.append(("Other", remainder))
    groups = [(kind, group) for kind, group in groups if group]
    available = right - x - 30 - (len(groups) - 1) * 14
    px = x + 15
    for kind, group in groups:
        width = int(available * len(group) / len(nodes))
        _text(c, px, top - 1, kind.title(), width, size=12, muted=True)
        size = max(12, min(31, bottom - top - 29, (width - (len(group) - 1) * 5) // len(group)))
        for index, node in enumerate(group):
            nx, ny = px + index * (size + 5), top + 20
            unlocked = node.unlocked or node.id in model.talents.unlocked_node_ids
            links = node.icon if unlocked else node.locked_icon
            source = _source(c, links) or _source(c, node.icon)
            if source is None:
                c.draw.ellipse(
                    (nx + 2, ny + 2, nx + size - 2, ny + size - 2),
                    outline=c.fg if unlocked else c.muted,
                    width=2,
                )
            else:
                glyph = fitted(source, (size, size), contain=True)
                if kind != "base" and glyph.getchannel("A").getextrema() != (255, 255):
                    alpha = glyph.getchannel("A")
                    glyph = Image.new("RGBA", glyph.size, c.fg if unlocked else c.muted)
                    glyph.putalpha(alpha)
                if not unlocked:
                    glyph.putalpha(glyph.getchannel("A").point(lambda alpha: int(alpha * 0.34)))
                c.image.alpha_composite(glyph, (nx, ny))
        px += width + 14

    if bottom - y < 150:
        return
    text_top = top + 63
    capacity = max(0, ((bottom - text_top - 8) // 28) * 2)
    named = []
    seen = set()
    for kind in ("combat", "base", "attribute", "Other"):
        for node in nodes:
            if node.kind != kind or not node.name:
                continue
            key = (node.name, node.level, node.max_level)
            if key in seen:
                continue
            seen.add(key)
            named.append(node)
    cell = (right - x - 42) // 2
    for index, node in enumerate(named[:capacity]):
        row, column = divmod(index, 2)
        nx, ny = x + 15 + column * (cell + 12), text_top + row * 28
        _text(c, nx, ny, node.name, cell - 50, size=14, muted=True)
        _text(c, nx + cell - 43, ny, f"{node.level}/{node.max_level}", 43, size=12, muted=True)


def _effect_text(model: Any, effect: Any) -> str | None:
    stat = model.stats.values.get(effect.id) if model.stats is not None else None
    name = STAT_NAMES.get(effect.id) or (stat.name if stat is not None else "")
    if not name or name.casefold().startswith(("stat ", "property ")):
        return None
    if effect.unit == StatUnit.FRACTION:
        value = format_percent(effect.value)
    elif effect.unit == StatUnit.FACTOR:
        value = f"{effect.value:g}×"
    else:
        value = f"{effect.value:g}"
    sign = "+" if effect.value >= 0 and effect.unit != StatUnit.FACTOR else ""
    return f"{sign}{value} {name}"


def _essence_icon(c: PageCanvas, gem: Any, box: Box) -> None:
    base = _source(c, gem.base_icon)
    badge = _source(c, gem.icon)
    if base is None:
        _item(c, gem.icon, box, gem.rarity or 5)
        return
    x, y, right, bottom = box
    size = right - x, bottom - y
    tile = fitted(base, size, contain=True)
    if badge is not None:
        glyph = ImageOps.contain(
            badge.convert("RGBA"), (int(size[0] * 0.50), int(size[1] * 0.50)), Image.Resampling.LANCZOS
        )
        tile.alpha_composite(glyph, ((size[0] - glyph.width) // 2, (size[1] - glyph.height) // 2))
    c.image.alpha_composite(tile, (x, y))


def draw_weapon(c: PageCanvas, model: Any, box: Box) -> None:
    """Use AKEF's dark weapon band and restore the caller's drawing palette."""
    previous = c.panel_color, c.fg, c.muted, c.line
    if not c.dark:
        c.panel_color, c.fg, c.muted, c.line = "#20242C", "#F2F3F6", "#ABB2BF", "#3B424D"
    try:
        _draw_weapon(c, model, box)
    finally:
        c.panel_color, c.fg, c.muted, c.line = previous


def _draw_weapon(c: PageCanvas, model: Any, box: Box) -> None:
    """Show actual weapon state, resolved skill effects and three essence terms."""
    x, y, right, bottom = box
    c.panel(box)
    top = _title(c, box, "Weapon")
    weapon = model.weapon
    if weapon is None:
        _text(c, x + 18, top + 15, c.t("Unavailable"), right - x - 36, muted=True)
        return
    width, height = right - x - 32, bottom - top - 12
    wide = width >= 710
    gem = weapon.gem
    gem_width = min(290, width // 3) if gem is not None and wide else 0
    weapon_width = width - gem_width - (18 if gem_width else 0)
    px = x + 16
    icon_size = min(79, max(54, height // 3))
    _item(c, weapon.images, (px, top + 3, px + icon_size, top + 3 + icon_size), weapon.rarity)
    text_x = px + icon_size + 14
    _text(c, text_x, top, weapon.name or weapon.id, weapon_width - icon_size - 14, size=27, bold=True)
    _text(
        c,
        text_x,
        top + 34,
        f"Lv {weapon.level} · B{weapon.breakthrough} · R{weapon.refinement}",
        weapon_width - icon_size - 14,
        size=17,
        muted=True,
    )
    _stars(c, weapon.rarity, text_x, top + 60, 12)
    if weapon.base_attack is not None:
        _text(
            c, px + weapon_width - 139, top + 59, f"Base ATK {weapon.base_attack:g}", 138, size=13, muted=True
        )
    skill_top = top + icon_size + 15
    skills = weapon.skills[:3]
    if skills:
        cell = weapon_width // len(skills)
        for index, skill in enumerate(skills):
            sx = px + index * cell
            _text(c, sx, skill_top, skill.name or skill.key, cell - 12, size=15, muted=True, lines=1)
            effects = [value for effect in skill.effects if (value := _effect_text(model, effect))]
            _text(
                c,
                sx,
                skill_top + 24,
                " · ".join(effects[:2]) or f"Lv {skill.level}",
                cell - 12,
                size=17,
                bold=True,
                lines=1,
            )
            _text(c, sx, skill_top + 49, f"{skill.level}/{skill.max_level}", cell - 12, size=12, muted=True)
            _pips(c, sx, skill_top + 73, skill.level, skill.max_level, cell - 14)
    elif weapon.effects:
        values = [value for effect in weapon.effects if (value := _effect_text(model, effect))]
        _text(c, px, skill_top, " · ".join(values[:3]), weapon_width, size=17, lines=2)
    if gem is None:
        return
    if wide:
        gx, gy, room = right - gem_width - 16, top, gem_width
        c.draw.line((gx - 12, top, gx - 12, bottom - 15), fill=c.line)
        _essence_icon(c, gem, (gx, gy + 5, gx + 52, gy + 57))
        _text(c, gx + 62, gy + 3, c.t("Essence"), room - 62, size=13, muted=True)
        _text(c, gx + 62, gy + 23, gem.name, room - 62, size=18, bold=True, lines=2, color=c.accent)
        ty = gy + 82
        for term in gem.terms[:3]:
            _text(c, gx, ty, term.name or term.id, room - 66, size=16, muted=True)
            _text(c, gx + room - 49, ty - 1, f"+{term.points}", 49, size=18, bold=True)
            _pips(c, gx, ty + 25, term.points, max(1, term.points), room - 61, height=4)
            ty += 40
    else:
        gy = max(skill_top + 86, bottom - 85)
        _essence_icon(c, gem, (px, gy + 4, px + 39, gy + 43))
        _text(
            c, px + 48, gy, c.t("Essence") + " · " + gem.name, width - 48, size=16, bold=True, color=c.accent
        )
        term_top = gy + 30
        terms = gem.terms[:3]
        cell = (width - 44) // max(1, len(terms))
        for index, term in enumerate(terms):
            tx = px + 44 + index * cell
            _text(c, tx, term_top, term.name or term.id, cell - 8, size=13, muted=True)
            _text(c, tx, term_top + 21, f"+{term.points}", cell - 8, size=16, bold=True)


def _affix_icon(c: PageCanvas, line: Any, x: int, y: int) -> int:
    direct = image_url(line.icon)
    if direct:
        return 22 if c.icon(direct, x, y, 16, tint=c.muted) else 0
    offset = 0
    for key in line.stat_ids[:2]:
        if c.icon(f"stat.{key}", x + offset, y, 15, tint=c.muted):
            offset += 20
    return offset


def draw_equipment(c: PageCanvas, model: Any, box: Box, *, columns: int = 4) -> None:
    """Retain all four observed pieces and their exact values/enhancement levels."""
    x, y, right, bottom = box
    title_y = _title(c, box, "Equipment")
    width = right - x
    sets = model.equipment_sets
    if sets:
        summary = " · ".join(f"{suit.name} {suit.pieces}/{suit.required_pieces}" for suit in sets)
        _text(c, x + 16, title_y - 1, summary, width - 34, size=16, bold=True, color=c.accent)
        title_y += 28
    if model.tactical_item is not None:
        item = model.tactical_item
        icon_x = right - min(270, width // 2)
        c.icon(image_url(item.icon) or "", icon_x, y + 6, 23)
        _text(c, icon_x + 31, y + 6, item.name, right - icon_x - 44, size=15, muted=True)
    pieces = model.equipment[:4]
    if not pieces:
        c.panel((x, title_y + 2, right, bottom))
        _text(c, x + 18, title_y + 22, c.t("Unavailable"), width - 36, muted=True)
        return
    columns = max(1, min(columns, len(pieces)))
    rows = math.ceil(len(pieces) / columns)
    gap = 13
    card_w = (width - (columns - 1) * gap) // columns
    card_h = (bottom - title_y - (rows - 1) * gap) // rows
    for index, piece in enumerate(pieces):
        row, column = divmod(index, columns)
        px, py = x + column * (card_w + gap), title_y + row * (card_h + gap)
        c.panel((px, py, px + card_w, py + card_h))
        rare = RARITY_COLORS.get(piece.rarity, c.accent)
        c.draw.rectangle((px + 10, py + 1, px + card_w - 10, py + 5), fill=rare)
        icon_size = min(55, card_w // 3)
        _item(c, piece.icon, (px + 12, py + 14, px + 12 + icon_size, py + 14 + icon_size), piece.rarity)
        hx = px + icon_size + 23
        _text(
            c,
            hx,
            py + 12,
            SLOT_NAMES.get(str(piece.slot), str(piece.slot)),
            card_w - icon_size - 36,
            size=13,
            muted=True,
        )
        defense = f"DEF {piece.defense:g}" if piece.defense is not None else "DEF —"
        _text(c, hx, py + 34, defense, card_w - icon_size - 36, size=22, bold=True)
        enhancement = str(piece.enhance_count)
        if piece.max_enhance is not None:
            enhancement += f"/{piece.max_enhance}"
        _text(c, px + 12, py + 70, enhancement, icon_size + 5, size=12, muted=True)
        name_y = py + 91
        _text(c, px + 12, name_y, piece.name or piece.id, card_w - 24, size=16, bold=True)
        affix_top = name_y + 24
        lines = piece.stat_lines[:3]
        if not lines:
            _text(c, px + 12, affix_top + 8, c.t("Unavailable"), card_w - 24, size=14, muted=True)
            continue
        step = max(27, (py + card_h - affix_top - 8) // len(lines))
        for line_index, line in enumerate(lines):
            ly = affix_top + line_index * step
            offset = _affix_icon(c, line, px + 12, ly + 1)
            value_width = min(75, max(49, int(card_w * 0.24)))
            if card_h < 225:
                pip_width = 26
                pip_x = px + card_w - 70
                value_x = pip_x - value_width - 8
                label_width = value_x - px - 20 - offset
                _text(c, px + 12 + offset, ly, line.name, label_width, size=13, muted=True)
                _text(c, value_x, ly - 1, line.display or "—", value_width, size=17, bold=True)
                _pips(c, pip_x, ly + 7, line.level, line.max_level, pip_width, height=4)
                _text(c, pip_x + 33, ly + 1, f"{line.level}/{line.max_level}", 26, size=11, muted=True)
                continue
            label_width = card_w - 30 - offset - value_width
            _text(c, px + 12 + offset, ly, line.name, label_width, size=13, muted=True)
            _text(
                c,
                px + card_w - value_width - 12,
                ly - 1,
                line.display or "—",
                value_width,
                size=17,
                bold=True,
            )
            pip_width = max(15, min(label_width, 64))
            _pips(c, px + 12 + offset, ly + step - 10, line.level, line.max_level, pip_width, height=4)
            _text(
                c, px + card_w - 62, ly + step - 13, f"{line.level}/{line.max_level}", 50, size=12, muted=True
            )


def draw_identity(c: PageCanvas, model: Any, x: int, y: int, width: int) -> None:
    _text(c, x, y, model.name, width, size=58, bold=True)
    meta_y = y + 72
    _text(
        c,
        x,
        meta_y,
        f"Lv {model.level}/{model.max_level} · E{model.evolution} · P{model.potential}",
        width,
        size=23,
        bold=True,
    )
    badge_y = meta_y + 37
    c.icon(
        image_url(model.profession.icons) or f"profession.{model.profession.key}", x, badge_y, 31, tint=c.fg
    )
    tint = ELEMENT_COLORS.get(element_key(model), "#87919E")
    c.draw.ellipse((x + 41, badge_y - 1, x + 75, badge_y + 33), fill=tint)
    element_icon = image_url(model.element.icons)
    if element_icon is None:
        key = ELEMENT_STAT.get(element_key(model))
        element_icon = f"stat.{key}" if key is not None else f"element.{model.element.key}"
    c.icon(element_icon, x + 47, badge_y + 5, 23, tint="#FFFFFF")
    _text(
        c,
        x + 84,
        badge_y + 2,
        " · ".join(value for value in (model.profession.name, model.element.name) if value)
        or c.t("Unavailable"),
        max(40, width - 214),
        size=20,
        muted=True,
    )
    _stars(c, model.rarity, x, badge_y + 46, 16)
    if model.weapon_type.name:
        _text(c, x + 155, badge_y + 44, model.weapon_type.name, width - 155, size=17, muted=True)
