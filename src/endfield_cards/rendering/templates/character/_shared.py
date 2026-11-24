"""Rectified legacy panoramic showcase and three complementary compositions."""

from collections.abc import Iterator
from importlib import import_module
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.models import Artwork
from endfield_cards.utils.blending import hero_url
from endfield_cards.utils.records import (
    Record,
    append_model_text,
    iter_records,
    record_page_count,
)


def urls(model: Any) -> set[str]:
    links = [hero_url(model)]
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


SIZE_BY_VARIANT = {
    "field": (1920, 1000),
    "dossier": (1600, 1400),
    "terminal": (1920, 1240),
    "portrait": (1100, 1950),
}


def page_count(model: Any, context: Any, *, variant: str = "field", details: bool = False) -> int:
    if not details:
        return 1
    detail_size = (1100, 1700) if variant == "portrait" else (1600, 1100)
    return 1 + record_page_count(
        context, records(model), size=detail_size, columns=1 if variant == "portrait" else 2
    )


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "field",
    assets: Any = None,
    artwork: Artwork | None = None,
    details: bool = False,
    **options: Any,
) -> Iterator[Image.Image]:
    """Draw the actual named layout; descriptions remain an explicit optional export."""
    module = import_module(f"endfield_cards.rendering.templates.character.{variant}")
    total = page_count(model, context, variant=variant, details=details)
    yield module.render(model, context, assets=assets, artwork=artwork, page=1, pages=total, **options)
    if not details:
        return
    detail_size = (1100, 1700) if variant == "portrait" else (1600, 1100)
    yield from iter_records(
        model.name,
        context,
        records(model),
        variant="dark" if variant in {"field", "terminal"} else "light",
        assets=assets,
        size=detail_size,
        columns=1 if variant == "portrait" else 2,
        page_offset=1,
        total_pages=total,
    )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
