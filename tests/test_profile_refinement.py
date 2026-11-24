"""Profile reference fidelity, source identity and single-image layout contracts."""

from __future__ import annotations

import importlib
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest
from PIL import Image
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    CharacterImages,
    ImageLinks,
    MedalSummary,
    OwnershipCounts,
    PlayerCard,
    PlayerIdentity,
    RegionProgress,
    SemanticLabel,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.rendering.templates import profile
from endfield_cards.utils.drawing import PageCanvas

SIZES = {"overview": (1600, 1400), "operations": (1600, 1400), "identity": (1920, 1200)}


def shared():
    return importlib.import_module("endfield_cards.rendering.templates.profile._shared")


def link(name: str) -> ImageLinks:
    return ImageLinks(skport=f"https://profile.example.test/{name}.png")


def player() -> PlayerIdentity:
    return PlayerIdentity(name="Actual Owner", skport_id="social-id", game_uid="6397007521")


def model(count: int = 8) -> PlayerCard:
    owner = player()
    return PlayerCard(
        player=owner,
        avatar=link("avatar"),
        banner=link("banner"),
        biography="Source biography",
        mission="Source mission",
        authority_level=60,
        world_level=7,
        server_name="Asia",
        counts=OwnershipCounts(characters=24, weapons=51, documents=137, achievements=73),
        created_at=datetime(2026, 2, 3, 6, 22, tzinfo=UTC),
        snapshot_at=datetime(2026, 11, 6, 16, 10, tzinfo=UTC),
        server_time=datetime(2026, 11, 24, 10, 54, tzinfo=UTC),
        regions=[RegionProgress(id="r", name="Valley IV", level=12)],
        medals=[
            MedalSummary(id=f"medal-{slot}", name=f"Medal {slot}", slot=slot, icon=link(f"medal-{slot}"))
            for slot in range(1, 11)
        ],
        characters=[
            CharacterBuild(
                identity=CharacterIdentity(skport_id=f"operator-{index}", str_id=f"canonical-{index}"),
                name=f"Operator {index}",
                owner=owner,
                level=67,
                max_level=80,
                evolution=4,
                potential=2,
                rarity=6,
                images=CharacterImages(portrait=link(f"portrait-{index}")),
                profession=SemanticLabel(key="profession_assault", name="Striker", icons=link("profession")),
                element=SemanticLabel(key="char_property_pulse", name="Electric", icons=link("element")),
            )
            for index in range(count)
        ],
    )


class SourceImages(dict[str, Image.Image]):
    def __init__(self, card: PlayerCard) -> None:
        links = [card.avatar.url, card.banner.url, *[m.icon.url for m in card.medals]]
        links.extend(c.images.portrait.url for c in card.characters)
        links.extend(
            ["https://profile.example.test/profession.png", "https://profile.example.test/element.png"]
        )
        super().__init__({url: Image.new("RGBA", (96, 160), (87, 133, 171, 255)) for url in links if url})
        self.requested: set[str] = set()

    def get(self, key, default=None):
        if isinstance(key, str):
            self.requested.add(key)
        return super().get(key, default)

    def close(self) -> None:
        for image in self.values():
            image.close()


@pytest.fixture
def text_log(monkeypatch):
    values = []
    original = PageCanvas.text

    def capture(self, x, y, value, **kwargs):
        height = original(self, x, y, value, **kwargs)
        values.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return values


@pytest.mark.parametrize("variant", SIZES)
def test_profile_reference_information_and_all_ten_medal_images(variant, text_log):
    card = model()
    images = SourceImages(card)
    original_pixels = {key: pixels.tobytes() for key, pixels in images.items()}
    original_model = card.model_dump(mode="json")
    pages = profile.render(card, context_for(card), variant=variant, assets=images)
    try:
        assert len(pages) == 1 and pages[0].size == SIZES[variant]
        assert {
            card.avatar.url,
            *[c.images.portrait.url for c in card.characters],
            *[m.icon.url for m in card.medals],
        }.issubset(images.requested)
        assert {card.characters[0].profession.icons.url, card.characters[0].element.icons.url}.issubset(
            images.requested
        )
        declared = profile.urls(card)
        assert card.banner.url in declared
        assert {m.icon.url for m in card.medals}.issubset(declared)
        text = "\n".join(value[0] for value in text_log)
        for supplied in ("Actual Owner", "6397007521", "Asia", "Source biography", "Valley IV"):
            assert supplied.casefold() in text.casefold()
        for index in range(8):
            assert f"Operator {index}" in text
        assert "67/80" in text.replace("\n", "") and "E4" in text
        if variant != "operations":
            assert "P2" in text
        assert "24" in text and "51" in text and "137" in text
        assert card.model_dump(mode="json") == original_model
        assert {key: pixels.tobytes() for key, pixels in images.items()} == original_pixels
        assert all(y + height <= page_height for _, _, y, height, _, page_height in text_log)
    finally:
        for image in pages:
            image.close()
        images.close()


def test_days_are_completed_source_days_and_prefer_server_time():
    card = model()
    assert shared().days_played(card) == (card.server_time - card.created_at).days
    stale_only = card.model_copy(update={"server_time": None})
    assert shared().days_played(stale_only) == (card.snapshot_at - card.created_at).days
    assert shared().days_played(card.model_copy(update={"created_at": None})) is None
    assert shared().days_played(card.model_copy(update={"server_time": None, "snapshot_at": None})) is None
    future = card.model_copy(update={"created_at": card.server_time + timedelta(days=1)})
    assert shared().days_played(future) is None


def test_profile_facts_distinguish_absence_from_supplied_zero_counts():
    card = PlayerCard(player=player())
    assert shared().facts(card) == []
    zero = PlayerCard(player=player(), counts=OwnershipCounts(characters=0), authority_level=0)
    assert ("Operators", "0") in shared().facts(zero)
    assert ("Authority", "0") in shared().facts(zero)


def test_medal_slots_preserve_explicit_placement_and_fill_only_unused_slots():
    explicit = MedalSummary(id="placed", slot=8, icon=link("placed"))
    no_slot = MedalSummary(id="unplaced", icon=link("unplaced"))
    card = PlayerCard(player=player(), medals=[no_slot, explicit])
    slots = shared().medal_slots(card)
    assert slots[8].id == "placed"
    assert len(slots) == 2 and next(key for key, value in slots.items() if value.id == "unplaced") != 8


def test_medal_icon_uses_observed_state_and_source_preference():
    medal = MedalSummary(
        id="m", plated=True, icon=link("observed"), initial_icon=link("initial"), plated_icon=link("plated")
    )
    assert shared().medal_url(medal) == medal.icon.url
    without_observed = medal.model_copy(update={"icon": ImageLinks()})
    assert shared().medal_url(without_observed) == medal.plated_icon.url
    unplated = without_observed.model_copy(update={"plated": False})
    assert shared().medal_url(unplated) == medal.initial_icon.url


def test_medal_geometry_contains_ten_staggered_bounded_hexagons():
    boxes = shared().medal_geometry(400, 80, 32)
    assert set(boxes) == set(range(1, 11))
    assert all(
        left >= 400 and top >= 80 and right > left and bottom > top
        for left, top, right, bottom in boxes.values()
    )
    assert max(right for _, _, right, _ in boxes.values()) <= 400 + 32 * 12
    assert max(bottom for _, _, _, bottom in boxes.values()) <= 80 + 32 * 4.2
    assert boxes[1][1] == boxes[3][1] and boxes[2][1] > boxes[1][1]
    assert boxes[2][0] > boxes[1][0]


@pytest.mark.parametrize("variant", SIZES)
def test_missing_optional_profile_values_do_not_create_age_or_owned_counts(variant, text_log):
    card = PlayerCard(player=player(), mission="Source mission")
    pages = profile.render(card, context_for(card), variant=variant)
    try:
        assert len(pages) == 1
        text = "\n".join(value[0] for value in text_log)
        assert "Source mission" in text
        assert "Day 0" not in text and "Days 0" not in text
        assert "No characters supplied" in text
    finally:
        for image in pages:
            image.close()


@pytest.mark.parametrize(
    "locale,name",
    [
        ("en", "A Long Supplied Owner Name"),
        ("ja", "長い名前の管理人"),
        ("ko", "긴이름의관리자"),
        ("zh-Hans", "具有很长名称的管理员"),
        ("zh-Hant", "具有很長名稱的管理員"),
    ],
)
def test_owner_names_across_supported_scripts_remain_inside_page(locale, name, text_log):
    card = model(1)
    card.player.name = name
    card.characters[0].owner.name = name
    context = replace(context_for(card), locale=locale)
    pages = profile.render(card, context, variant="overview")
    try:
        assert len(pages) == 1
        assert name in "\n".join(entry[0] for entry in text_log)
        assert all(y + height <= height_limit for _, _, y, height, _, height_limit in text_log)
    finally:
        for image in pages:
            image.close()
