"""Source article sections, skills and talents with measured continuation pages."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.utils.records import Record, append_model_text, iter_records


def urls(model: Any) -> set[str]:
    links = [image_url(model.summary.icon), image_url(model.illustration)]
    links.extend(image_url(skill.icon) for skill in model.skills)
    links.extend(image_url(node.icon) for node in model.talents.nodes)
    links.extend(image_url(item.icon) for section in model.sections for item in section.items)
    return {link for link in links if link}


def _effects(lines: list[str], effects: Any) -> None:
    for effect in effects:
        value = (
            f"{effect.value * 100:g}%"
            if str(effect.unit) == "fraction"
            else f"{effect.value:g}×"
            if str(effect.unit) == "factor"
            else f"{effect.value:g}"
        )
        lines.append(f"Property {effect.id}: {value} · {effect.formula}")


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    summary = model.summary
    lines = [summary.category.name or summary.category.key]
    if summary.description:
        lines.append(summary.description)
    records = [
        Record(
            summary.name or summary.id,
            lines,
            images=[(image_url(model.illustration) or image_url(summary.icon), summary.name)],
        )
    ]
    for skill in model.skills:
        lines = [f"Level: {skill.level}/{skill.max_level}", skill.description or skill.raw_description]
        if skill.type is not None:
            lines.insert(0, skill.type.name or skill.type.key)
        _effects(lines, skill.effects)
        for form in skill.forms:
            lines.extend([form.name, form.description])
            append_model_text(lines, form.params)
        append_model_text(lines, skill.params)
        append_model_text(lines, skill.level_params)
        records.append(Record(skill.name or skill.id, lines, images=[(image_url(skill.icon), skill.name)]))
    for node in model.talents.nodes:
        unlocked = node.unlocked or node.id in model.talents.unlocked_node_ids
        lines = [
            f"{node.kind} · Level {node.level}/{node.max_level} · {'Unlocked' if unlocked else 'Locked'}",
            node.description,
        ]
        _effects(lines, node.effects)
        records.append(Record(node.name or node.id, lines, images=[(image_url(node.icon), node.name)]))
    for potential in model.talents.potentials:
        lines = [
            f"Potential {potential.level} · {'Unlocked' if potential.unlocked else 'Locked'}",
            potential.description,
        ]
        _effects(lines, potential.effects)
        records.append(Record(potential.name or f"Potential {potential.level}", lines))
    for section in model.sections:
        records.append(Record(section.title or "Article section", [section.text]))
        for item in section.items:
            lines = [item.description]
            if item.rarity is not None:
                lines.insert(0, f"Rarity: {item.rarity}")
            records.append(Record(item.name or item.id, lines, images=[(image_url(item.icon), item.name)]))
    yield from iter_records("WIKI", context, records, variant=variant, assets=assets)


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    """Collect the explicitly requested render batch."""
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
