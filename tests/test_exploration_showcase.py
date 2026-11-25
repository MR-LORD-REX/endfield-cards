"""Exploration boards preserve all regions/categories without factory or Dijiang data."""

import pytest
from skport.games.endfield.models import FactoryState, PlayerCard, PlayerIdentity, ResourceMeter
from skport.games.endfield.models.world import AreaProgress, Cabin, CrewMember, RegionProgress, Settlement

from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import DataValidationError, OwnerMismatchError
from endfield_cards.rendering.templates import exploration
from endfield_cards.rendering.templates.exploration import _shared as parts
from endfield_cards.utils.drawing import PageCanvas

KEYS = tuple(parts.ICONS)
NAMES = ("Puzzles", "Chests", "Equipment chests", "Fragments", "Blackboxes", "Aurylenes")


def state(counts=(6, 13), categories=6):
    owner = PlayerIdentity(name="Exploration owner", game_uid="game", skport_id="social")
    regions = []
    for region_index, area_count in enumerate(counts):
        areas = []
        for area_index in range(area_count):
            areas.append(
                AreaProgress(
                    id=f"r{region_index}-a{area_index}",
                    name=f"Area {region_index}-{area_index}",
                    counters=[
                        ResourceMeter(
                            key=KEYS[index] if index < len(KEYS) else f"extra-{index}",
                            name=NAMES[index] if index < len(NAMES) else f"Extra category {index}",
                            current=area_index * 20 + index,
                            maximum=area_index * 20 + index + 10,
                        )
                        for index in range(categories)
                    ],
                )
            )
        regions.append(
            RegionProgress(
                id=f"region-{region_index}",
                name=f"Region {region_index}",
                areas=areas,
                funds=ResourceMeter(name="Factory funds secret", current=99999, maximum=100000),
                settlements=[Settlement(name="Factory-only settlement")],
                factory={"production": "Factory-only production"},
            )
        )
    return FactoryState(
        player=owner,
        regions=regions,
        cabins=[Cabin(name="Dijiang-only cabin", crew=[CrewMember(name="Factory-only crew")])],
    )


@pytest.fixture
def drawn(monkeypatch):
    values = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        values.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return values


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_ordinary_two_region_board_fits_one_card_and_keeps_all_area_counts(variant, drawn):
    model = state()
    original = model.model_dump()
    pages = exploration.render(model, context_for(model), variant=variant)
    text = "\n".join(value for value, *_ in drawn)
    assert len(pages) == 1 and pages[0].width == 2000 and pages[0].height <= parts.MAX_HEIGHT
    for region in model.regions:
        assert region.name in text
        for area in region.areas:
            assert area.name in text
            assert all(parts.counter_text(counter) in text for counter in area.counters)
    assert all(name in text for name in NAMES)
    assert "Factory-only" not in text and "Dijiang" not in text and "99999" not in text
    assert "akef-cards" in text and "endfield-cards" in text and "UID game" in text
    assert all(0 <= y and y + height <= page_height for _, _, y, height, _, page_height in drawn)
    assert model.model_dump() == original
    pages[0].close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_large_area_collections_paginate_without_losing_source_order(variant, drawn):
    model = state((80,), categories=2)
    pages = exploration.render(model, context_for(model), variant=variant)
    text = "\n".join(value for value, *_ in drawn)
    assert len(pages) > 1 and all(page.height <= parts.MAX_HEIGHT for page in pages)
    assert all(area.name in text for area in model.regions[0].areas)
    area_labels = [value for value, *_ in drawn if value[:2].isdigit() and "Area 0-" in value]
    assert area_labels == [f"{index + 1:02d}  Area 0-{index}" for index in range(80)]
    assert f"01 / {len(pages):02d}" in text and f"{len(pages):02d} / {len(pages):02d}" in text
    for page in pages:
        page.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_additional_counter_categories_are_preserved_in_bounded_continuations(variant, drawn):
    model = state((1,), categories=13)
    pages = exploration.render(model, context_for(model), variant=variant)
    text = "\n".join(value for value, *_ in drawn)
    assert all(
        counter.name in text and parts.counter_text(counter) in text
        for counter in model.regions[0].areas[0].counters
    )
    assert all(page.height <= parts.MAX_HEIGHT for page in pages)
    assert len(model.regions[0].areas[0].counters) == 13
    for page in pages:
        page.close()


def test_missing_zero_capacity_and_overflow_counters_remain_distinct():
    assert parts.counter_text(ResourceMeter(maximum=10)) == "— / 10"
    assert parts.counter_text(ResourceMeter(current=0, maximum=10)) == "0 / 10"
    assert parts.counter_text(ResourceMeter(current=0, maximum=0)) == "0 / 0"
    assert parts.counter_text(ResourceMeter(current=15, maximum=10)) == "15 / 10"
    assert parts.percent(parts.summary([ResourceMeter(current=0, maximum=0)])) == "—"
    assert parts.percent(parts.summary([ResourceMeter(current=0, maximum=10)])) == "0%"
    assert parts.percent(parts.summary([ResourceMeter(current=15, maximum=10)])) == "150%"
    partial = parts.summary([ResourceMeter(current=3, maximum=10), ResourceMeter(maximum=5)])
    assert partial.label == "3 / 10 known" and parts.percent(partial) == "30% known"


def test_unnamed_equal_counters_remain_distinct_by_source_position(drawn):
    model = state((1,))
    first = ResourceMeter(current=3, maximum=10)
    model.regions[0].areas[0].counters = [first, first.model_copy(deep=True)]
    pages = exploration.render(model, context_for(model), variant="dark")
    headings = [value for value, _, y, *_ in drawn if y == parts.TOP + 78 + 36]
    assert headings == ["3 / 10", "3 / 10"]
    pages[0].close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_empty_regions_and_areas_have_small_valid_boards(variant, drawn):
    model = state(())
    pages = exploration.render(model, context_for(model), variant=variant)
    assert len(pages) == 1 and pages[0].size == (2000, 730)
    assert "No exploration regions supplied" in "\n".join(value for value, *_ in drawn)
    pages[0].close()
    model = state((0,))
    pages = exploration.render(model, context_for(model), variant=variant)
    assert "No area data supplied" in "\n".join(value for value, *_ in drawn)
    pages[0].close()


def test_owner_and_duplicate_identity_validation_precedes_page_allocation(monkeypatch):
    model = state((1,))
    wrong = PlayerCard(player=PlayerIdentity(name="Other", game_uid="other", skport_id="other"))
    with pytest.raises(OwnerMismatchError):
        exploration.render(model, context_for(model), profile=wrong)
    model.regions[0].areas.append(model.regions[0].areas[0].model_copy(deep=True))
    monkeypatch.setattr(
        parts, "light_page", lambda *args, **kwargs: pytest.fail("Validation must precede drawing")
    )
    with pytest.raises(DataValidationError, match="duplicate"):
        exploration.render(model, context_for(model))
