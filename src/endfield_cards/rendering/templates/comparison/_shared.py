"""Source-backed, aligned comparison components for two builds of one operator."""

from __future__ import annotations

import math
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from skport.games.endfield.models import StatUnit, StatValue

from endfield_cards.adapters.skport import image_url
from endfield_cards.rendering.templates.character import components as parts
from endfield_cards.utils.blending import draw_character_art, element_colour, paint_background
from endfield_cards.utils.drawing import PageCanvas

SIZE = (2160, 1440)
SIDE_WIDTH = 680
BUILD_COLORS = ("#FFC800", "#77C7D5")
CORE = (*parts.CORE_IDS, 9, 10, 44, 30)
BONUSES = (29, 87, 26, 17, 32, 33, 28, 50, 51, 52, 53, 54, 55, 61)
SLOTS = tuple(parts.SLOT_NAMES)


@dataclass(frozen=True)
class ComparisonRow:
    stat_id: int
    name: str
    first: StatValue | None
    second: StatValue | None
    delta: float | None
    delta_text: str


def _difference(first: StatValue | None, second: StatValue | None) -> tuple[float | None, str]:
    if first is None or second is None or first.unit != second.unit:
        return None, "—"
    difference = Decimal(str(second.value)) - Decimal(str(first.value))
    value = float(difference)
    if not math.isfinite(value):
        return None, "—"
    prefix = "+" if value > 0 else ""
    if first.unit == StatUnit.FRACTION:
        points = (difference * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        if points.is_zero():
            return value, "0.0 pp"
        return value, f"{prefix}{points:.1f} pp"
    if first.unit == StatUnit.FACTOR:
        return value, f"{prefix}{value:.4g}×"
    return value, prefix + (f"{value:,.0f}" if value.is_integer() else f"{value:,.4g}")


def compare_rows(first: Any, second: Any) -> list[ComparisonRow]:
    """Union useful observed properties; never substitute zero for absent values."""
    left = first.stats.values if first.stats is not None else {}
    right = second.stats.values if second.stats is not None else {}
    own = parts.ELEMENT_STAT.get(parts.element_key(first))
    order = dict.fromkeys((*CORE, own, *BONUSES, *sorted(set(left) | set(right))))
    rows = []
    for key in order:
        a, b = left.get(key), right.get(key)
        observed = [stat for stat in (a, b) if stat is not None]
        if not observed:
            continue
        source = observed[0]
        changed = a is not None and b is not None and (a.value != b.value or a.unit != b.unit)
        label = parts.STAT_NAMES.get(key, source.name or f"Property {key}")
        if key not in CORE and not changed:
            if all(abs(stat.value) <= 1e-6 for stat in observed):
                continue
            if all(stat.unit == StatUnit.FACTOR and stat.value == 1 for stat in observed):
                continue
            if label.casefold().startswith(("stat ", "property ")) and key in {8, 11, 12, 25, 49, 90}:
                continue
        delta, delta_text = _difference(a, b)
        rows.append(ComparisonRow(source.id, label, a, b, delta, delta_text))
    return rows


def side_assets(assets: Any, index: int) -> Any:
    """Select custom artwork independently, including identical default hero URLs."""
    view = assets.fork() if assets is not None and hasattr(assets, "fork") else dict(assets or {})
    if index == 1:
        view.pop("custom_art", None)
        if "second_custom_art" in view:
            view["custom_art"] = view["second_custom_art"]
    return view


def _text(c: PageCanvas, x: int, y: int, value: object, width: int, **kwargs: Any) -> None:
    c.text(x, y, value, width=width, max_lines=kwargs.pop("max_lines", 1), **kwargs)


def _center(c: PageCanvas, x: int, y: int, value: str, width: int, *, size: int, **kwargs: Any) -> None:
    font = c.fonts.get(size, weight="semibold" if kwargs.get("bold") else "regular", text=value)
    measured = c.draw.textlength(value, font=font)
    _text(c, x + max(0, int((width - measured) / 2)), y, value, width, size=size, **kwargs)


def draw_heading(c: PageCanvas, model: Any, *, dark: bool) -> None:
    c.draw.line((40, 63, 2120, 63), fill=c.line)
    _text(c, 43, 22, "ENDFIELD / " + c.t("Comparison"), 750, size=21, bold=True, fill=c.muted)
    _text(c, 1775, 22, "SAME OPERATOR · TWO BUILDS", 345, size=17, fill=c.muted)
    _center(c, 750, 128, model.name, 660, size=57, bold=True)
    meta = " · ".join(
        value for value in (model.profession.name, model.element.name, model.weapon_type.name) if value
    )
    _center(c, 750, 209, meta or c.t("Unavailable"), 660, size=20, fill=c.muted)
    glyph_x = 948
    c.icon(
        image_url(model.profession.icons) or f"profession.{model.profession.key}", glyph_x, 253, 32, tint=c.fg
    )
    color = element_colour(model)
    c.draw.ellipse((glyph_x + 45, 252, glyph_x + 79, 286), fill=color)
    c.icon(
        image_url(model.element.icons) or f"element.{model.element.key}",
        glyph_x + 50,
        257,
        24,
        tint="#FFFFFF",
    )
    parts._stars(c, model.rarity, glyph_x + 95, 260, 17)
    c.draw.line((918, 315, 1242, 315), fill=c.accent, width=3)
    _center(c, 750, 334, "A vs B   /   " + c.t("Statistics"), 660, size=18, fill=c.muted)
    if dark:
        c.draw.line((731, 89, 731, 1345), fill=c.line)
        c.draw.line((1429, 89, 1429, 1345), fill=c.line)


def draw_build_header(
    c: PageCanvas, model: Any, owner_context: Any, index: int, assets: Any, artwork: Any, *, dark: bool
) -> None:
    x = 40 + index * 1400
    color = BUILD_COLORS[index]
    if not dark:
        c.panel((x, 85, x + SIDE_WIDTH, 406))
    draw_character_art(c, model, (x + 250, 79, x + SIDE_WIDTH, 310), assets, artwork, portrait=True)
    # Keep the owner's text on its own quiet surface, away from the artwork.
    c.scrim((x + 12, 95, x + 308, 289), dark=dark, alpha=244)
    c.draw.rounded_rectangle((x + 18, 101, x + 54, 135), radius=6, fill=color)
    _text(c, x + 29, 104, "AB"[index], 23, size=21, bold=True, fill="#171C24")
    _text(c, x + 67, 107, c.t("Build"), 175, size=18, fill=c.muted)
    _text(c, x + 18, 148, owner_context.owner.name, 277, size=35, bold=True)
    _text(c, x + 19, 196, f"UID {owner_context.owner.game_uid}", 281, size=18, fill=c.muted)
    _text(
        c,
        x + 18,
        233,
        f"Lv {model.level}/{model.max_level} · E{model.evolution} · P{model.potential}",
        285,
        size=23,
        bold=True,
    )
    parts.draw_talents(c, model, (x + 12, 298, x + SIDE_WIDTH - 12, 399))


def draw_stat_comparison(c: PageCanvas, first: Any, second: Any) -> None:
    box = (750, 384, 1410, 1077)
    c.panel(box)
    x, y, right, bottom = box
    c.draw.rectangle((x + 15, y + 15, x + 19, y + 33), fill=c.accent)
    _text(c, x + 29, y + 9, c.t("Statistics"), 320, size=23, bold=True)
    _text(c, x + 396, y + 15, "Δ B − A", 245, size=16, fill=c.muted)
    columns = ((x + 18, 196, "PROPERTY"), (x + 215, 129, "A"), (x + 355, 126, "B"), (x + 491, 148, "Δ"))
    for px, width, label in columns:
        _text(c, px, y + 49, label, width, size=14, fill=c.muted, bold=True)
    rows = compare_rows(first, second)
    if not rows:
        _text(c, x + 19, y + 99, c.t("Unavailable"), 620, size=24, fill=c.muted)
        return
    top = y + 80
    visible = rows[:20]
    step = min(37, (bottom - top - 48) // len(visible))
    for index, row in enumerate(visible):
        py = top + index * step
        if index % 2 == 0:
            c.draw.rounded_rectangle(
                (x + 9, py - 1, right - 9, py + step - 3), radius=5, fill="#2B313B" if c.dark else "#F0EFE9"
            )
        source = row.first if row.first is not None else row.second
        role = ""
        if source is not None:
            role = "Main" if source.is_main else "Sub" if source.is_sub else ""
            for model in (first, second):
                if model.stats is not None and model.stats.main_attribute == row.stat_id:
                    role = "Main"
                    break
                if model.stats is not None and model.stats.sub_attribute == row.stat_id:
                    role = role or "Sub"
        color = (c.accent if c.dark else "#916900") if role == "Main" else c.fg if role == "Sub" else c.muted
        offset = parts._stat_icon(c, source, x + 17, py + 6, 18, color) if source else 0
        label = row.name + (" · " + c.t(role) if role else "")
        _text(c, x + 17 + offset, py + 3, label, 188 - offset, size=min(17, step - 13), fill=color)
        for stat, (px, width, _) in zip((row.first, row.second), columns[1:3], strict=True):
            _text(
                c,
                px,
                py + 1,
                parts.display_value(stat) if stat is not None else "—",
                width,
                size=min(23, step - 9),
                bold=True,
            )
        _text(c, columns[3][0], py + 4, row.delta_text, columns[3][1], size=min(18, step - 12), fill=c.muted)
    note = "pp = percentage points · — = unavailable"
    if len(rows) > len(visible):
        note += f" · +{len(rows) - len(visible)} properties"
    _text(c, x + 18, bottom - 29, note, 623, size=13, fill=c.muted)


def skill_pairs(first: Any, second: Any) -> list[tuple[Any, Any]]:
    """Match canonical skill IDs/keys, never unrelated positional levels."""

    def key(skill: Any) -> tuple[str, str]:
        if skill.id:
            return "id", skill.id
        if skill.key:
            return "key", skill.key
        return "name", skill.name

    left = {key(skill): skill for skill in first.skills}
    right = {key(skill): skill for skill in second.skills}
    return [(left.get(item), right.get(item)) for item in dict.fromkeys((*left, *right))]


def draw_skill_comparison(c: PageCanvas, first: Any, second: Any) -> None:
    x, y, right, bottom = 750, 1094, 1410, 1346
    c.panel((x, y, right, bottom))
    parts._title(c, (x, y, right, bottom), "Skills")
    _text(c, x + 431, y + 8, "A             B", 211, size=16, fill=c.muted, bold=True)
    pairs = skill_pairs(first, second)
    if not pairs:
        _text(c, x + 19, y + 63, c.t("Unavailable"), 620, size=20, fill=c.muted)
        return
    visible = pairs[:8]
    step = min(49, (bottom - y - (68 if len(pairs) > len(visible) else 46)) // len(visible))
    for index, (a, b) in enumerate(visible):
        source = a if a is not None else b
        py = y + 42 + index * step
        size = min(36, step - 7)
        parts._item(c, source.icon, (x + 15, py, x + 15 + size, py + size))
        _text(
            c,
            x + 62,
            py + 2,
            source.name or source.key or source.id,
            352,
            size=max(12, min(17, step - 14)),
            bold=True,
        )
        for skill, px in ((a, x + 433), (b, x + 548)):
            _text(
                c,
                px,
                py + 1,
                f"{skill.level}/{skill.max_level}" if skill is not None else "—",
                100,
                size=min(22, step - 10),
                bold=True,
            )

    if len(pairs) > len(visible):
        _text(c, x + 17, bottom - 25, f"+{len(pairs) - len(visible)} skills", 620, size=13, fill=c.muted)


def equipment_slots(model: Any) -> list[tuple[str, Any]]:
    supplied = {str(piece.slot): piece for piece in model.equipment}
    return [(slot, supplied.get(slot)) for slot in SLOTS]


def draw_loadout(c: PageCanvas, model: Any, index: int, *, dark: bool) -> None:
    x = 40 + index * 1400
    parts.draw_weapon(c, model, (x, 426, x + SIDE_WIDTH, 769))
    box = (x, 788, x + SIDE_WIDTH, 1346)
    c.panel(box)
    parts._title(c, box, "Equipment")
    _text(c, x + 538, 800, f"{len(model.equipment)}/4", 121, size=18, bold=True, fill=c.muted)
    sets = " · ".join(f"{suit.name} {suit.pieces}/{suit.required_pieces}" for suit in model.equipment_sets)
    _text(
        c,
        x + 17,
        826,
        sets or "—",
        SIDE_WIDTH - 34,
        size=17,
        fill=c.accent if c.dark else "#916900",
        bold=True,
    )
    top, cell_w, cell_h = 859, 323, 228
    for position, (slot, piece) in enumerate(equipment_slots(model)):
        row, column = divmod(position, 2)
        px, py = x + 13 + column * 331, top + row * 237
        c.panel((px, py, px + cell_w, py + cell_h))
        if piece is None:
            _text(c, px + 15, py + 16, parts.SLOT_NAMES[slot], cell_w - 30, size=18, bold=True)
            c.draw.rounded_rectangle((px + 19, py + 68, px + 65, py + 114), radius=9, outline=c.line, width=2)
            c.draw.line((px + 31, py + 91, px + 53, py + 91), fill=c.muted, width=2)
            _text(c, px + 81, py + 77, c.t("Unavailable"), cell_w - 94, size=21, fill=c.muted)
            continue
        rarity = parts.RARITY_COLORS.get(piece.rarity, c.accent)
        c.draw.rectangle((px + 10, py + 1, px + cell_w - 10, py + 4), fill=rarity)
        parts._item(c, piece.icon, (px + 11, py + 13, px + 62, py + 64), piece.rarity)
        _text(c, px + 74, py + 12, parts.SLOT_NAMES[slot], cell_w - 85, size=13, fill=c.muted)
        defense = f"DEF {piece.defense:g}" if piece.defense is not None else "DEF —"
        _text(c, px + 74, py + 32, defense, 137, size=24, bold=True)
        enhanced = str(piece.enhance_count) + (
            f"/{piece.max_enhance}" if piece.max_enhance is not None else ""
        )
        _text(c, px + 217, py + 39, enhanced, 95, size=13, fill=c.muted)
        _text(c, px + 12, py + 75, piece.name or piece.id, cell_w - 24, size=19, bold=True)
        for line_index, line in enumerate(piece.stat_lines[:3]):
            ly = py + 107 + line_index * 37
            offset = parts._affix_icon(c, line, px + 12, ly + 2)
            _text(c, px + 12 + offset, ly, line.name, 200 - offset, size=14, fill=c.muted)
            _text(c, px + 224, ly - 2, line.display or "—", 86, size=19, bold=True)
            parts._pips(c, px + 12 + offset, ly + 25, line.level, line.max_level, 67, height=4)
            _text(c, px + 95 + offset, ly + 20, f"{line.level}/{line.max_level}", 97, size=12, fill=c.muted)
        if not piece.stat_lines:
            _text(c, px + 12, py + 110, c.t("Unavailable"), cell_w - 24, size=15, fill=c.muted)
    if model.tactical_item is not None:
        item = model.tactical_item
        c.icon(image_url(item.icon) or "", x + 17, 1326, 17)
        _text(c, x + 42, 1325, item.name, SIDE_WIDTH - 60, size=13, fill=c.muted)


def render_layout(
    first: Any,
    second: Any,
    context: Any,
    second_context: Any,
    *,
    dark: bool,
    assets: Any = None,
    artwork: Any = None,
    second_artwork: Any = None,
) -> PageCanvas:
    from dataclasses import replace

    c = PageCanvas(
        "Comparison",
        replace(context, comparison_owner=second_context.owner),
        dark=dark,
        size=SIZE,
        assets=assets,
        header=False,
    )
    views = (side_assets(assets, 0), side_assets(assets, 1))
    paint_background(c, first, views[0], artwork, style="field" if dark else "dossier")
    draw_heading(c, first, dark=dark)
    for index, (model, owner_context, custom) in enumerate(
        ((first, context, artwork), (second, second_context, second_artwork))
    ):
        draw_build_header(c, model, owner_context, index, views[index], custom, dark=dark)
        draw_loadout(c, model, index, dark=dark)
    draw_stat_comparison(c, first, second)
    draw_skill_comparison(c, first, second)
    return c
