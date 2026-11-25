"""Factory boards preserve observed industry and Dijiang data without exploration."""

import pytest
from PIL import Image
from skport.games.endfield.models import (
    AreaProgress,
    Cabin,
    CrewMember,
    FactoryState,
    ImageLinks,
    ItemSummary,
    PlayerCard,
    PlayerIdentity,
    RegionProgress,
    ResourceMeter,
    Settlement,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import DataValidationError, OwnerMismatchError
from endfield_cards.rendering.templates import factory
from endfield_cards.rendering.templates.factory import _shared as parts
from endfield_cards.utils.drawing import PageCanvas


def link(name):
    return ImageLinks(skport=f"https://factory.example.test/{name}.png")


def state(*, regions=2, posts=3, cabins=6, crew=3):
    owner = PlayerIdentity(name="Factory Owner", game_uid="game", skport_id="social")
    return FactoryState(
        player=owner,
        regions=[
            RegionProgress(
                id=f"region-{index}",
                name=f"Industry region {index}",
                level=12,
                funds=ResourceMeter(current=7_656_928, maximum=30_000_000),
                factory={"power": {"current": 0, "maximum": 100}},
                settlements=[
                    Settlement(
                        id=f"post-{index}-{number}",
                        name=f"Settlement {index}-{number}",
                        level=4,
                        maximum_level=number != 2,
                        stock=ResourceMeter(current=300, maximum=100),
                        experience=ResourceMeter(current=7, maximum=10),
                        officer=ItemSummary(name="Officer", icon=link("officer")),
                    )
                    for number in range(posts)
                ],
                areas=[
                    AreaProgress(
                        name="Exploration-only area",
                        counters=[ResourceMeter(name="Puzzles", current=7, maximum=19)],
                    )
                ],
            )
            for index in range(regions)
        ],
        cabins=[
            Cabin(
                name=f"Dijiang cabin {index}",
                level=3,
                kind=(0, 1, 2, 5)[index % 4],
                crew=[
                    CrewMember(
                        name=f"Crew {index}-{number}",
                        icon=link(f"crew-{number}"),
                        physical_strength=0 if number == 0 else 4567,
                        favorability=1500,
                    )
                    for number in range(crew)
                ],
                reports={"credit": 0},
            )
            for index in range(cabins)
        ],
    )


@pytest.fixture
def drawn(monkeypatch):
    calls = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        calls.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return calls


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_factory_keeps_industry_and_dijiang_on_one_board_without_any_exploration(variant, drawn):
    model = state()
    original = model.model_dump()
    assets = {url: Image.new("RGBA", (96, 96), "#A15463") for url in parts.urls(model)}
    pixels = {url: image.tobytes() for url, image in assets.items()}
    images = factory.render(model, context_for(model), variant=variant, assets=assets)
    assert len(images) == 1 and images[0].width == 1600 and images[0].height < 1700
    values = "\n".join(value for value, *_ in drawn)
    assert "Exploration" not in values and "EXPLORATION" not in values and "Puzzles" not in values
    assert "300 / 100" in values and "7 / 10" in values and "0 / 100" in values
    assert "DIJIANG CABINS" in values and all(
        member.name in values for room in model.cabins for member in room.crew
    )
    assert all(post.name in values for region in model.regions for post in region.settlements)
    assert "akef-cards" in values and "endfield-cards" in values
    assert all(0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in drawn)
    assert model.model_dump() == original
    assert pixels == {url: image.tobytes() for url, image in assets.items()}
    images[0].close()
    for image in assets.values():
        image.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_missing_funds_and_progression_do_not_become_observed_zero(variant, drawn):
    owner = PlayerIdentity(name="Owner", game_uid="game", skport_id="social")
    model = FactoryState(
        player=owner,
        regions=[RegionProgress(name="Unknown region", settlements=[Settlement(name="Unknown settlement")])],
        cabins=[Cabin(name="Unknown cabin", crew=[CrewMember(name="Unknown operator")])],
    )
    images = factory.render(model, context_for(model), variant=variant)
    values = "\n".join(value for value, *_ in drawn)
    assert (
        "— / —" in values and "Lv —" in values and "Status unavailable" in values
        if variant == "dark"
        else "— / —" in values and "Lv —" in values
    )
    assert "0 / 0" not in values and "MAX" not in values and "FULL" not in values
    images[0].close()


def test_large_industry_and_cabin_collections_stream_bounded_continuations(drawn):
    model = state(regions=3, posts=5, cabins=7, crew=4)
    pages = factory.render(model, context_for(model), variant="dark")
    assert len(pages) == 3 and max(page.height for page in pages) < 1900
    values = "\n".join(value for value, *_ in drawn)
    assert all(post.name in values for region in model.regions for post in region.settlements)
    assert all(member.name in values for room in model.cabins for member in room.crew)
    assert "01 / 03" in values and "03 / 03" in values
    for page in pages:
        page.close()


def test_owner_and_duplicate_region_validation_precede_canvas_allocation(monkeypatch):
    model = state()

    def fail(*args, **kwargs):
        raise AssertionError("Validation must precede drawing")

    monkeypatch.setattr(parts, "draw", fail)
    wrong = PlayerCard(player=PlayerIdentity(name="Other", game_uid="other", skport_id="other"))
    with pytest.raises(OwnerMismatchError):
        factory.render(model, context_for(model), profile=wrong)
    model.regions[1].id = model.regions[0].id
    with pytest.raises(DataValidationError, match="duplicate"):
        factory.render(model, context_for(model))


def test_empty_factory_and_dijiang_remain_a_single_concise_owned_card(drawn):
    owner = PlayerIdentity(name="Owner", game_uid="game", skport_id="social")
    model = FactoryState(player=owner)
    images = factory.render(model, context_for(model))
    assert len(images) == 1 and images[0].size == (1600, 790)
    assert "UID game" in "\n".join(value for value, *_ in drawn)
    images[0].close()
