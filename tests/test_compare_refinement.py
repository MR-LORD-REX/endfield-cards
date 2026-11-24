"""Comparison preserves two observed builds without fabricating missing values."""

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
    ModelIssue,
    PlayerIdentity,
    SemanticLabel,
    Skill,
    StatBlock,
    StatLine,
    StatUnit,
    StatValue,
    Weapon,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.assets.store import AssetStore
from endfield_cards.errors import DataValidationError, DownloadError, OwnerMismatchError
from endfield_cards.models import Artwork, OwnerIdentity, RenderContext, RenderIssue
from endfield_cards.rendering import RenderEngine
from endfield_cards.rendering.templates import compare
from endfield_cards.rendering.templates.comparison._shared import compare_rows, equipment_slots, skill_pairs
from endfield_cards.utils.drawing import PageCanvas


def image_link(name: str) -> ImageLinks:
    return ImageLinks(skport=f"https://compare.example.test/{name}.png")


def comparison_build(*, second: bool = False) -> CharacterBuild:
    """Retain the same opaque character ID across independently owned builds."""
    prefix = "Second" if second else "First"
    values = {
        key: StatValue(id=key, name=name, value=value, unit=StatUnit.FLAT)
        for key, name, value in (
            (1, "HP", 5900),
            (2, "ATK", 4112),
            (3, "DEF", 140),
            (39, "Strength", 82),
            (40, "Agility", 312),
            (41, "Intellect", 671),
            (42, "Will", 105),
        )
    }
    values.update(
        {
            9: StatValue(id=9, name="Critical Rate", value=0.15, unit=StatUnit.FRACTION),
            10: StatValue(id=10, name="Critical Damage", value=0.5, unit=StatUnit.FRACTION),
            44: StatValue(id=44, name="Ultimate Gain", value=1, unit=StatUnit.FRACTION),
            52: StatValue(id=52, name="Electric Damage", value=0.4, unit=StatUnit.FRACTION),
        }
    )
    slots = ("arms", "accessory1", "accessory2") if second else ("body", "arms", "accessory1", "accessory2")
    return CharacterBuild(
        identity=CharacterIdentity(
            skport_id="same-opaque-character", str_id="chr_0030_zhuangfy", template_id=46
        ),
        owner=PlayerIdentity(
            skport_id="owner-two" if second else "owner-one",
            game_uid="6397007521" if second else "4572346170",
            name=f"{prefix} Owner",
        ),
        name="Zhuang Fangyi",
        level=67 if second else 90,
        max_level=90,
        evolution=4,
        potential=2 if second else 5,
        rarity=6,
        profession=SemanticLabel(key="profession_assault", name="Striker", icons=image_link("profession")),
        element=SemanticLabel(key="char_property_pulse", name="Electric", icons=image_link("element")),
        weapon_type=SemanticLabel(key="funnel", name="Arts Unit"),
        stats=StatBlock(values=values, main_attribute=41, sub_attribute=40),
        skills=[
            Skill(
                id=f"skill-{index}",
                name=f"Combat skill {index}",
                level=9 + index,
                max_level=12,
                icon=image_link(f"skill-{index}"),
            )
            for index in range(4)
        ],
        weapon=Weapon(
            name=f"{prefix} weapon",
            level=70 if second else 90,
            refinement=3,
            breakthrough=4,
            base_attack=510,
            rarity=6,
            images=image_link(f"{prefix}-weapon"),
            skills=[Skill(id="weapon-will", name="Will [L]", level=9, max_level=9)],
            gem=Gem(
                name=f"{prefix} Essence",
                icon=image_link(f"{prefix}-essence"),
                terms=[GemTerm(name="Will", points=6), GemTerm(name="ATK", points=3)],
            ),
        ),
        equipment=[
            Equipment(
                slot=slot,
                name=f"{prefix} gear {index}",
                rarity=5,
                defense=56 - index * 7,
                enhance_count=9,
                max_enhance=9,
                icon=image_link(f"{prefix}-gear-{index}"),
                stat_lines=[
                    StatLine(
                        name="Intellect", value=113, unit=StatUnit.FLAT, stat_ids=[41], level=3, max_level=3
                    )
                ],
            )
            for index, slot in enumerate(slots)
        ],
        equipment_sets=[EquipmentSet(name=f"{prefix} Set", pieces=3, required_pieces=3)],
    )


@pytest.fixture
def text_log(monkeypatch):
    entries = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        entries.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return entries


def test_comparison_uses_aligned_observed_union_and_second_minus_first_deltas():
    first, second = comparison_build(), comparison_build(second=True)
    second.stats.values[1].value = 7123
    second.stats.values.pop(2)
    second.stats.values[9].value = 0.25
    second.stats.values[10].value = 0.4
    second.stats.values[50] = StatValue(id=50, name="Physical Damage", value=0.1, unit=StatUnit.FRACTION)
    first.stats.values[777] = StatValue(id=777, name="Future multiplier", value=1.1, unit=StatUnit.FACTOR)
    second.stats.values[777] = StatValue(id=777, name="Future multiplier", value=1.3, unit=StatUnit.FACTOR)
    second.stats.values[999] = StatValue(id=999, name="Future property", value=12, unit=StatUnit.NUMBER)
    rows = compare_rows(first, second)
    assert [row.stat_id for row in rows[:7]] == [1, 2, 3, 39, 40, 41, 42]
    assert len({row.stat_id for row in rows}) == len(rows)
    by_id = {row.stat_id: row for row in rows}
    assert by_id[1].delta == 1223 and by_id[1].delta_text == "+1,223"
    assert by_id[9].delta == pytest.approx(0.1) and by_id[9].delta_text == "+10.0 pp"
    assert by_id[10].delta == pytest.approx(-0.1) and by_id[10].delta_text == "-10.0 pp"
    assert by_id[777].delta == pytest.approx(0.2) and by_id[777].delta_text == "+0.2×"
    assert by_id[2].first.value == 4112 and by_id[2].second is None
    assert by_id[2].delta is None and by_id[2].delta_text == "—"
    assert by_id[50].first is None and by_id[50].second.value == pytest.approx(0.1)
    assert by_id[999].first is None and by_id[999].second.value == 12
    assert by_id[50].delta is None and by_id[999].delta is None


def test_comparison_distinguishes_equal_zero_from_missing_or_incompatible_units():
    first, second = comparison_build(), comparison_build(second=True)
    first.stats.values[3].value = second.stats.values[3].value = 0
    second.stats.values[9].unit = StatUnit.FLAT
    first.stats.values[52].value = 0
    second.stats.values[52].value = 0.3
    by_id = {row.stat_id: row for row in compare_rows(first, second)}
    assert by_id[3].first.value == by_id[3].second.value == 0
    assert by_id[3].delta == 0 and by_id[3].delta_text == "0"
    assert by_id[9].delta is None and by_id[9].delta_text == "—"
    assert by_id[52].first.value == 0 and by_id[52].delta == pytest.approx(0.3)
    second.stats = None
    rows = compare_rows(first, second)
    assert rows and all(row.second is None and row.delta is None for row in rows)
    first.stats = None
    assert compare_rows(first, second) == []


@pytest.mark.parametrize(
    "first_value,second_value,expected",
    [(0.1, 0.1005, "+0.1 pp"), (0.1005, 0.1, "-0.1 pp"), (0.1, 0.0999, "0.0 pp"), (0.1, 0.1001, "0.0 pp")],
)
def test_fraction_delta_uses_sdk_rounding_and_neutralizes_rounded_zero(first_value, second_value, expected):
    first, second = comparison_build(), comparison_build(second=True)
    first.stats.values[9].value, second.stats.values[9].value = first_value, second_value
    row = next(row for row in compare_rows(first, second) if row.stat_id == 9)
    assert row.delta == pytest.approx(second_value - first_value)
    assert row.delta_text == expected


def test_comparison_hides_equal_internal_and_neutral_bonus_properties():
    first, second = comparison_build(), comparison_build(second=True)
    for model in (first, second):
        model.stats.values[8] = StatValue(id=8, name="Stat 8", value=1, unit=StatUnit.NUMBER)
        model.stats.values[4] = StatValue(id=4, name="Physical Damage Taken", value=1, unit=StatUnit.FACTOR)
        model.stats.values[17] = StatValue(id=17, name="Basic Attack Damage", value=0, unit=StatUnit.FRACTION)
    assert {8, 4, 17}.isdisjoint(row.stat_id for row in compare_rows(first, second))


def test_comparison_accepts_equal_builds_and_same_owner_snapshots():
    first = comparison_build()
    second = first.model_copy(deep=True)
    compare.validate_pair(first, second)
    assert all(row.delta == 0 for row in compare_rows(first, second))
    second.identity.template_id = 47
    with pytest.raises(DataValidationError) as error:
        compare.validate_pair(first, second)
    assert error.value.code == "character_mismatch"


def test_skill_and_equipment_comparison_align_canonical_ids_and_fixed_slots():
    first, second = comparison_build(), comparison_build(second=True)
    second.skills = list(reversed(second.skills[:-1]))
    second.skills[0].level = 1
    pairs = skill_pairs(first, second)
    assert [left.id for left, _ in pairs] == [skill.id for skill in first.skills]
    assert all(left.id == right.id for left, right in pairs if right is not None)
    assert pairs[2][1].level == 1 and pairs[3][1] is None
    second.equipment.reverse()
    slots = equipment_slots(second)
    assert [slot for slot, _ in slots] == ["body", "arms", "accessory1", "accessory2"]
    assert slots[0][1] is None
    assert all(str(piece.slot) == slot for slot, piece in slots if piece is not None)


@pytest.mark.parametrize("variant", ["field", "dossier", "terminal", "portrait"])
def test_concise_comparison_preserves_both_real_builds_and_partial_gear(variant, text_log):
    first, second = comparison_build(), comparison_build(second=True)
    second.equipment[1].defense = None
    second.equipment[1].stat_lines[0].value = None
    before = first.model_dump(), second.model_dump()
    pages = compare.render(first, second, context_for(first), context_for(second), variant=variant)
    assert len(pages) == 1 and pages[0].size == (2160, 1440)
    text = "\n".join(entry[0] for entry in text_log)
    for owner, uid in (("First Owner", "4572346170"), ("Second Owner", "6397007521")):
        assert owner in text and f"UID {uid}" in text
    for model in (first, second):
        assert model.weapon.name in text and model.weapon.gem.name in text
        assert all(piece.name in text for piece in model.equipment)
        assert all(skill.name in text for skill in model.skills)
    assert "First Set" in text and "Second Set" in text and "3/3" in text
    assert "DEF —" in text and "9/9" in text and "113" in text
    assert "INT · Main" in text and "AGI · Sub" in text
    assert "akef-cards" in text and "endfield-cards" in text
    assert "ahead" not in text.casefold() and "winner" not in text.casefold()
    assert all(
        0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in text_log
    )
    assert before == (first.model_dump(), second.model_dump())
    pages[0].close()


@pytest.mark.parametrize("variant", ["field", "dossier"])
def test_both_custom_artworks_affect_the_card_and_keep_caller_pixels(variant):
    first, second = comparison_build(), comparison_build(second=True)
    first_art = Image.new("RGBA", (400, 700), (223, 65, 60, 205))
    second_art = Image.new("RGBA", (800, 300), (42, 112, 220, 235))
    replacement = Image.new("RGBA", (500, 500), (36, 197, 99, 225))
    original = first_art.tobytes(), second_art.tobytes(), replacement.tobytes()

    def pixels(left, right):
        image = compare.render(
            first,
            second,
            context_for(first),
            context_for(second),
            variant=variant,
            assets={"custom_art": left, "second_custom_art": right},
            artwork=Artwork(left, fit="cover", focal_point=(0.2, 0.8)),
            second_artwork=Artwork(right, fit="contain", focal_point=(0.8, 0.2)),
        )[0]
        result = image.tobytes()
        image.close()
        return result

    baseline = pixels(first_art, second_art)
    assert baseline != pixels(replacement, second_art)
    assert baseline != pixels(first_art, replacement)
    assert original == (first_art.tobytes(), second_art.tobytes(), replacement.tobytes())
    for artwork in (first_art, second_art, replacement):
        artwork.close()


def test_oversized_future_records_keep_readable_single_card_and_explicit_overflow(text_log):
    first, second = comparison_build(), comparison_build(second=True)
    for key in range(1000, 1100):
        first.stats.values[key] = StatValue(id=key, name=f"Future property {key}", value=key)
    first.skills.extend(Skill(id=f"future-{index}", name=f"Future skill {index}") for index in range(20))
    assert len(compare_rows(first, second)) > 100
    pages = compare.render(first, second, context_for(first), context_for(second))
    assert len(pages) == 1
    text = "\n".join(entry[0] for entry in text_log)
    assert "properties" in text and "+16 skills" in text
    assert all(
        0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in text_log
    )
    pages[0].close()


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["canonical", "owner"])
async def test_pair_and_owner_validation_happens_before_any_custom_art_load(monkeypatch, failure):
    calls = []

    async def unexpected_load(self, source: Any):
        calls.append(source)
        raise AssertionError("Invalid comparison must fail before resource loading")

    monkeypatch.setattr(AssetStore, "load", unexpected_load)
    first, second = comparison_build(), comparison_build(second=True)
    options = {"art": b"invalid-image", "second_art": b"invalid-image"}
    if failure == "canonical":
        second.identity.str_id = "different-character"
        expected = DataValidationError
    else:
        options["second_context"] = RenderContext(OwnerIdentity("Wrong Owner", "different-uid"))
        expected = OwnerMismatchError
    async with RenderEngine() as cards:
        with pytest.raises(expected):
            await cards.render_compare(first, second, **options)
    assert calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("optional_image_failure", [False, True])
async def test_comparison_results_preserve_both_sdk_issue_lists_before_asset_fallback(
    monkeypatch, optional_image_failure
):
    calls = []
    first, second = (
        CharacterBuild(
            identity=CharacterIdentity(skport_id="opaque-character", str_id="same-character"),
            owner=PlayerIdentity(skport_id=f"owner-{index}", name=f"Owner {index}", game_uid=f"game-{index}"),
            name="Same character",
            issues=[ModelIssue(code=f"source-{index}", message=f"Observed issue {index}")],
        )
        for index in (1, 2)
    )
    first.issues.append(ModelIssue(code="first-extra", message="Observed first-build detail"))
    if optional_image_failure:
        first.images.splash = image_link("optional-missing")
    before = first.model_dump(), second.model_dump()

    async def source_image(self, url, *, retain=True):
        calls.append(url)
        if optional_image_failure:
            raise DownloadError("Simulated unavailable source")
        raise AssertionError("Source issue propagation must not require HTTP")

    monkeypatch.setattr(AssetStore, "get", source_image)
    async with RenderEngine() as cards:
        pages = await cards.render_compare(first, second)
    assert len(pages) == 1
    issues = pages[0].issues
    assert issues[:3] == (
        RenderIssue("source-1", "Observed issue 1"),
        RenderIssue("first-extra", "Observed first-build detail"),
        RenderIssue("source-2", "Observed issue 2"),
    )
    if optional_image_failure:
        assert calls and all(url == first.images.splash.url for url in calls)
        assert issues[3:] and all(issue.code == "download_failed" for issue in issues[3:])
    else:
        assert calls == [] and len(issues) == 3
    assert before == (first.model_dump(), second.model_dump())
