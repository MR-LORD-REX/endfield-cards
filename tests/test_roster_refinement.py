"""Concise full-roster layout, observed build state and explicit extra exports."""

import pytest
from PIL import Image
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    CharacterImages,
    Equipment,
    Gem,
    ImageLinks,
    PlayerCard,
    PlayerIdentity,
    SemanticLabel,
    Skill,
    TalentNode,
    TalentTree,
    Weapon,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.templates import roster
from endfield_cards.rendering.templates.roster import _shared as parts
from endfield_cards.utils.drawing import PageCanvas


def link(name):
    return ImageLinks(skport=f"https://roster.example.test/{name}.png")


def operator(owner, index):
    return CharacterBuild(
        identity=CharacterIdentity(skport_id=f"opaque-{index}", str_id=f"canonical-{index}"),
        owner=owner,
        name=f"Operator {index}",
        level=67,
        max_level=80,
        evolution=3,
        potential=2,
        rarity=5,
        images=CharacterImages(avatar=link(f"avatar-{index}"), portrait=link(f"portrait-{index}")),
        profession=SemanticLabel(key="profession_assault", name="Striker", icons=link("profession")),
        element=SemanticLabel(key="char_property_pulse", name="Electric", icons=link("element")),
        skills=[
            Skill(
                id=f"skill-{index}-{key}",
                level=6,
                max_level=7,
                name=f"Skill {key}",
                icon=link(f"skill-{key}"),
            )
            for key in range(4)
        ],
        talents=TalentTree(nodes=[TalentNode(id=f"talent-{key}", unlocked=key < 4) for key in range(8)]),
        weapon=Weapon(
            name=f"Weapon {index}",
            level=51,
            breakthrough=2,
            refinement=3,
            rarity=5,
            images=link(f"weapon-{index}"),
            gem=Gem(name=f"Essence {index}", icon=link("essence")),
        ),
        equipment=[
            Equipment(slot=slot, icon=link(f"gear-{slot}"), enhance_count=0, max_enhance=5)
            for slot in ("body", "arms", "accessory1", "accessory2")
        ],
    )


@pytest.fixture
def owner():
    return PlayerIdentity(skport_id="social", name="Owned Account", game_uid="1234567890")


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


@pytest.mark.parametrize("variant", ["light", "dark"])
@pytest.mark.parametrize("count", [0, 1, 13, 24, 48, 72])
def test_normal_full_rosters_keep_every_operator_on_one_image(count, variant, owner, text_log):
    model = PlayerCard(
        player=owner,
        characters=[operator(owner, index) for index in range(count)],
        source_scope="owner",
        roster_complete=True,
    )
    pages = roster.render(model, context_for(model), variant=variant)
    assert len(pages) == 1 and pages[0].size == parts.page_size(count)
    assert pages[0].width * pages[0].height < 13_000_000
    values = [entry[0] for entry in text_log]
    assert [value for value in values if value.startswith("Operator ")] == [
        f"Operator {index}" for index in range(count)
    ]
    assert "Owned Account" in values and any("UID 1234567890" in value for value in values)
    assert any("akef-cards" in value and "endfield-cards" in value for value in values)
    assert any("Complete" in value for value in values)
    assert all(
        0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in text_log
    )
    pages[0].close()


def test_extreme_roster_is_bounded_without_dropping_last_operator(owner, text_log):
    model = PlayerCard(
        player=owner, characters=[operator(owner, index) for index in range(73)], source_scope="owner"
    )
    pages = roster.render(model, context_for(model))
    assert len(pages) == 2 and [page.size for page in pages] == [parts.page_size(72), parts.page_size(1)]
    values = [entry[0] for entry in text_log]
    assert "Operator 72" in values and values.count("Owned Account") == 4
    for page in pages:
        page.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_actual_skill_talent_weapon_gear_units_and_missing_state_remain_honest(variant, owner, text_log):
    item = operator(owner, 0)
    item.equipment = item.equipment[1:]
    item.equipment[0].max_enhance = None
    item.weapon.gem = None
    model = PlayerCard(player=owner, characters=[item], source_scope="owner")
    before = model.model_dump()
    pages = roster.render(model, context_for(model), variant=variant)
    text = "\n".join(entry[0] for entry in text_log)
    assert "Lv 67/80 · E3 · P2" in text and "6/7" in text and "Talents 4/8" in text
    assert "Lv 51 · B2 · R3" in text and "Essence · Unavailable" in text
    assert "0/5" in text and "0/9" not in text and "—" in text
    assert "0/0" not in text
    assert before == model.model_dump()
    pages[0].close()


def test_empty_and_absent_build_details_do_not_turn_into_zero_state(owner, text_log):
    item = CharacterBuild(identity=CharacterIdentity(skport_id="partial"), name="Partial", owner=owner)
    pages = roster.render([item], context_for(owner, source_scope="supplied"))
    text = "\n".join(entry[0] for entry in text_log)
    assert (
        "Skills · Unavailable" in text and "Talents · Unavailable" in text and "Weapon · Unavailable" in text
    )
    assert "Talents 0/12" not in text and "Skills 0" not in text and "Lv 0" not in text
    pages[0].close()


def test_no_automatic_identity_appendix_and_explicit_details_keep_source_text(owner, text_log):
    name = "非常に長い名前" * 15 + "TAIL"
    item = operator(owner, 0)
    item.name = name
    pages = roster.render([item], context_for(owner))
    assert len(pages) == 1
    pages[0].close()
    text_log.clear()
    pages = roster.render([item], context_for(owner), details=True)
    assert len(pages) > 1 and any("TAIL" in value for value, *_ in text_log)
    for page in pages:
        page.close()


def test_selection_keeps_source_order_and_never_claims_full_roster(owner, text_log):
    model = PlayerCard(
        player=owner,
        characters=[operator(owner, index) for index in range(4)],
        source_scope="owner",
        roster_complete=True,
    )
    pages = roster.render(model, context_for(model), character_ids=["canonical-3", "opaque-1"])
    values = [entry[0] for entry in text_log]
    assert [value for value in values if value.startswith("Operator ")] == ["Operator 1", "Operator 3"]
    assert any("2 selected" in value for value in values) and not any("Complete" in value for value in values)
    pages[0].close()


def test_header_caps_count_only_supplied_limits_and_never_an_overall_build_score(owner):
    first, second = operator(owner, 0), operator(owner, 1)
    first.skills[0].level = first.skills[0].max_level
    first.skills[1].max_level = 0
    second.skills = []
    second.level = second.max_level
    assert parts.roster_counts([first, second]) == [
        ("CHARACTERS", "2"),
        ("LEVEL CAPPED", "1"),
        ("SKILLS AT CAP", "1/3"),
    ]
    assert parts.roster_counts([])[-1] == ("SKILLS AT CAP", "—")


def test_duplicate_identity_is_rejected_before_any_page_is_allocated(owner, monkeypatch):
    item = operator(owner, 0)

    def unexpected(*args, **options):
        raise AssertionError("Invalid roster must not allocate pixels")

    monkeypatch.setattr(PageCanvas, "__init__", unexpected)
    with pytest.raises(DataValidationError) as error:
        roster.render([item, item], context_for(owner), character_ids=[])
    assert error.value.code == "duplicate_character"


def test_roster_photos_icons_and_caller_pixels_are_preserved(owner):
    item = operator(owner, 0)
    model = PlayerCard(player=owner, avatar=link("owner"), characters=[item])
    source = Image.new("RGBA", (80, 80), (70, 120, 150, 205))
    original = source.tobytes()

    class Assets(dict):
        def __init__(self):
            super().__init__()
            self.requested = []

        def get(self, key, default=None):
            self.requested.append(key)
            return source if isinstance(key, str) and key.startswith("https://") else default

    assets = Assets()
    pages = roster.render(model, context_for(model), assets=assets)
    assert item.images.avatar.url in assets.requested and item.images.portrait.url not in assets.requested
    assert all(skill.icon.url in assets.requested for skill in item.skills)
    assert all(piece.icon.url in assets.requested for piece in item.equipment)
    assert model.avatar.url in assets.requested and item.weapon.images.url in assets.requested
    assert source.tobytes() == original
    pages[0].close()
    source.close()
