"""Unit-aware character components preserve observed build state and supplied art."""

from __future__ import annotations

from typing import Any

import pytest
from PIL import Image
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    Equipment,
    EquipmentSet,
    Gem,
    GemTerm,
    ImageLinks,
    ItemSummary,
    PlayerIdentity,
    SemanticLabel,
    Skill,
    StatBlock,
    StatLine,
    StatModifier,
    StatUnit,
    StatValue,
    TalentNode,
    TalentTree,
    Weapon,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.rendering.templates.character import components as parts
from endfield_cards.utils.drawing import PageCanvas


def link(name: str) -> ImageLinks:
    return ImageLinks(skport=f"https://build.example.test/{name}.png")


def build() -> CharacterBuild:
    values = {
        1: StatValue(id=1, name="HP", value=5990, unit=StatUnit.FLAT),
        2: StatValue(id=2, name="ATK", value=7379, unit=StatUnit.FLAT),
        3: StatValue(id=3, name="DEF", value=140, unit=StatUnit.FLAT),
        4: StatValue(id=4, name="Physical Damage Taken", value=1, unit=StatUnit.FACTOR),
        9: StatValue(id=9, name="Critical Rate", value=0.05, unit=StatUnit.FRACTION),
        10: StatValue(id=10, name="Critical Damage", value=0.5, unit=StatUnit.FRACTION),
        30: StatValue(id=30, name="Treatment Received", value=0.862, unit=StatUnit.FRACTION),
        39: StatValue(id=39, name="Strength", value=99, unit=StatUnit.FLAT),
        40: StatValue(id=40, name="Agility", value=99, unit=StatUnit.FLAT),
        41: StatValue(id=41, name="Intellect", value=307, unit=StatUnit.FLAT, is_sub=True),
        42: StatValue(id=42, name="Will", value=862, unit=StatUnit.FLAT, is_main=True),
        44: StatValue(id=44, name="Ultimate Gain", value=1, unit=StatUnit.FRACTION),
        52: StatValue(id=52, name="Electric Damage", value=0.655, unit=StatUnit.FRACTION),
        999: StatValue(id=999, name="Future unknown property", value=12, unit=StatUnit.NUMBER),
    }
    owner = PlayerIdentity(skport_id="social-owner", name="Source Owner", game_uid="4572346170")
    effects = [
        StatModifier(id=42, formula="BaseAddition", value=156, unit=StatUnit.FLAT),
        StatModifier(id=2, formula="BaseMultiplier", value=0.39, unit=StatUnit.FRACTION),
    ]
    pieces = []
    for index, slot in enumerate(("body", "arms", "accessory1", "accessory2")):
        pieces.append(
            Equipment(
                slot=slot,
                id=f"piece-{index}",
                name=f"Observed equipment {index}",
                rarity=5,
                defense=56 - index * 7,
                icon=link(f"piece-{index}"),
                enhance_count=9,
                max_enhance=9,
                stat_lines=[
                    StatLine(name="Will", value=113, unit=StatUnit.FLAT, level=3, max_level=3, stat_ids=[42]),
                    StatLine(
                        name="Intellect", value=75, unit=StatUnit.FLAT, level=3, max_level=3, stat_ids=[41]
                    ),
                    StatLine(
                        name="Cryo & Electric DMG",
                        value=0.1495,
                        unit=StatUnit.FRACTION,
                        level=3,
                        max_level=3,
                        stat_ids=[53, 52],
                    ),
                ],
            )
        )
    return CharacterBuild(
        identity=CharacterIdentity(skport_id="opaque-character", str_id="chr_0030_zhuangfy", template_id=46),
        owner=owner,
        name="Zhuang Fangyi",
        level=67,
        max_level=80,
        evolution=4,
        potential=2,
        rarity=6,
        profession=SemanticLabel(key="profession_assault", name="Striker", icons=link("profession")),
        element=SemanticLabel(key="char_property_pulse", name="Electric", icons=link("element")),
        weapon_type=SemanticLabel(key="funnel", name="Arts Unit"),
        stats=StatBlock(values=values, main_attribute=42, sub_attribute=41),
        skills=[
            Skill(
                id=f"skill-{index}",
                name=f"Observed skill {index}",
                icon=link(f"skill-{index}"),
                level=9 + index,
                max_level=12,
            )
            for index in range(4)
        ],
        talents=TalentTree(
            nodes=[
                TalentNode(
                    id=f"talent-{index}",
                    name=f"Observed talent {index}",
                    kind=("attribute", "combat", "base")[index // 4],
                    icon=link(f"talent-{index}"),
                    unlocked=index != 11,
                )
                for index in range(12)
            ]
        ),
        weapon=Weapon(
            name="Observed weapon",
            level=70,
            refinement=3,
            breakthrough=4,
            rarity=6,
            base_attack=510,
            images=link("weapon"),
            effects=effects,
            skills=[
                Skill(id="will", name="Will [L]", level=9, max_level=9, effects=effects[:1]),
                Skill(id="atk", name="ATK [L]", level=9, max_level=9, effects=effects[1:]),
            ],
            gem=Gem(
                name="Observed Essence",
                rarity=5,
                icon=link("gem-badge"),
                base_icon=link("gem-base"),
                terms=[
                    GemTerm(name="Will", points=6),
                    GemTerm(name="ATK", points=6),
                    GemTerm(name="Suppression", points=3),
                ],
            ),
        ),
        equipment=pieces,
        equipment_sets=[EquipmentSet(name="Observed Set", pieces=3, required_pieces=3)],
        tactical_item=ItemSummary(name="Observed Capsule", icon=link("tactical")),
    )


class Images(dict[str, Image.Image]):
    def __init__(self, model: CharacterBuild) -> None:
        links = [
            model.profession.icons.url,
            model.element.icons.url,
            model.weapon.images.url,
            model.weapon.gem.icon.url,
            model.weapon.gem.base_icon.url,
            model.tactical_item.icon.url,
        ]
        links.extend(skill.icon.url for skill in model.skills)
        links.extend(node.icon.url for node in model.talents.nodes)
        links.extend(piece.icon.url for piece in model.equipment)
        super().__init__({url: Image.new("RGBA", (32, 48), (37, 121, 194, 255)) for url in links if url})
        self.requested: set[str] = set()

    def get(self, key: Any, default: Any = None) -> Any:
        if isinstance(key, str):
            self.requested.add(key)
        return super().get(key, default)


@pytest.fixture
def text_log(monkeypatch):
    entries = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        entries.append((str(value), x, y, height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return entries


def test_stats_selection_preserves_units_and_avoids_neutral_unknown_fields():
    model = build()
    rows = parts.stats_rows(model)
    assert [stat.id for stat in rows[:7]] == list(parts.CORE_IDS)
    assert {9, 10, 30, 44, 52}.issubset({stat.id for stat in rows})
    assert {4, 999}.isdisjoint({stat.id for stat in rows})
    assert parts.display_value(model.stats.values[1]) == "5,990"
    assert parts.display_value(model.stats.values[44]) == "100.0%"
    assert parts.display_value(model.stats.values[52]) == "65.5%"
    model.stats = None
    assert parts.stats_rows(model) == []


@pytest.mark.parametrize("layout,box", [("rows", (15, 25, 528, 570)), ("columns", (15, 25, 831, 387))])
def test_stats_boxes_show_source_values_and_attribute_roles(layout, box, text_log):
    model = build()
    c = PageCanvas("Character", context_for(model), header=False, size=(1000, 650))
    parts.draw_stats(c, model, box, layout=layout)
    text = "\n".join(entry[0] for entry in text_log)
    for expected in ("5,990", "7,379", "140", "99", "307", "862", "100.0%", "65.5%", "86.2%", "Main", "Sub"):
        assert expected in text
    assert all(box[0] <= x < box[2] and box[1] <= y and y + height <= box[3] for _, x, y, height in text_log)
    c.image.close()


@pytest.mark.parametrize("box", [(15, 20, 831, 267), (15, 20, 545, 326)])
def test_weapon_preserves_observed_effects_and_composed_essence(box, text_log):
    model = build()
    images = Images(model)
    original = {key: image.tobytes() for key, image in images.items()}
    c = PageCanvas("Character", context_for(model), header=False, size=(1000, 600), assets=images)
    parts.draw_weapon(c, model, box)
    text = "\n".join(entry[0] for entry in text_log)
    for expected in (
        "Observed weapon",
        "Lv 70",
        "R3",
        "B4",
        "510",
        "+156",
        "+39.0%",
        "Observed Essence",
        "Suppression",
        "+6",
        "+3",
    ):
        assert expected in text
    assert model.weapon.images.url in images.requested
    assert {model.weapon.gem.icon.url, model.weapon.gem.base_icon.url}.issubset(images.requested)
    assert "BaseAddition" not in text and "BaseMultiplier" not in text
    assert all(box[0] <= x < box[2] and box[1] <= y and y + height <= box[3] for _, x, y, height in text_log)
    assert original == {key: image.tobytes() for key, image in images.items()}
    c.image.close()


@pytest.mark.parametrize("columns,box", [(4, (15, 20, 831, 340)), (2, (15, 20, 611, 500))])
def test_equipment_preserves_all_slots_defense_and_actual_enhancement_bounds(columns, box, text_log):
    model = build()
    images = Images(model)
    c = PageCanvas("Character", context_for(model), header=False, size=(1000, 600), assets=images)
    parts.draw_equipment(c, model, box, columns=columns)
    text = "\n".join(entry[0] for entry in text_log)
    for index in range(4):
        assert f"Observed equipment {index}" in text
        assert model.equipment[index].icon.url in images.requested
        assert f"DEF {56 - index * 7}" in text
    assert text.count("9/9") == 4
    assert "3/3" in text and "15.0%" in text and "113" in text and "75" in text
    assert "Observed Set 3/3" in text and "Observed Capsule" in text
    assert all(box[0] <= x < box[2] and box[1] <= y and y + height <= box[3] for _, x, y, height in text_log)
    c.image.close()


def test_talent_group_state_preserves_colored_source_images(text_log):
    model = build()
    images = Images(model)
    c = PageCanvas("Character", context_for(model), header=False, size=(750, 200), assets=images)
    original = {key: image.tobytes() for key, image in images.items()}
    parts.draw_talents(c, model, (15, 15, 670, 105))
    text = "\n".join(entry[0] for entry in text_log)
    assert "11/12" in text
    assert all(group in text for group in ("Attribute", "Combat", "Base"))
    assert all(node.icon.url in images.requested for node in model.talents.nodes)
    assert original == {key: image.tobytes() for key, image in images.items()}
    assert all(15 <= x < 670 and 15 <= y and y + height <= 105 for _, x, y, height in text_log)
    c.image.close()


def test_skill_levels_use_the_observed_maximum_and_fit_the_component(text_log):
    model = build()
    images = Images(model)
    c = PageCanvas("Character", context_for(model), header=False, size=(900, 250), assets=images)
    parts.draw_skills(c, model, (15, 20, 831, 133))
    text = "\n".join(entry[0] for entry in text_log)
    assert all(f"Observed skill {index}" in text for index in range(4))
    assert all(f"{9 + index}/12" in text for index in range(4))
    assert all(skill.icon.url in images.requested for skill in model.skills)
    assert all(15 <= x < 831 and 20 <= y and y + height <= 133 for _, x, y, height in text_log)
    c.image.close()


def test_missing_equipment_values_remain_unavailable(text_log):
    model = build()
    model.equipment = [
        Equipment(
            slot="body",
            name="Partial piece",
            enhance_count=9,
            stat_lines=[StatLine(name="Unknown affix", value=None, level=1, max_level=7)],
        )
    ]
    c = PageCanvas("Character", context_for(model), header=False, size=(600, 450))
    parts.draw_equipment(c, model, (10, 15, 540, 400), columns=1)
    text = "\n".join(entry[0] for entry in text_log)
    assert "DEF —" in text and "1/7" in text
    assert "9/3" not in text and "9/9" not in text and "DEF 0" not in text
    c.image.close()


def test_light_weapon_palette_is_restored_after_drawing_and_failure(monkeypatch):
    model = build()
    c = PageCanvas("Character", context_for(model), header=False, size=(900, 500), assets=Images(model))
    palette = c.panel_color, c.fg, c.muted, c.line
    parts.draw_weapon(c, model, (15, 20, 831, 267))
    assert (c.panel_color, c.fg, c.muted, c.line) == palette

    def fail(*args, **kwargs):
        assert c.fg == "#F2F3F6" and c.panel_color == "#20242C"
        raise RuntimeError("injected draw failure")

    monkeypatch.setattr(parts, "_draw_weapon", fail)
    with pytest.raises(RuntimeError, match="injected draw failure"):
        parts.draw_weapon(c, model, (15, 20, 831, 267))
    assert (c.panel_color, c.fg, c.muted, c.line) == palette
    c.image.close()


def test_two_column_skill_layout_and_tall_talent_names_fit(text_log):
    model = build()
    images = Images(model)
    c = PageCanvas("Character", context_for(model), header=False, size=(1100, 550), assets=images)
    skill_box = (15, 20, 611, 210)
    parts.draw_skills(c, model, skill_box, columns=2)
    assert all(skill.name in "\n".join(entry[0] for entry in text_log) for skill in model.skills)
    assert all(
        skill_box[0] <= x < skill_box[2] and skill_box[1] <= y and y + height <= skill_box[3]
        for _, x, y, height in text_log
    )
    text_log.clear()
    talent_box = (15, 240, 453, 448)
    parts.draw_talents(c, model, talent_box)
    assert "Observed talent 4" in "\n".join(entry[0] for entry in text_log)
    assert all(
        talent_box[0] <= x < talent_box[2] and talent_box[1] <= y and y + height <= talent_box[3]
        for _, x, y, height in text_log
    )
    c.image.close()


def test_identity_keeps_source_element_label_and_visible_light_badge(text_log):
    model = build()
    images = Images(model)
    c = PageCanvas("Character", context_for(model), header=False, size=(900, 400), assets=images)
    parts.draw_identity(c, model, 20, 20, 700)
    text = "\n".join(entry[0] for entry in text_log)
    assert "Striker · Electric" in text and "67/80" in text and "P2" in text
    assert model.element.icons.url in images.requested
    assert c.image.getpixel((20 + 42, 20 + 109 + 16))[:3] != (242, 241, 236)
    c.image.close()
