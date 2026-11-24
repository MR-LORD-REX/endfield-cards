"""Verify bounded pagination and source information across card families."""

from importlib import import_module

import pytest
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    ContractState,
    EventStage,
    FactoryState,
    LiveStatus,
    MonumentEvent,
    MonumentState,
    PlayerCard,
    PlayerIdentity,
    PullHistory,
    ResourceMeter,
    StageRun,
    TeamMember,
    WikiPage,
    WikiSection,
    WikiSummary,
)
from skport.games.endfield.models.world import AreaProgress, Cabin, CrewMember, RegionProgress, Settlement

from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.components import PageCanvas
from endfield_cards.rendering.templates._records import Record, photo, record_page_count


@pytest.fixture
def owner():
    return PlayerIdentity(skport_id="social", game_uid="1234567890", name="Fixture Owner")


@pytest.fixture
def text_spy(monkeypatch):
    drawn = []
    original = PageCanvas.text

    def capture(self, x, y, value, **kwargs):
        drawn.append((str(value), x, y, self.width, self.height))
        return original(self, x, y, value, **kwargs)

    monkeypatch.setattr(PageCanvas, "text", capture)
    return drawn


def test_roster_small_full_collection_stays_on_one_image_with_owner_footer(owner, text_spy):
    roster = import_module("endfield_cards.rendering.templates.roster")
    builds = [
        CharacterBuild(identity=CharacterIdentity(skport_id=f"id-{i}"), name=f"Operator {i}", owner=owner)
        for i in range(13)
    ]
    model = PlayerCard(player=owner, characters=builds, source_scope="owner", roster_complete=True)
    pages = roster.render(model, context_for(model))
    assert len(pages) == 1
    assert {page.size for page in pages} == {(2400, 1345)}
    names = [value for value, *_ in text_spy if value.startswith("Operator ")]
    assert names == [f"Operator {i}" for i in range(13)]
    footers = [value for value, *_ in text_spy if "UID 1234567890" in value]
    assert len(footers) == 2  # Header and reserved footer both retain the owner UID.
    for page in pages:
        page.close()


def test_roster_duplicates_raise_before_drawing(owner):
    roster = import_module("endfield_cards.rendering.templates.roster")
    build = CharacterBuild(identity=CharacterIdentity(skport_id="same"), owner=owner)
    with pytest.raises(DataValidationError, match="duplicate"):
        roster.render([build, build], context_for(owner))


def test_monument_detail_keeps_both_difficulties_and_teams(owner, text_spy):
    detail = import_module("endfield_cards.rendering.templates.monument_detail")
    event = MonumentEvent(
        id="e",
        name="Fixture Event",
        stages=[
            EventStage(
                id="s",
                name="Stage A",
                normal_cleared=True,
                hard_cleared=True,
                normal=StageRun(
                    duration_seconds=62.25,
                    completed=True,
                    team=[TeamMember(character_id="c", name="Team Normal", level=80)],
                ),
                hard=StageRun(
                    duration_seconds=71.5,
                    completed=True,
                    team=[TeamMember(character_id="c", name="Team Hard", level=90)],
                ),
            )
        ],
    )
    state = MonumentState(player=owner, events=[event])
    pages = detail.render(state, context_for(state), event_id="e")
    text = "\n".join(value for value, *_ in text_spy)
    assert "Team Normal" in text and "Team Hard" in text
    assert "01:02.25" in text and "01:11.50" in text
    assert all(page.size == (1600, 1100) for page in pages)
    with pytest.raises(DataValidationError, match="absent"):
        detail.render(state, context_for(state), event_id="missing")
    for page in pages:
        page.close()


def test_long_wiki_text_paginates_with_final_content(owner, text_spy):
    wiki = import_module("endfield_cards.rendering.templates.wiki")
    paragraphs = "\n".join(f"Paragraph {i}: source lore remains visible." for i in range(100))
    model = WikiPage(
        summary=WikiSummary(id="w", name="Fixture Wiki"),
        sections=[WikiSection(title="Lore", text=paragraphs)],
    )
    pages = wiki.render(model, context_for(model, owner))
    assert len(pages) > 2
    assert any("Paragraph 99" in value for value, *_ in text_spy)
    # Body lines never extend into the reserved footer.
    body_y = [y for value, _, y, _, height in text_spy if value.startswith("Paragraph")]
    assert max(body_y) < 996
    for page in pages:
        page.close()


def test_factory_retains_all_areas_settlements_crews(owner, text_spy):
    factory = import_module("endfield_cards.rendering.templates.factory")
    state = FactoryState(
        player=owner,
        regions=[
            RegionProgress(
                id="r",
                name="Region A",
                settlements=[
                    Settlement(
                        id="s", name="Settlement A", level=5, stock=ResourceMeter(current=300, maximum=100)
                    )
                ],
                areas=[
                    AreaProgress(
                        id="a",
                        name="Area A",
                        counters=[ResourceMeter(key="chests", name="Chests", current=7, maximum=10)],
                    )
                ],
            )
        ],
        cabins=[
            Cabin(
                id="c",
                name="Cabin A",
                crew=[CrewMember(id="operator", name="Crew A", physical_strength=63, favorability=44)],
            )
        ],
    )
    pages = factory.render(state, context_for(state))
    text = "\n".join(value for value, *_ in text_spy)
    assert all(
        term in text for term in ("300 / 100", "Chests: 7 / 10", "Crew A", "Stamina 63", "Favorability 44")
    )
    for page in pages:
        page.close()


def test_empty_lazy_asset_mapping_is_not_discarded(owner):
    calls = []

    class LazyAssets(dict):
        def get(self, key, default=None):
            calls.append(key)
            return default

    assets = LazyAssets()
    canvas = PageCanvas("Test", context_for(owner), assets=assets)
    photo(canvas, "https://example.test/image.png", (0, 0, 20, 20), assets)
    assert calls == ["https://example.test/image.png"]
    canvas.image.close()


def test_record_count_planning_allocates_no_page_images(owner, monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("Planning must not draw decoded pages")

    monkeypatch.setattr(PageCanvas, "__init__", fail)
    records = [Record("Complete source lore", ["\n".join(f"Line {i}" for i in range(200))])]
    assert record_page_count(context_for(owner), records) >= 4


def test_very_long_roster_name_has_complete_appendix(owner, text_spy):
    roster = import_module("endfield_cards.rendering.templates.roster")
    name = "非常に長い名前" * 14 + "TAIL"
    build = CharacterBuild(identity=CharacterIdentity(skport_id="long-name"), name=name, owner=owner)
    pages = roster.render([build], context_for(owner), details=True)
    assert len(pages) == 2
    assert any("TAIL" in value for value, *_ in text_spy)
    for page in pages:
        page.close()


@pytest.mark.parametrize(
    "family",
    [
        "activity",
        "factory",
        "monument",
        "monument_detail",
        "contingency_contract",
        "contingency_contract_detail",
        "pulls",
        "wiki",
    ],
)
def test_empty_families_are_bounded_and_dark_works(family, owner):
    state = {
        "activity": LiveStatus(player=owner),
        "factory": FactoryState(player=owner),
        "monument": MonumentState(player=owner),
        "monument_detail": MonumentState(player=owner),
        "contingency_contract": ContractState(player=owner),
        "contingency_contract_detail": ContractState(player=owner),
        "pulls": PullHistory(player=owner),
        "wiki": WikiPage(summary=WikiSummary(id="empty")),
    }[family]
    module = import_module(f"endfield_cards.rendering.templates.{family}")
    pages = module.render(state, context_for(state, owner), variant="dark")
    assert 1 <= len(pages) <= 2
    expected_width = 2000 if family == "contingency_contract_detail" else 1600
    assert all(page.width == expected_width and page.height <= 1100 for page in pages)
    for page in pages:
        page.close()
