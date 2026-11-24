"""Showcase information, account identity and artwork integrity contracts."""

from dataclasses import replace

import pytest
from PIL import Image
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    Equipment,
    EquipmentSet,
    Gem,
    GemTerm,
    ItemSummary,
    PlayerCard,
    PlayerIdentity,
    Potential,
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
from skport.games.endfield.models.progress import ResourceMeter
from skport.games.endfield.models.world import AreaProgress, RegionProgress

from endfield_cards.adapters.skport import context_for
from endfield_cards.client import Cards
from endfield_cards.config import OutputConfig
from endfield_cards.errors import DataValidationError
from endfield_cards.models import Artwork
from endfield_cards.rendering.components import PageCanvas
from endfield_cards.rendering.templates import character, compare, profile
from endfield_cards.rendering.templates.profile._shared import SIZE_BY_VARIANT


@pytest.fixture
def player():
    return PlayerIdentity(skport_id="social-one", game_uid="game-one", name="First Owner")


@pytest.fixture
def drawn_text(monkeypatch):
    entries = []
    original = PageCanvas.text

    def capture(self, x, y, value, **kwargs):
        height = original(self, x, y, value, **kwargs)
        entries.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return entries


def make_character(player, index=0, **kwargs):
    return CharacterBuild(
        identity=CharacterIdentity(
            skport_id=f"character-{index}", str_id="canonical-operator", template_id=54
        ),
        owner=player,
        name=f"Operator {index}",
        level=67,
        max_level=80,
        **kwargs,
    )


def close_pages(pages):
    for page in pages:
        page.close()


@pytest.mark.parametrize("count", [0, 1, 7, 8])
@pytest.mark.parametrize("variant", ["overview", "operations", "identity"])
def test_public_profile_zero_to_eight_supplied_entries(count, variant, player, drawn_text):
    model = PlayerCard(player=player, characters=[make_character(player, i) for i in range(count)])
    pages = profile.render(model, context_for(model), variant=variant)
    text = [entry[0] for entry in drawn_text]
    names = [value for value in text if value.startswith("Operator ")]
    expected = [f"Operator {i}" for i in range(count)]
    assert names[:count] == expected
    assert set(names) == set(expected)
    assert any(f"{count}/8" in value for value in text)
    assert all(page.size == SIZE_BY_VARIANT[variant] for page in pages)
    assert len(pages) == 1
    assert any("No characters supplied" in value for value in text) is (count == 0)
    assert sum("UID game-one" in value for value in text) >= len(pages)
    close_pages(pages)


def test_owner_profile_paginates_all_owned_entries(player, drawn_text):
    model = PlayerCard(
        player=player,
        characters=[make_character(player, i) for i in range(17)],
        source_scope="owner",
        roster_complete=True,
    )
    pages = profile.render(model, context_for(model))
    names = [entry[0] for entry in drawn_text if entry[0].startswith("Operator ")]
    expected = [f"Operator {i}" for i in range(17)]
    assert names[:17] == expected
    assert set(names) == set(expected)
    assert any("17 supplied" in entry[0] for entry in drawn_text)
    assert len(pages) == 3
    close_pages(pages)


@pytest.mark.parametrize(
    "variant,size",
    [
        ("field", (1920, 900)),
        ("dossier", (1600, 1100)),
        ("terminal", (1600, 1000)),
        ("portrait", (1000, 1400)),
    ],
)
def test_character_variants_keep_actual_max_level_and_optional_missing_state(
    variant, size, player, drawn_text
):
    model = make_character(player)
    iterator = character.iter_render(model, context_for(model), variant=variant)
    page = next(iterator)
    assert page.size == size
    text = "\n".join(entry[0] for entry in drawn_text)
    assert "67/80" in text
    assert "Unavailable" in text
    assert "UID game-one" in text
    page.close()
    iterator.close()


def test_profile_keeps_current_sdk_exploration_counters(player, drawn_text):
    model = PlayerCard(
        player=player,
        regions=[
            RegionProgress(
                name="Region supplied",
                areas=[
                    AreaProgress(
                        name="Area supplied",
                        counters=[ResourceMeter(name="Dataloggers", current=13, maximum=17)],
                    )
                ],
            )
        ],
    )
    pages = profile.render(model, context_for(model), details=True)
    text = "\n".join(entry[0] for entry in drawn_text)
    assert "Area supplied" in text and "Dataloggers" in text and "13" in text and "17" in text
    close_pages(pages)


@pytest.fixture
def rich_character(player):
    effect = StatModifier(id=52, formula="add", value=0.31, unit=StatUnit.FRACTION)
    return make_character(
        player,
        stats=StatBlock(
            values={999: StatValue(id=999, name="Future statistic", value=2.25, unit=StatUnit.FACTOR)}
        ),
        skills=[
            Skill(
                id="s", name="Skill supplied", level=9, max_level=12, description="Complete skill text marker"
            ),
            Skill(id="raw", name="Raw skill", raw_description="Raw description fallback marker"),
        ],
        talents=TalentTree(
            nodes=[
                TalentNode(id="t", name="Talent supplied", description="Talent detail marker", unlocked=True)
            ],
            potentials=[
                Potential(
                    level=4, name="Potential supplied", description="Potential detail marker", unlocked=True
                )
            ],
        ),
        weapon=Weapon(
            name="Weapon supplied",
            level=70,
            base_attack=480,
            skills=[Skill(id="ws", name="Weapon skill supplied", description="Weapon skill detail marker")],
            gem=Gem(name="Essence supplied", terms=[GemTerm(name="Socket supplied", points=8)]),
        ),
        equipment=[
            Equipment(
                slot="body",
                name="Equipment supplied",
                enhance_count=2,
                max_enhance=4,
                stat_lines=[
                    StatLine(
                        name="Combined affix supplied", value=0.31, unit=StatUnit.FRACTION, effects=[effect]
                    )
                ],
            )
        ],
        equipment_sets=[
            EquipmentSet(
                name="Set supplied",
                pieces=3,
                required_pieces=3,
                description="Equipment set detail marker",
                effects=[effect],
            )
        ],
        tactical_item=ItemSummary(name="Tactical supplied", description="Tactical description marker"),
    )


def test_character_detail_retains_every_supported_source_section(rich_character, drawn_text):
    pages = character.render(rich_character, context_for(rich_character), variant="field", details=True)
    assert len(pages) > 1
    text = "\n".join(entry[0] for entry in drawn_text)
    for marker in (
        "Future statistic",
        "Complete skill text marker",
        "Raw description fallback marker",
        "Talent detail marker",
        "Potential detail marker",
        "Weapon skill detail marker",
        "Essence supplied",
        "Socket supplied",
        "8 points",
        "Combined affix supplied",
        "31.0%",
        "Equipment set detail marker",
        "Tactical description marker",
    ):
        assert marker in text
    assert all(page.width <= 1920 and page.height <= 1100 for page in pages)
    close_pages(pages)


@pytest.mark.parametrize("variant", ["field", "dossier", "terminal", "portrait"])
def test_rich_character_is_one_concise_card_by_default(variant, rich_character, drawn_text, monkeypatch):
    def unexpected_appendix(*args, **kwargs):
        raise AssertionError("A concise card must not build or plan appendix records")

    monkeypatch.setattr(character, "records", unexpected_appendix)
    monkeypatch.setattr(character, "record_page_count", unexpected_appendix)
    monkeypatch.setattr(character, "iter_records", unexpected_appendix)
    pages = character.render(rich_character, context_for(rich_character), variant=variant)
    assert len(pages) == 1
    assert character.page_count(rich_character, context_for(rich_character), variant=variant) == 1
    text = "\n".join(entry[0] for entry in drawn_text)
    assert "67/80" in text and "UID game-one" in text
    assert "Weapon supplied" in text and "Essence supplied" in text
    assert "Complete skill text marker" not in text and "Talent detail marker" not in text
    assert "Raw description fallback marker" not in text
    close_pages(pages)


@pytest.mark.parametrize("variant", ["field", "dossier", "terminal", "portrait"])
def test_concise_character_keeps_present_unit_aware_bonus_stats(variant, player, drawn_text):
    model = make_character(
        player,
        stats=StatBlock(
            values={
                1: StatValue(id=1, name="HP", value=5990, unit=StatUnit.FLAT),
                44: StatValue(id=44, name="Ultimate Gain", value=1, unit=StatUnit.FRACTION),
                52: StatValue(id=52, name="Electric Damage", value=0.655, unit=StatUnit.FRACTION),
            }
        ),
    )
    pages = character.render(model, context_for(model), variant=variant)
    text = "\n".join(entry[0] for entry in drawn_text)
    assert len(pages) == 1
    assert "5990" in text and "100.0%" in text and "65.5%" in text
    assert "Ultimate Gain" in text and "Electric Damage" in text
    assert "ATK" not in text and "DEF" not in text
    close_pages(pages)


@pytest.mark.parametrize("variant", ["overview", "operations", "identity"])
def test_rich_public_profile_does_not_generate_default_appendices(variant, player):
    model = PlayerCard(
        player=player,
        biography="Long biography " * 300,
        characters=[make_character(player, index) for index in range(8)],
        regions=[
            RegionProgress(
                id=f"region-{index}",
                name=f"Region {index}",
                areas=[
                    AreaProgress(
                        name="Area supplied",
                        counters=[ResourceMeter(name="Dataloggers", current=13, maximum=17)],
                    )
                ],
            )
            for index in range(12)
        ],
    )
    pages = profile.render(model, context_for(model), variant=variant)
    assert len(pages) == 1
    close_pages(pages)


def test_default_comparison_never_generates_individual_character_appendices(player, monkeypatch):
    def unexpected_individual_cards(*args, **kwargs):
        raise AssertionError("A concise comparison must stay on one combined card")

    monkeypatch.setattr(character, "page_count", unexpected_individual_cards)
    monkeypatch.setattr(character, "iter_render", unexpected_individual_cards)
    other = PlayerIdentity(skport_id="social-two", game_uid="game-two", name="Second Owner")
    first, second = make_character(player), make_character(other)
    pages = compare.render(first, second, context_for(first), context_for(second))
    assert len(pages) == 1
    close_pages(pages)


@pytest.mark.asyncio
async def test_cards_facade_returns_one_page_without_appendices_by_default(rich_character, player):
    other = PlayerIdentity(skport_id="social-two", game_uid="game-two", name="Second Owner")
    output = OutputConfig(format="JPEG")
    async with Cards() as cards:
        pages = await cards.render_character(rich_character, output=output)
        assert len(pages) == 1 and pages[0].page == 1 and pages[0].pages == 1
        assert len(await cards.render_profile(PlayerCard(player=player), output=output)) == 1
        compared = await cards.render_compare(make_character(player), make_character(other), output=output)
        assert len(compared) == 1 and compared[0].pages == 1


def test_comparison_mismatch_is_explicit(player):
    first = make_character(player)
    second = first.model_copy(deep=True)
    second.identity.str_id = "other-operator"
    with pytest.raises(DataValidationError, match="same canonical"):
        compare.validate_pair(first, second)


@pytest.mark.parametrize("details", [False, True])
def test_comparison_every_page_carries_both_owners(details, player, drawn_text, monkeypatch):
    footer_owners = []
    original = PageCanvas.finish

    def capture(self, page=1, pages=1):
        footer_owners.append(
            (
                self.context.owner.game_uid,
                self.context.comparison_owner.game_uid if self.context.comparison_owner else None,
            )
        )
        return original(self, page, pages)

    monkeypatch.setattr(PageCanvas, "finish", capture)
    other = PlayerIdentity(skport_id="social-two", game_uid="game-two", name="Second Owner")
    first, second = make_character(player), make_character(other)
    pages = compare.render(
        first, second, context_for(first), context_for(second), variant="field", details=details
    )
    assert len(footer_owners) >= len(pages)
    assert all(set(owners) == {"game-one", "game-two"} for owners in footer_owners)
    assert sum(entry[0] == "UID game-one" for entry in drawn_text) >= len(pages)
    assert sum(entry[0] == "UID game-two" for entry in drawn_text) >= len(pages)
    assert len(pages) >= 3 if details else len(pages) == 1
    close_pages(pages)


@pytest.mark.parametrize("art_size,fit", [((64, 600), "cover"), ((600, 64), "contain")])
@pytest.mark.parametrize("variant", ["field", "dossier", "terminal", "portrait"])
def test_custom_tall_and_wide_art_does_not_mutate_caller_pixels(art_size, fit, variant, player):
    pixels = Image.new("RGBA", art_size, (81, 123, 164, 201))
    original = pixels.tobytes()
    artwork = Artwork(pixels, fit=fit, focal_point=(0.2, 0.8))
    model = make_character(player)
    iterator = character.iter_render(
        model, context_for(model), variant=variant, artwork=artwork, assets={"custom_art": pixels}
    )
    page = next(iterator)
    assert pixels.tobytes() == original and pixels.size == art_size
    page.close()
    iterator.close()
    pixels.close()


@pytest.mark.parametrize(
    "locale,name",
    [
        ("en", "A very long operator name with several words"),
        ("ja", "長い名前のオペレーターと情報"),
        ("ko", "긴이름의오퍼레이터정보"),
        ("zh-Hans", "具有很长名称的干员信息"),
        ("zh-Hant", "具有很長名稱的幹員資訊"),
    ],
)
def test_five_scripts_keep_character_name_and_owner_identity(locale, name, player, drawn_text):
    local_player = player.model_copy(update={"name": name})
    model = make_character(local_player)
    model.name = name
    context = replace(context_for(model), locale=locale)
    pages = character.render(model, context, variant="field")
    text = "\n".join(entry[0] for entry in drawn_text)
    assert name in text and "UID game-one" in text
    assert all(y + height <= page_height for _, _, y, height, _, page_height in drawn_text)
    close_pages(pages)
