"""Compact talent summaries preserve source effects, tiers and missing state."""

from __future__ import annotations

import pytest
from PIL import Image
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    ImageLinks,
    PlayerIdentity,
    SemanticLabel,
    StatModifier,
    StatUnit,
    TalentNode,
    TalentTree,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.rendering.templates.character import components as parts
from endfield_cards.rendering.templates.character.components import draw_talents
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.talents import compact_talents


def model(nodes: list[TalentNode], unlocked: list[str] | None = None) -> CharacterBuild:
    return CharacterBuild(
        identity=CharacterIdentity(skport_id="opaque-character", str_id="chr_same"),
        owner=PlayerIdentity(skport_id="source-owner", name="Source", game_uid="12345678"),
        element=SemanticLabel(key="char_property_pulse"),
        talents=TalentTree(nodes=nodes, unlocked_node_ids=unlocked or []),
    )


def attribute(identifier: str, amount: float, *, active: bool = True) -> TalentNode:
    return TalentNode(
        id=identifier,
        name="Stalwart",
        kind="attribute",
        level=1 if active else 0,
        unlocked=active,
        effects=[StatModifier(id=42, formula="BaseAddition", value=amount, unit=StatUnit.FLAT)],
    )


def progression(
    identifier: str, *, active: bool = True, kind: str = "combat", name: str = "Force"
) -> TalentNode:
    tier = int(identifier.rpartition("_")[2])
    return TalentNode(
        id=identifier,
        name=name,
        kind=kind,
        level=tier if active else 0,
        max_level=tier,
        unlocked=active,
    )


def compact_model() -> CharacterBuild:
    nodes = [attribute(f"attr_{index}", amount) for index, amount in enumerate((10, 15, 15, 20))]
    nodes += [progression(f"combat_{number}_{tier}") for number in range(2) for tier in (1, 2)]
    nodes += [
        TalentNode(
            id=f"base_{number}_{tier}",
            name=f"Workshop {number} {stage}",
            kind="base",
            level=1,
            max_level=1,
            unlocked=True,
        )
        for number in range(2)
        for tier, stage in ((1, "β"), (2, "γ"))
    ]
    return model(nodes)


def test_observed_attribute_sum_and_talent_progressions_remain_source_backed():
    source = compact_model()
    before = source.model_dump()
    badges = compact_talents(source)
    assert len(badges) == 5
    assert badges[0].bonus == "+60"
    assert len(badges[0].nodes) == 4
    assert [(badge.level, badge.max_level) for badge in badges[1:3]] == [(2, 2), (2, 2)]
    assert [badge.stage for badge in badges[3:]] == ["γ", "γ"]
    assert source.model_dump() == before


def test_locked_attribute_effect_is_excluded_but_unlocked_ids_are_respected():
    source = model([attribute("attr_1", 10), attribute("attr_2", 50, active=False)])
    assert compact_talents(source)[0].bonus == "+10"
    source.talents.unlocked_node_ids = ["attr_2"]
    assert compact_talents(source)[0].bonus == "+60"


@pytest.mark.parametrize(
    "formula,unit", [("BaseMultiplier", StatUnit.FRACTION), ("BaseAddition", StatUnit.FACTOR)]
)
def test_nonadditive_effects_never_become_an_attribute_total(formula, unit):
    node = attribute("attr_1", 10)
    node.effects[0] = StatModifier(id=42, formula=formula, value=1.5, unit=unit)
    assert compact_talents(model([node]))[0].bonus is None


def test_missing_effects_are_unavailable_and_multiple_properties_stay_labelled():
    empty = attribute("attr_1", 10)
    empty.effects = []
    assert compact_talents(model([empty]))[0].bonus is None
    multi = attribute("attr_2", 60)
    multi.effects += [StatModifier(id=41, formula="BaseAddition", value=20, unit=StatUnit.FLAT)]
    assert compact_talents(model([multi]))[0].bonus == "+20 INT / +60 WILL"


def test_different_units_do_not_merge_as_one_attribute_total():
    flat = attribute("attr_1", 10)
    fraction = attribute("attr_2", 0.2)
    fraction.effects[0] = StatModifier(id=42, formula="BaseAddition", value=0.2, unit=StatUnit.FRACTION)
    badges = compact_talents(model([flat, fraction]))
    assert len(badges) == 2
    assert [badge.bonus for badge in badges] == ["+10", "+20.0%"]


def test_tiers_never_come_from_identifier_suffixes_or_unlocked_counts():
    node = TalentNode(id="base_99", kind="base", level=1, max_level=1, unlocked=True)
    badge = compact_talents(model([node]))[0]
    assert badge.stage == "α"
    node.level = 0
    node.unlocked = False
    badge = compact_talents(model([node]))[0]
    assert badge.stage == "" and not badge.unlocked and badge.level == 0


def test_unobserved_combat_tier_keeps_its_actual_maximum():
    nodes = [progression("combat_1"), progression("combat_2", active=False)]
    badge = compact_talents(model(nodes))[0]
    assert badge.level == 1 and badge.max_level == 2
    assert badge.node.id == "combat_1"


@pytest.mark.parametrize(
    "box",
    [
        (36, 1227, 704, 1323),
        (48, 662, 525, 755),
        (43, 1732, 1057, 1830),
        (44, 860, 482, 1068),
    ],
)
def test_consolidated_badges_fit_each_showcase_and_preserve_source_art(box, monkeypatch):
    source = compact_model()
    images = {}
    for node in source.talents.nodes:
        node.icon = ImageLinks(skport=f"https://talent.example/{node.id}.png")
        images[node.icon.url] = Image.new("RGBA", (40, 40), (200, 170, 10, 120))
    # Attribute icon is shared by its progression, as in the API model.
    for node in source.talents.nodes[:4]:
        node.icon = source.talents.nodes[0].icon
    pixels_before = {url: pixels.tobytes() for url, pixels in images.items()}
    entries = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        entries.append((str(value), x, y, height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    c = PageCanvas("Character", context_for(source), header=False, size=(1920, 1950), assets=images)
    draw_talents(c, source, box)
    text = "\n".join(entry[0] for entry in entries)
    assert "+60" in text and "γ" in text and "12/12" in text
    assert "2/2" not in text
    assert all(box[0] <= x < box[2] and box[1] <= y and y + height <= box[3] for _, x, y, height in entries)
    assert pixels_before == {url: pixels.tobytes() for url, pixels in images.items()}
    c.image.close()


@pytest.mark.parametrize("level", [0, 1, 2])
@pytest.mark.parametrize("size", [14, 28, 42])
def test_combat_badge_draws_one_capsule_per_observed_level_without_numeric_overlay(level, size, monkeypatch):
    node = TalentNode(
        id="combat_99", kind="combat", name="Force", level=level, max_level=2, unlocked=level > 0
    )
    source = model([node])
    badge = compact_talents(source)[0]
    c = PageCanvas("Character", context_for(source), header=False, dark=True, size=(100, 100))
    text = []
    original = c.text

    def capture(x, y, value, **options):
        text.append(str(value))
        return original(x, y, value, **options)

    monkeypatch.setattr(c, "text", capture)
    before = c.image.copy()
    parts._talent_badge(c, source, badge, 20, 20, size)
    # Count separated white marks in the actual pixels, including compact badges.
    columns = [
        any(c.image.getpixel((x, y))[:3] == (244, 243, 238) for y in range(20, 20 + size))
        for x in range(20, 20 + size)
    ]
    count = sum(visible and (index == 0 or not columns[index - 1]) for index, visible in enumerate(columns))
    assert count == level
    assert text == []
    for box in (
        (0, 0, 100, 20),
        (0, 20 + size, 100, 100),
        (0, 20, 20, 20 + size),
        (20 + size, 20, 100, 20 + size),
    ):
        assert c.image.crop(box).tobytes() == before.crop(box).tobytes()
    assert source.talents.nodes[0].level == level
    before.close()
    c.image.close()


@pytest.mark.parametrize("level", [1, 2])
def test_tall_talent_layout_uses_observed_capsules_in_badges_and_named_rows(level, monkeypatch):
    source = model(
        [TalentNode(id="combat_99", kind="combat", name="Force", level=level, max_level=2, unlocked=True)]
    )
    c = PageCanvas("Character", context_for(source), header=False, size=(600, 350))
    calls = []
    original = parts._level_capsules

    def capture(canvas, x, y, base, bonus, width):
        calls.append((base, bonus, x, y))
        return original(canvas, x, y, base, bonus, width)

    monkeypatch.setattr(parts, "_level_capsules", capture)
    box = (40, 20, 478, 228)
    draw_talents(c, source, box)
    assert [(base, bonus) for base, bonus, *_ in calls] == [(level, 0), (level, 0)]
    assert all(box[0] <= x < box[2] and box[1] <= y and y + 13 <= box[3] for _, _, x, y in calls)
    c.image.close()
