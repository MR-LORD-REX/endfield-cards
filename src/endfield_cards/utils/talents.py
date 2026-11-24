"""Source-backed talent summaries for compact character and comparison badges."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from skport.games.endfield.models import StatUnit, format_percent

GREEK_TIERS = "αβγδε"
ATTRIBUTE_NAMES = {39: "STR", 40: "AGI", 41: "INT", 42: "WILL"}


@dataclass(frozen=True)
class TalentBadge:
    """A single progression, retaining the original nodes and declared modifiers."""

    kind: str
    name: str
    node: Any
    nodes: tuple[Any, ...]
    unlocked: bool
    level: int
    max_level: int
    bonus: str | None = None
    stage: str = ""


def _name_stage(node: Any) -> tuple[str, str]:
    name = node.name.strip()
    if node.kind == "base" and name and name[-1] in GREEK_TIERS:
        return name[:-1].rstrip(), name[-1]
    return name, ""


def _key(node: Any) -> tuple[Any, ...]:
    name, _ = _name_stage(node)
    prefix, _, suffix = node.id.rpartition("_")
    if node.kind == "attribute":
        # Different properties and formula semantics are separate progressions.
        signature = tuple(sorted({(effect.id, effect.unit, effect.formula) for effect in node.effects}))
        return node.kind, name, node.icon.url, signature
    family = prefix if suffix.isdecimal() else node.id
    return node.kind, family, name


def _bonus(active: tuple[Any, ...]) -> str | None:
    if not active:
        return None
    # Never silently treat an unavailable or non-additive modifier as zero.
    if any(not node.effects for node in active):
        return None
    values: dict[tuple[int, StatUnit], list[float]] = {}
    for node in active:
        for effect in node.effects:
            if (
                effect.formula != "BaseAddition"
                or effect.unit is StatUnit.FACTOR
                or not math.isfinite(effect.value)
            ):
                return None
            values.setdefault((effect.id, effect.unit), []).append(effect.value)
    labels = []
    for (stat_id, unit), amounts in sorted(values.items()):
        value = math.fsum(amounts)
        text = format_percent(value) if unit is StatUnit.FRACTION else f"{value:g}"
        sign = "+" if value >= 0 else ""
        # Label multiple properties so that independent effects remain visible.
        label = ATTRIBUTE_NAMES.get(stat_id, f"#{stat_id}")
        suffix = f" {label}" if len(values) > 1 else ""
        labels.append(f"{sign}{text}{suffix}")
    return " / ".join(labels) or None


def compact_talents(model: Any) -> list[TalentBadge]:
    """Consolidate known progressions without calculating final character stats.

    Active additive attribute effects may be summed. Combat levels come from
    the supplied level/max fields. A base tier comes from an explicit Greek
    name suffix, falling back to the supplied level for canonical tiered nodes.
    IDs are used only to keep distinct progressions separate, never for levels.
    """
    grouped: dict[tuple[Any, ...], list[Any]] = {}
    for node in model.talents.nodes:
        grouped.setdefault(_key(node), []).append(node)
    unlocked_ids = set(model.talents.unlocked_node_ids)
    badges = []
    for group in grouped.values():
        nodes = tuple(group)
        active = tuple(node for node in nodes if node.unlocked or node.id in unlocked_ids)

        def rank(node: Any) -> tuple[int, int]:
            _, stage = _name_stage(node)
            return GREEK_TIERS.index(stage) + 1 if stage else node.level, node.max_level

        representative = max(active or nodes, key=rank)
        name, explicit_stage = _name_stage(representative)
        level = max((node.level for node in active), default=0)
        maximum = max((node.max_level for node in nodes), default=0)
        stage = ""
        if active and representative.kind == "base":
            if explicit_stage:
                stage = explicit_stage
            elif 1 <= level <= len(GREEK_TIERS):
                stage = GREEK_TIERS[level - 1]
        badges.append(
            TalentBadge(
                kind=representative.kind,
                name=name,
                node=representative,
                nodes=nodes,
                unlocked=bool(active),
                level=level,
                max_level=maximum,
                bonus=_bonus(active) if representative.kind == "attribute" else None,
                stage=stage,
            )
        )
    order = {"attribute": 0, "combat": 1, "base": 2}
    return sorted(badges, key=lambda badge: order.get(badge.kind, 3))
