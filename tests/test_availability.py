"""Unfinished layouts fail before fetching, importing templates or admitting worker jobs."""

from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from skport import ClientConfig
from skport.games.endfield.models import (
    ContractState,
    CrisisContract,
    EventStage,
    MonumentEvent,
    MonumentState,
    PlayerIdentity,
    StageRun,
)

from endfield_cards import CardError, CardNotImplementedError, Cards, EF_Cards
from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import UnsupportedVariantError
from endfield_cards.rendering import RenderEngine, registry
from endfield_cards.utils.selection import default_monument_event_index, render_info


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method, args, options, family",
    [
        ("factory_card", (2348675939926,), {"template": 2}, "factory"),
        ("wiki_card", (None,), {"owner": None, "template": 1}, "wiki"),
        ("monument_detailed_card", (2348675939926,), {"template": 2}, "monument_detail"),
        (
            "contingency_contract_detailed_card",
            (2348675939926,),
            {"template": 1},
            "contingency_contract_detail",
        ),
    ],
)
async def test_planned_card_raises_before_any_sdk_or_renderer_work(
    monkeypatch, method, args, options, family
):
    monkeypatch.setattr(registry, "UNIMPLEMENTED", frozenset({family}))
    game = SimpleNamespace(card=AsyncMock(), monument=AsyncMock(), contract=AsyncMock(), factory=AsyncMock())
    sdk = SimpleNamespace(config=ClientConfig(), endfield=game)
    draw = AsyncMock()
    monkeypatch.setattr(RenderEngine, "render", draw)
    async with Cards(sdk) as renderer:
        with pytest.raises(CardNotImplementedError) as caught:
            await getattr(renderer, method)(*args, **options)
    assert isinstance(caught.value, (CardError, NotImplementedError))
    assert caught.value.code == "not_implemented"
    assert method in str(caught.value)
    assert all(call.await_count == 0 for call in vars(game).values())
    draw.assert_not_awaited()


@pytest.mark.asyncio
async def test_advanced_engine_rejects_unfinished_card_before_import_or_owner_validation(monkeypatch):
    monkeypatch.setattr(registry, "UNIMPLEMENTED", frozenset({"factory", "wiki"}))
    importer = AsyncMock()
    monkeypatch.setattr(registry, "import_module", importer)
    async with RenderEngine() as engine:
        with pytest.raises(CardNotImplementedError):
            await engine.render("factory", None, variant="dark")
        with pytest.raises(CardNotImplementedError):
            await anext(engine.iter_pages("wiki", None))
        with pytest.raises(UnsupportedVariantError):
            await engine.render("factory", None, variant="missing")
    importer.assert_not_called()


@pytest.mark.parametrize("family", ["pulls", "wiki"])
@pytest.mark.parametrize("template", [1, 2])
@pytest.mark.asyncio
async def test_pulls_and_wiki_are_disabled_before_any_client_or_engine_work(monkeypatch, family, template):
    game = SimpleNamespace(card=AsyncMock())
    sdk = SimpleNamespace(config=ClientConfig(), endfield=game)
    draw = AsyncMock()
    importer = AsyncMock()
    monkeypatch.setattr(RenderEngine, "render", draw)
    monkeypatch.setattr(registry, "import_module", importer)
    async with EF_Cards(sdk) as cards:
        with pytest.raises(CardNotImplementedError) as caught:
            await getattr(cards, f"{family}_card")(template=template)
    assert caught.value.code == "not_implemented"
    assert f"{family}_card(template={template})" in str(caught.value)
    assert isinstance(caught.value, NotImplementedError)
    game.card.assert_not_awaited()
    draw.assert_not_awaited()
    importer.assert_not_called()



@pytest.mark.parametrize("family", ["pulls", "wiki"])
@pytest.mark.parametrize("template", [1, 2])
@pytest.mark.asyncio
async def test_pulls_and_wiki_engine_entry_points_are_disabled_before_template_import(
    monkeypatch, family, template
):
    importer = AsyncMock()
    monkeypatch.setattr(registry, "import_module", importer)
    async with RenderEngine() as engine:
        with pytest.raises(CardNotImplementedError):
            await engine.render(family, None, variant="light" if template == 1 else "dark")
        with pytest.raises(CardNotImplementedError):
            await anext(engine.iter_pages(family, None, variant="light" if template == 1 else "dark"))
    importer.assert_not_called()


def test_detailed_metadata_defaults_match_one_selected_event_and_current_contract():
    owner = PlayerIdentity(name="Owner", game_uid="game", skport_id="social")
    monument = MonumentState(
        player=owner,
        events=[
            MonumentEvent(id="archived", name="Archived", is_active=False),
            MonumentEvent(id="active", name="Active", is_active=True),
        ],
    )
    info = render_info("monument_detail", monument, context_for(monument))
    assert [(event.index, event.id) for event in info.events] == [(1, "active")]
    info = render_info("monument_detail", monument, context_for(monument), event_id="archived")
    assert [(event.index, event.id) for event in info.events] == [(0, "archived")]
    assert len(render_info("monument", monument, context_for(monument)).events) == 2
    contract = ContractState(
        player=owner, current=CrisisContract(id="current"), contracts=[CrisisContract(id="old")]
    )
    info = render_info("contingency_contract_detail", contract, context_for(contract))
    assert [entry.id for entry in info.contracts] == ["current"]
    assert len(render_info("contingency_contract", contract, context_for(contract)).contracts) == 2


def test_default_monument_selection_uses_latest_source_date_without_host_clock():
    events = [
        MonumentEvent(id="old", starts_at=datetime(2026, 1, 1, tzinfo=UTC)),
        MonumentEvent(id="new", starts_at=datetime(2026, 10, 1, tzinfo=UTC)),
        MonumentEvent(id="undated"),
    ]
    assert default_monument_event_index(events) == 1
    owner = PlayerIdentity(name="Owner", game_uid="game", skport_id="social")
    model = MonumentState(player=owner, events=events)
    assert [
        (item.id, item.index) for item in render_info("monument_detail", model, context_for(model)).events
    ] == [("new", 1)]
    events[0].is_active = True
    assert default_monument_event_index(events) == 0
    assert default_monument_event_index([MonumentEvent(id="first"), MonumentEvent(id="second")]) == 0
    assert default_monument_event_index([]) is None


def test_monument_metadata_matches_observed_clear_when_stage_flag_is_missing():
    owner = PlayerIdentity(name="Owner", game_uid="game", skport_id="social")
    stages = [
        EventStage(id="observed", normal=StageRun(completed=True)),
        EventStage(id="unknown"),
        EventStage(id="uncleared", normal_cleared=False),
    ]
    model = MonumentState(player=owner, events=[MonumentEvent(id="event", stages=stages)])
    info = render_info("monument_detail", model, context_for(model))
    assert [stage.normal_cleared for stage in info.events[0].stages] == [True, None, False]
    assert all(stage.hard_cleared is None for stage in info.events[0].stages)
