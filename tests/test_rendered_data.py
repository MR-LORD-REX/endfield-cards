"""Rendered cards and source-backed selection/time data stay consistent and copy safe."""

import asyncio
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from skport import ImageSource
from skport.games.endfield.clean.endgame import build_contract_report
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    ContractState,
    CrisisContract,
    EventStage,
    LiveStatus,
    MonumentEvent,
    MonumentState,
    PlayerCard,
    PlayerIdentity,
    ResourceMeter,
)

from endfield_cards import CardResult
from endfield_cards.adapters.skport import context_for
from endfield_cards.models import CharacterListInfo, ContractInfo, LiveInfo, MonumentInfo, RenderedCard
from endfield_cards.rendering import RenderEngine
from endfield_cards.utils.selection import bundle_render


def profile(count=3):
    player = PlayerIdentity(name="Owner", game_uid="123", skport_id="social")
    return PlayerCard(
        player=player,
        source_scope="public",
        characters=[
            CharacterBuild(
                identity=CharacterIdentity(skport_id=f"opaque-{i}", str_id=f"canonical-{i}"),
                owner=player,
                name=f"Character {i}",
                showcase_index=7 - i if i < 8 else None,
            )
            for i in range(count)
        ],
    )


def card(family="profile"):
    return CardResult(b"encoded image", "PNG", 16, 16, family, "overview")


def test_character_selector_order_source_slot_and_filter_pagination():
    model = profile(9)
    bundle = bundle_render("profile", model, [card()], context_for(model))
    assert isinstance(bundle.info, CharacterListInfo)
    assert [(c.index, c.id, c.name, c.showcase_index) for c in bundle.info.characters[:2]] == [
        (0, "opaque-0", "Character 0", 7),
        (1, "opaque-1", "Character 1", 6),
    ]
    assert bundle.info.characters[8].page == 2 and bundle.info.characters[8].page_index == 0
    roster = bundle_render(
        "roster", model, [card("roster")], context_for(model), character_ids=["canonical-2", "opaque-0"]
    )
    assert [c.id for c in roster.info.characters] == ["opaque-0", "opaque-2"]
    assert [(c.index, c.source_index) for c in roster.info.characters] == [(0, 0), (1, 2)]


def test_bundle_model_access_and_info_never_mutate_rendered_source():
    model = profile()
    bundle = bundle_render("profile", model, [card()], context_for(model))
    model.characters[0].name = "Original mutated"
    first = bundle.model
    first.characters[0].name = "Copy mutated"
    assert bundle.model.characters[0].name == "Character 0"
    assert bundle.info.characters[0].name == "Character 0"
    assert bundle.card.data == b"encoded image"
    with pytest.raises(FrozenInstanceError):
        bundle.info.characters[0].name = "Invalid"
    with pytest.raises(ValueError):
        _ = RenderedCard([card(), card()], model, None).card


def test_live_data_preserves_five_sections_missing_fields_and_utc_deadlines():
    player = profile().player
    clock = datetime(2026, 11, 24, 12, tzinfo=UTC)
    model = LiveStatus(
        player=player,
        server_time=clock,
        sanity=ResourceMeter(current=100, maximum=360, recovery_at=clock + timedelta(hours=2)),
        daily=ResourceMeter(current=0, maximum=100),
        weekly=ResourceMeter(current=9, maximum=10),
        battle_pass=ResourceMeter(current=60, maximum=60),
        credits=ResourceMeter(current=200, maximum=300, refresh_at=clock + timedelta(hours=3)),
        current_event={
            "war_echoes": {
                "seasons": [
                    {
                        "id": "season",
                        "name": "Season",
                        "weeks": [
                            {
                                "id": "cycle",
                                "name": "Cycle",
                                "stars": 0,
                                "dungeonGroups": [{"name": "Stage", "star": 0}],
                            }
                        ],
                    }
                ]
            },
            "crisis_contract": [
                {
                    "id": "cc",
                    "name": "Contract",
                    "highest": 0,
                    "weeklyMission": {"count": 0, "total": 7},
                    "gameplayEndAtTs": int((clock + timedelta(days=1)).timestamp()),
                }
            ],
        },
    )
    bundle = bundle_render(
        "live", model, [card("activity")], replace(context_for(model), display_timezone="Asia/Kolkata")
    )
    assert isinstance(bundle.info, LiveInfo)
    assert bundle.info.fully_replenished_at == clock + timedelta(hours=2)
    assert bundle.info.credits.refresh_at.tzinfo is UTC
    assert bundle.info.daily.current == 0 and bundle.info.weekly.current == 9
    assert bundle.info.battle_pass.complete is True
    assert bundle.info.war_echoes.cycle.id == "cycle" and bundle.info.war_echoes.cycle.stages[0].stars == 0
    assert bundle.info.contingency_contract.id == "cc" and bundle.info.contingency_contract.best_score == 0
    model.sanity = None
    model.credits = ResourceMeter(name="Unavailable source")
    info = bundle_render("live", model, [card()], context_for(model)).info
    assert (
        info.fully_replenished_at is None and info.credits.current is None and info.credits.complete is None
    )


def test_monument_and_contract_preserve_actual_stage_selectors():
    player = profile().player
    monument = MonumentState(
        player=player,
        events=[
            MonumentEvent(
                id="event",
                name="Event",
                stages=[EventStage(id="stage", normal_id="normal", hard_id="hard", name="Stage")],
            )
        ],
    )
    info = bundle_render("monument", monument, [card()], context_for(monument)).info
    assert isinstance(info, MonumentInfo)
    stage = info.events[0].stages[0]
    assert (stage.event_id, stage.id, stage.normal_id, stage.hard_id) == ("event", "stage", "normal", "hard")
    contract = ContractState(
        player=player,
        current=CrisisContract(
            id="contract", name="Contract", stage_id="dungeon", stage_name="Stage", stage_recommended_level=0
        ),
    )
    info = bundle_render("contingency_contract", contract, [card()], context_for(contract)).info
    assert isinstance(info, ContractInfo)
    assert info.contracts[0].stage_id == "dungeon" and info.contracts[0].stage_recommended_level == 0
    assert info.contracts[0].best_score is None  # absent SDK default is not an observed zero


@pytest.mark.parametrize(
    "value,expected", [(0, 0), (60, 60), ("60", 60), (True, None), (2.5, None), ("bad", None), (None, None)]
)
def test_sdk_retains_dungeon_identity_without_fabricating_recommended_levels(value, expected):
    source = {
        "crisisContract": {
            "status": {"id": "contract"},
            "dungeon": {"id": "stage", "name": "Stage", "recommendLevel": value},
        }
    }
    state = build_contract_report(source, profile().player, ImageSource.SKPORT)
    assert state.current.stage_id == "stage" and state.current.stage_name == "Stage"
    assert state.current.stage_recommended_level == expected


@pytest.mark.asyncio
async def test_facade_captures_model_before_async_work_and_keeps_injected_sdk_borrowed(monkeypatch):
    entered, release = asyncio.Event(), asyncio.Event()
    sdk = SimpleNamespace(endfield=SimpleNamespace())
    model = profile()

    async def draw(self, family, snapshot, **kwargs):
        entered.set()
        await release.wait()
        return [card(family)]

    monkeypatch.setattr(RenderEngine, "render", draw)
    async with RenderEngine(skport=sdk) as cards:
        pending = asyncio.create_task(cards.render_profile_with_data(model))
        await entered.wait()
        model.characters[0].name = "Changed while rendering"
        release.set()
        response = await pending
        assert cards.skport is sdk and response.info.characters[0].name == "Character 0"
        response.model.characters[0].name = "Another copy"
        assert response.model.characters[0].name == "Character 0"


@pytest.mark.asyncio
async def test_actual_live_with_data_keeps_legacy_image_method_and_utc_time_data():
    model = LiveStatus(player=profile().player, server_time=datetime(2026, 11, 24, 12, tzinfo=UTC))
    async with RenderEngine() as cards:
        legacy = await cards.render_live(model)
        result = await cards.render_live_with_data(
            model, context=replace(context_for(model), display_timezone="Asia/Kolkata")
        )
    assert len(legacy) == len(result.cards) == 1 and result.card.data == legacy[0].data
    assert isinstance(result.info, LiveInfo) and result.info.server_time.tzinfo is UTC


@pytest.mark.asyncio
async def test_selected_monument_card_and_info_use_the_same_event():
    player = profile().player
    model = MonumentState(
        player=player, events=[MonumentEvent(id=f"event-{i}", name=f"Event {i}") for i in range(3)]
    )
    async with RenderEngine() as cards:
        result = await cards.render_monument_with_data(model, event_id="event-2")
    assert len(result.cards) == 1
    assert [(event.index, event.id) for event in result.info.events] == [(2, "event-2")]
    assert len(result.model.events) == 3
