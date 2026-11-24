"""Weapon progression uses exact applied levels and readable adjacent stat badges."""

from types import SimpleNamespace

import pytest
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    Gem,
    GemTerm,
    PlayerIdentity,
    Skill,
    StatBlock,
    StatUnit,
    StatValue,
    Weapon,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.rendering.templates.character import components as parts
from endfield_cards.utils.drawing import PageCanvas


def model() -> CharacterBuild:
    owner = PlayerIdentity(skport_id="owner", name="Owner", game_uid="game")
    return CharacterBuild(
        identity=CharacterIdentity(skport_id="operator"),
        name="Operator",
        owner=owner,
        stats=StatBlock(
            main_attribute=42,
            sub_attribute=41,
            values={
                41: StatValue(id=41, name="INT", value=307, unit=StatUnit.FLAT, is_sub=True),
                42: StatValue(id=42, name="WILL", value=862, unit=StatUnit.FLAT, is_main=True),
            },
        ),
    )


@pytest.mark.parametrize("layout", ["rows", "columns"])
def test_attribute_badges_follow_the_label_instead_of_the_cell_edge(monkeypatch, layout):
    data = model()
    c = PageCanvas("Character", context_for(data), header=False, size=(950, 650))
    labels, badges = {}, []
    original_text, original_tag = c.text, parts._role_tag

    def capture_text(x, y, value, **options):
        if str(value) in {"INT", "WILL"}:
            labels[str(value)] = (x, y, options["size"])
        return original_text(x, y, value, **options)

    def capture_tag(canvas, x, y, role):
        badges.append((role, x, y))
        return original_tag(canvas, x, y, role)

    monkeypatch.setattr(c, "text", capture_text)
    monkeypatch.setattr(parts, "_role_tag", capture_tag)
    parts.draw_stats(c, data, (10, 20, 910, 600), layout=layout)
    assert {role for role, *_ in badges} == {"Main", "Sub"}
    for role, x, y in badges:
        name = "WILL" if role == "Main" else "INT"
        label_x, label_y, size = labels[name]
        font = c.fonts.get(size, locale=c.context.locale, text=name)
        assert y == label_y and 0 <= x - label_x - c.draw.textlength(name, font=font) <= 16
    c.image.close()


def test_capsules_have_exact_white_yellow_count_and_tilt():
    data = model()
    c = PageCanvas("Character", context_for(data), header=False, dark=True, size=(230, 100))
    parts._level_capsules(c, 15, 20, 3, 6, 180)
    colors = {(244, 243, 238): "base", (255, 200, 0): "bonus"}
    columns = []
    for x in range(15, 195):
        values = {
            colors[pixel[:3]] for y in range(20, 33) if (pixel := c.image.getpixel((x, y)))[:3] in colors
        }
        columns.append(next(iter(values)) if values else None)
    groups = []
    previous = None
    for color in columns:
        if color is not None and color != previous:
            groups.append(color)
        previous = color
    assert groups == ["base"] * 3 + ["bonus"] * 6
    top = [x for x in range(15, 27) for y in range(20, 26) if c.image.getpixel((x, y))[:3] == (244, 243, 238)]
    low = [x for x in range(15, 27) for y in range(27, 33) if c.image.getpixel((x, y))[:3] == (244, 243, 238)]
    assert top and low and sum(top) / len(top) > sum(low) / len(low)
    c.image.close()


@pytest.mark.parametrize(
    "level,base,bonus,expected",
    [(9, 3, 6, (3, 6)), (5, 2, 3, (2, 3)), (9, 4, 5, (4, 5)), (0, 0, 0, (0, 0)), (9, 4, 6, None)],
)
def test_applied_levels_are_used_without_replacing_capped_bonus_with_raw_points(level, base, bonus, expected):
    skill = SimpleNamespace(level=level, base_level=base, bonus_level=bonus)
    gem = Gem(terms=[GemTerm(name="Same display label", points=6)])
    assert parts._weapon_level_split(skill, gem) == expected


def test_legacy_gem_snapshot_does_not_guess_split_from_a_matching_name():
    skill = Skill(name="Will", level=9)
    gem = Gem(terms=[GemTerm(name="Will", points=6)])
    assert parts._weapon_level_split(skill, gem) is None
    assert parts._weapon_level_split(skill, None) == (9, 0)


@pytest.mark.parametrize("box", [(15, 20, 831, 267), (15, 20, 545, 326)])
def test_weapon_and_essence_rows_pass_exact_applied_and_source_counts(monkeypatch, box):
    data = model()
    data.weapon = Weapon(
        name="Weapon",
        skills=[Skill(name="Will", level=9).model_copy(update={"base_level": 3, "bonus_level": 6})],
        gem=Gem(name="Essence", terms=[GemTerm(name="Will", points=6)]),
    )
    c = PageCanvas("Character", context_for(data), header=False, size=(950, 550))
    calls = []
    original = parts._level_capsules

    def capture(canvas, x, y, base, bonus, width):
        calls.append((base, bonus, x, y))
        return original(canvas, x, y, base, bonus, width)

    monkeypatch.setattr(parts, "_level_capsules", capture)
    parts.draw_weapon(c, data, box)
    assert [(base, bonus) for base, bonus, *_ in calls] == [(3, 6), (0, 6)]
    assert all(box[0] <= x < box[2] and box[1] <= y and y + 13 <= box[3] for _, _, x, y in calls)
    assert data.weapon.skills[0].level == 9 and data.weapon.gem.terms[0].points == 6
    c.image.close()
