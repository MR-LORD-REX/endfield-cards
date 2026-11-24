"""Rectified legacy panoramic showcase and three complementary compositions."""

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.models import Artwork
from endfield_cards.rendering.components import (
    ELEMENT_COLORS,
    STAT_ICONS,
    PageCanvas,
    art_url,
    element_key,
    place_art,
)
from endfield_cards.rendering.templates._records import (
    Record,
    append_model_text,
    iter_records,
    record_page_count,
)


def urls(model: Any) -> set[str]:
    links = [art_url(model)]
    links.extend(image_url(skill.icon) for skill in model.skills)
    links.extend(image_url(item.icon) for item in model.equipment)
    links.extend(image_url(node.icon) for node in model.talents.nodes)
    if model.weapon is not None:
        links.append(image_url(model.weapon.images))
        links.extend(image_url(skill.icon) for skill in model.weapon.skills)
        if model.weapon.gem is not None:
            links.append(image_url(model.weapon.gem.icon))
    if model.tactical_item is not None:
        links.append(image_url(model.tactical_item.icon))
    return {link for link in links if link}


def _effects(effects: list[Any]) -> list[str]:
    return [
        f"Property {effect.id} · {effect.formula} · {effect.value:g} ({effect.unit})" for effect in effects
    ]


def records(model: Any) -> list[Record]:
    """Preserve detailed stats, observed skills, talent states and equipped effects."""
    result: list[Record] = []
    if model.stats is not None:
        lines = []
        for stat in model.stats.values.values():
            role = " · Main" if stat.is_main else " · Sub" if stat.is_sub else ""
            lines.append(f"{stat.name or 'Property ' + str(stat.id)}: {stat.display}{role}")
        result.append(Record("Statistics", lines))
    else:
        result.append(
            Record("Statistics", [f"Calculation: {model.calculation_state} · Statistics unavailable"])
        )
    for skill in model.skills:
        lines = [
            f"Level {skill.level}/{skill.max_level}",
            skill.description or skill.raw_description,
            *_effects(skill.effects),
        ]
        for form in skill.forms:
            lines.extend([form.name, form.description])
            append_model_text(lines, form.params)
        result.append(
            Record(skill.name or skill.key or skill.id, lines, images=[(image_url(skill.icon), "")])
        )
    for node in model.talents.nodes:
        unlocked = node.unlocked or node.id in model.talents.unlocked_node_ids
        result.append(
            Record(
                node.name or node.id,
                [
                    f"{node.kind} · Level {node.level}/{node.max_level} · {'Unlocked' if unlocked else 'Locked'}",
                    node.description,
                    *_effects(node.effects),
                ],
                images=[(image_url(node.icon), "")],
            )
        )
    for potential in model.talents.potentials:
        result.append(
            Record(
                f"Potential {potential.level}: {potential.name}",
                [
                    "Unlocked" if potential.unlocked else "Locked",
                    potential.description,
                    *_effects(potential.effects),
                ],
            )
        )
    if model.weapon is not None:
        weapon = model.weapon
        lines = [
            f"Level {weapon.level} · Refinement {weapon.refinement} · Breakthrough {weapon.breakthrough}",
            f"Rarity {weapon.rarity}",
        ]
        if weapon.base_attack is not None:
            lines.append(f"Base attack: {weapon.base_attack:g}")
        lines.extend(_effects(weapon.effects))
        result.append(Record(weapon.name or weapon.id, lines, images=[(image_url(weapon.images), "")]))
        for skill in weapon.skills:
            skill_lines = [
                f"Level {skill.level}/{skill.max_level}",
                skill.description or skill.raw_description,
                *_effects(skill.effects),
            ]
            for form in skill.forms:
                skill_lines.extend([form.name, form.description])
                append_model_text(skill_lines, form.params)
            result.append(Record(skill.name or skill.id, skill_lines, images=[(image_url(skill.icon), "")]))
        if weapon.gem is not None:
            result.append(
                Record(
                    "Essence · " + weapon.gem.name,
                    [f"{term.name or term.id}: {term.points} points" for term in weapon.gem.terms],
                    images=[(image_url(weapon.gem.icon), "")],
                )
            )
    for item in model.equipment:
        lines = [
            f"Slot: {item.slot} · Rarity {item.rarity} · Enhancements {item.enhance_count}"
            + (f"/{item.max_enhance}" if item.max_enhance is not None else "")
        ]
        if item.defense is not None:
            lines.append(f"Defense: {item.defense:g}")
        if item.suit_name:
            lines.append(f"Set: {item.suit_name}")
        for line in item.stat_lines:
            lines.append(
                f"{line.name}: {line.display or 'Unavailable'} · Level {line.level}/{line.max_level}"
            )
            lines.extend(_effects(line.effects))
        result.append(Record(item.name or item.id, lines, images=[(image_url(item.icon), "")]))
    for suit in model.equipment_sets:
        result.append(
            Record(
                suit.name or suit.id,
                [
                    f"Pieces {suit.pieces}/{suit.required_pieces} · {'Active' if suit.active else 'Inactive'}",
                    suit.description,
                    *_effects(suit.effects),
                ],
            )
        )
    if model.set_effects:
        result.append(Record("Set effects", _effects(model.set_effects)))
    if model.tactical_item is not None:
        item = model.tactical_item
        result.append(
            Record("Tactical item · " + item.name, [item.description], images=[(image_url(item.icon), "")])
        )
    return result


def _stats(c: PageCanvas, model: Any, x: int, y: int, width: int, height: int = 510) -> None:
    y += c.section("Statistics", x, y, width)
    if model.stats is None:
        c.text(x, y, c.t("Unavailable"), fill=c.muted)
        return
    values = model.stats.values
    core = [key for key in (1, 2, 3, 39, 40, 41, 42, 9, 10) if key in values]
    extras = [
        key
        for key, stat in values.items()
        if key not in core
        and stat.unit == "fraction"
        and abs(stat.value) > 1e-6
        and stat.name
        and not stat.name.casefold().startswith(("stat ", "property "))
    ]
    extras.sort(key=lambda key: (key not in {50, 51, 52, 53, 54, 55}, key))
    order = core + extras[:6]
    step = min(33, (height - 45) // max(1, len(order)))
    for key in order:
        stat = values[key]
        icon = "stat." + STAT_ICONS[key] if key in STAT_ICONS else None
        name = stat.name or f"Property {key}"
        mark = "  " + c.t("Main") if stat.is_main else "  " + c.t("Sub") if stat.is_sub else ""
        if icon:
            c.icon(icon, x, y + 1, min(23, step - 3))
        offset = 31 if icon else 0
        c.text(
            x + offset,
            y,
            name + mark,
            size=min(19, step - 9),
            fill=c.muted,
            width=int(width * 0.68) - offset,
            max_lines=1,
        )
        c.text(
            x + int(width * 0.70),
            y,
            stat.display,
            size=min(23, step - 8),
            bold=True,
            width=int(width * 0.30),
            max_lines=1,
        )
        c.draw.line((x, y + step - 3, x + width, y + step - 3), fill=c.line)
        y += step


def _gear(c: PageCanvas, model: Any, x: int, y: int, width: int, *, compact: bool = False) -> None:
    y += c.section("Weapon", x, y, width)
    weapon = model.weapon
    if weapon is not None:
        c.icon(image_url(weapon.images) or "", x, y, 68)
        c.text(x + 80, y, weapon.name, size=27, bold=True, width=width - 80, max_lines=1)
        c.text(
            x + 80,
            y + 36,
            f"Lv {weapon.level} · R{weapon.refinement} · B{weapon.breakthrough}",
            size=18,
            fill=c.muted,
            width=width - 80,
            max_lines=1,
        )
    else:
        c.text(x, y, c.t("Unavailable"), fill=c.muted)
    y += 82
    y += c.section("Equipment", x, y, width)
    if not model.equipment:
        c.text(x, y, c.t("Unavailable"), size=20, fill=c.muted)
        y += 40
    for piece in model.equipment:
        c.icon(image_url(piece.icon) or "", x, y, 54)
        c.text(x + 70, y, piece.name or piece.id, size=23, bold=True, width=width - 70, max_lines=1)
        summary = " · ".join(f"{line.name} {line.display or '—'}" for line in piece.stat_lines[:3])
        c.text(
            x + 70,
            y + 30,
            summary or c.t("Unavailable"),
            size=14 if compact else 16,
            fill=c.muted,
            width=width - 70,
            max_lines=2,
        )
        c.text(x, y + 57, f"+{piece.enhance_count}", size=13, fill=c.muted, width=60, max_lines=1)
        y += 74 if compact else 84
    if model.equipment_sets:
        set_text = " · ".join(
            f"{suit.name} {suit.pieces}/{suit.required_pieces}" for suit in model.equipment_sets
        )
        c.text(x, y, set_text, size=16, fill=c.accent, width=width, max_lines=1)
        y += 27
    if weapon is not None and weapon.gem is not None:
        gem = weapon.gem
        c.icon(image_url(gem.icon) or "", x, y, 34)
        c.text(
            x + 44, y, c.t("Essence") + " · " + gem.name, size=18, bold=True, width=width - 44, max_lines=1
        )
        y += 31
        for term in gem.terms[:3]:
            c.text(x + 10, y, term.name or term.id, size=15, fill=c.muted, width=width - 72, max_lines=1)
            c.text(x + width - 54, y, f"+{term.points}", size=17, bold=True, width=54, max_lines=1)
            y += 23


def _tactical(c: PageCanvas, model: Any, x: int, y: int, width: int) -> None:
    if model.tactical_item is None:
        return
    c.icon(image_url(model.tactical_item.icon) or "", x, y, 25)
    c.text(x + 35, y, model.tactical_item.name, size=17, width=width - 35, max_lines=1)


def _talents(c: PageCanvas, model: Any, x: int, y: int, width: int) -> None:
    nodes = model.talents.nodes
    if not nodes:
        return
    c.scrim((x - 10, y - 6, x + width + 10, y + 64), dark=c.dark)
    c.text(x, y, c.t("Talents"), size=17, bold=True, width=width - 90, max_lines=1)
    c.text(
        x + width - 78,
        y,
        f"{model.talents.unlocked_count}/{len(nodes)}",
        size=17,
        bold=True,
        width=78,
        max_lines=1,
    )
    size = min(30, max(12, (width - 6 * (len(nodes) - 1)) // len(nodes)))
    for index, node in enumerate(nodes):
        unlocked = node.unlocked or node.id in model.talents.unlocked_node_ids
        px = x + index * (size + 6)
        url = image_url(node.icon if unlocked else node.locked_icon) or image_url(node.icon)
        tint = None if node.kind == "base" else c.fg if unlocked else c.muted
        if not url or not c.icon(url, px, y + 29, size, tint=tint):
            c.draw.ellipse(
                (px + 3, y + 32, px + size - 3, y + 29 + size - 3),
                outline=c.fg if unlocked else c.muted,
                width=2,
            )


def page_count(model: Any, context: Any, *, variant: str = "field", details: bool = False) -> int:
    if not details:
        return 1
    detail_size = (1000, 1400) if variant == "portrait" else (1600, 1100)
    return 1 + record_page_count(
        context, records(model), size=detail_size, columns=1 if variant == "portrait" else 2
    )


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "field",
    assets: dict | None = None,
    artwork: Artwork | None = None,
    details: bool = False,
    **options: Any,
) -> Iterator[Image.Image]:
    size = {
        "field": (1920, 900),
        "dossier": (1600, 1100),
        "terminal": (1600, 1000),
        "portrait": (1000, 1400),
    }[variant]
    c = PageCanvas("Character", context, dark=variant in {"field", "terminal"}, size=size, assets=assets)
    c.accent = ELEMENT_COLORS.get(element_key(model), "#FFC800")
    source = (assets or {}).get("custom_art") or (assets or {}).get(art_url(model))
    if variant == "field":
        # Preserve the old left-stat / central-art / right-equipment panorama.
        c.panel((28, 141, 459, 719))
        place_art(c, source, (465, 134, 1315, 829), artwork, blend=True)
        c.panel((1327, 141, 1892, 819))
        c.scrim((489, 143, 1300, 327), alpha=205)
        _stats(c, model, 48, 164, 390, height=515)
        _gear(c, model, 1350, 164, 518)
        _talents(c, model, 507, 648, 770)
        _tactical(c, model, 950, 239, 326)
        sx, sy, sw = 44, 734, 1220
        c.text(507, 146, model.name, size=53, bold=True, width=758, max_lines=2)
    elif variant == "dossier":
        place_art(c, source, (26, 145, 533, 1030), artwork, blend=True)
        c.panel((559, 282, 1033, 1006))
        c.panel((1053, 145, 1570, 1006))
        c.scrim((35, 687, 518, 811), dark=False)
        c.text(564, 150, model.name, size=47, bold=True, width=450, max_lines=2)
        _stats(c, model, 584, 305, 423)
        _gear(c, model, 1077, 168, 470)
        _talents(c, model, 584, 932, 422)
        _tactical(c, model, 584, 241, 422)
        sx, sy, sw = 580, 865, 423
    elif variant == "terminal":
        place_art(c, source, (25, 139, 832, 928), artwork, blend=True)
        c.panel((849, 268, 1215, 914))
        c.panel((1233, 268, 1574, 914))
        c.scrim((33, 689, 822, 819))
        c.text(858, 146, model.name, size=45, bold=True, width=700, max_lines=2)
        _stats(c, model, 872, 289, 320)
        _gear(c, model, 1250, 289, 300, compact=True)
        _talents(c, model, 872, 829, 320)
        _tactical(c, model, 872, 233, 675)
        sx, sy, sw = 44, 777, 751
    else:
        place_art(c, source, (18, 282, 981, 631), artwork, blend=True)
        c.panel((33, 142, 967, 267))
        c.text(46, 151, model.name, size=48, bold=True, width=880, max_lines=1)
        c.text(
            46,
            215,
            f"Lv {model.level}/{model.max_level}  ·  E{model.evolution}  ·  P{model.potential}",
            size=25,
            bold=True,
        )
        c.scrim((35, 561, 967, 628), dark=False)
        c.panel((33, 645, 494, 1260))
        c.panel((505, 645, 967, 1260))
        _stats(c, model, 58, 668, 411, height=450)
        _gear(c, model, 526, 668, 417, compact=True)
        _talents(c, model, 58, 1151, 411)
        _tactical(c, model, 621, 217, 320)
        sx, sy, sw = 45, 1273, 910
    if variant != "portrait":
        c.text(
            505 if variant == "field" else 45,
            235 if variant == "field" else 705,
            f"Lv {model.level}/{model.max_level}  ·  E{model.evolution}  ·  P{model.potential}",
            size=25,
            bold=True,
        )
    for index, skill in enumerate(model.skills[:4]):
        cell = sw // max(1, min(4, len(model.skills)))
        x = sx + index * cell
        icon_size = 44 if cell > 175 else 30
        c.icon(image_url(skill.icon) or "", x, sy, icon_size, tint=c.fg)
        c.text(
            x + icon_size + 9,
            sy,
            f"{skill.level}/{skill.max_level}",
            size=24 if cell > 175 else 18,
            bold=True,
        )
        if cell > 175:
            c.text(x + 53, sy + 33, skill.name, size=16, width=cell - 65, max_lines=1)
    profession_x = 505 if variant == "field" else 46
    profession_y = 283 if variant == "field" else 750 if variant != "portrait" else 579
    c.icon("profession." + model.profession.key, profession_x, profession_y, 32)
    c.icon("element." + model.element.key, profession_x + 43, profession_y, 32)
    c.text(profession_x + 90, profession_y, model.profession.name, size=23)
    c.icon(f"potential.{min(model.potential, 5)}", profession_x + 302, profession_y, 32)
    c.icon("rarity.star", profession_x + 350, profession_y + 3, 24, tint=c.accent)
    c.text(profession_x + 381, profession_y + 1, model.rarity, size=22, fill=c.fg)
    if not details:
        yield c.finish()
        return
    detail_size = (1000, 1400) if variant == "portrait" else (1600, 1100)
    detail_records = records(model)
    total = 1 + record_page_count(
        context, detail_records, size=detail_size, columns=1 if variant == "portrait" else 2
    )
    yield c.finish(1, total)
    yield from iter_records(
        model.name,
        context,
        detail_records,
        variant="dark" if c.dark else "light",
        assets=assets,
        size=detail_size,
        columns=1 if variant == "portrait" else 2,
        page_offset=1,
        total_pages=total,
    )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
