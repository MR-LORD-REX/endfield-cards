"""Owner endgame reviews use safe credentials, source selectors and injected SDKs."""

from __future__ import annotations

import importlib
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest
from skport.games.endfield.models import (
    ContractState,
    CrisisContract,
    EventStage,
    MonumentEvent,
    MonumentState,
    PlayerCard,
    PlayerIdentity,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.models import CardResult, OwnerIdentity
from endfield_cards.utils.drawing import PageCanvas


@pytest.fixture
def review(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "tools"))
    return importlib.import_module("render_endgame")


def profile() -> PlayerCard:
    return PlayerCard(
        player=PlayerIdentity(skport_id="main-owner", game_uid="123456", name="Main Owner"),
        source_scope="owner",
        roster_complete=True,
    )


def monument(owner=None) -> MonumentState:
    return MonumentState(
        player=owner or profile().player,
        events=[
            MonumentEvent(
                id="event-1",
                name="Observed Event",
                stages=[
                    EventStage(id="stage-1", name="Observed Stage", normal_id="normal-1", hard_id="hard-1")
                ],
            )
        ],
    )


def contract(owner=None) -> ContractState:
    item = CrisisContract(
        id="contract-1",
        name="Observed Contract",
        stage_id="dungeon-1",
        stage_name="Observed Dungeon",
        stage_recommended_level=40,
    )
    return ContractState(player=owner or profile().player, current=item, contracts=[item])


def test_endgame_report_preserves_source_event_and_difficulty_selectors(review):
    result = review.model_report(monument(), "saved-snapshot", None)
    assert result["events"] == [
        {
            "index": 0,
            "id": "event-1",
            "name": "Observed Event",
            "stages": [
                {
                    "index": 0,
                    "id": "stage-1",
                    "name": "Observed Stage",
                    "normal_id": "normal-1",
                    "hard_id": "hard-1",
                }
            ],
        }
    ]
    entry = review.model_report(contract(), "saved-snapshot", None)["contracts"][0]
    assert entry["id"] == "contract-1" and entry["stage_id"] == "dungeon-1"
    assert entry["stage_name"] == "Observed Dungeon" and entry["stage_recommended_level"] == 40
    state = contract()
    state.contracts = []
    assert review.model_report(state, "saved-snapshot", None)["contracts"][0]["id"] == "contract-1"


def test_endgame_validation_checks_owner_server_and_output_component(review):
    review.verify_models({"m": monument(), "c": contract()})
    foreign = PlayerIdentity(skport_id="another", name="Another Owner", game_uid="wrong")
    with pytest.raises(ValueError, match="same owner"):
        review.verify_models({"m": monument(), "c": contract(foreign)})
    unsafe = PlayerIdentity(skport_id="../outside", name="Owner", game_uid="123456")
    with pytest.raises(ValueError, match="output-directory"):
        review.verify_models({"m": monument(unsafe)})
    first, second = monument(), contract()
    first.player.server_id = "server-a"
    second.player = second.player.model_copy(update={"server_id": "server-b"})
    with pytest.raises(ValueError, match="same owner"):
        review.verify_models({"m": first, "c": second})


async def test_supplied_endgame_models_do_not_initialize_auth_and_inject_matching_profile(
    review, monkeypatch, tmp_path
):
    models = {"monument": monument(), "contract": contract(), "profile": profile()}
    for family, model in models.items():
        (tmp_path / f"{family}.json").write_text(model.model_dump_json(), encoding="utf-8")

    def unexpected(*args, **kwargs):
        pytest.fail("Supplied snapshots must not initialize authentication")

    calls = []

    class Renderer:
        def __init__(self, *, config, skport):
            assert skport is None

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            pass

        async def render(self, family, model, **options):
            calls.append(family)
            assert options["profile"].player == models["profile"].player
            assert options["context"].display_timezone == "UTC"
            return [CardResult(b"test-card", "JPEG", 1600, 1000, family, "dark")]

    monkeypatch.setattr(review, "SkportClient", unexpected)
    monkeypatch.setattr(review, "Cards", Renderer)
    result = await review.main(
        [
            "--monument-snapshot",
            str(tmp_path / "monument.json"),
            "--contract-snapshot",
            str(tmp_path / "contract.json"),
            "--profile-snapshot",
            str(tmp_path / "profile.json"),
            "--variant",
            "dark",
            "--output-dir",
            str(tmp_path / "out"),
        ]
    )
    assert calls == ["monument", "contingency_contract"] and len(result["images"]) == 2
    assert sorted(path.name for path in (tmp_path / "out/main-owner").glob("*.jpg")) == [
        "contingency-contract-dark.jpg",
        "monument-dark.jpg",
    ]
    assert not (tmp_path / "out/main-owner/monument.json").exists()


async def test_mismatched_snapshots_fail_before_auth_or_render(review, monkeypatch, tmp_path):
    first, second = monument(), contract(PlayerIdentity(skport_id="other", name="Other", game_uid="wrong"))
    paths = [tmp_path / "m.json", tmp_path / "c.json"]
    for path, model in zip(paths, (first, second), strict=True):
        path.write_text(model.model_dump_json(), encoding="utf-8")
    monkeypatch.setattr(
        review, "SkportClient", lambda **kwargs: pytest.fail("Validation should precede auth")
    )
    with pytest.raises(ValueError, match="same owner"):
        await review.main(
            ["--monument-snapshot", str(paths[0]), "--contract-snapshot", str(paths[1]), "--fetch-only"]
        )


async def test_fetch_uses_owner_identity_and_injected_sdk_and_closes_without_printing_token(
    review, monkeypatch, tmp_path, capsys
):
    token = "private-token-do-not-print"
    monkeypatch.setattr(review, "load_account_token", lambda arguments: token)
    instances, fetched = [], []

    class SDK:
        def __init__(self, *, tokens, config):
            assert tokens == [token] and config.calculate_stats is False
            self.endfield = self
            self.closed = False
            instances.append(self)

        async def warm(self):
            pass

        async def owned_card(self, **options):
            assert options["token"] == token
            return profile()

        async def close(self):
            self.closed = True

    async def fetch(sdk, family, owner):
        assert sdk is instances[0] and owner.player == profile().player
        fetched.append(family)
        return monument() if family == "monument" else contract()

    monkeypatch.setattr(review, "SkportClient", SDK)
    monkeypatch.setattr(review, "fetch_model", fetch)
    result = await review.main(["--fetch-only", "--output-dir", str(tmp_path)])
    assert fetched == ["monument", "contingency_contract"] and instances[0].closed
    assert result["images"] == []
    assert (tmp_path / "main-owner/monument.json").exists()
    assert (tmp_path / "main-owner/contingency-contract.json").exists()
    assert token not in capsys.readouterr().out
    assert token not in "".join(path.read_text(encoding="utf-8") for path in tmp_path.rglob("*.json"))


async def test_detailed_sdk_endpoints_are_read_once_and_normalized_with_owned_roster(review):
    calls = []
    owner = profile()
    target = object()

    class Game:
        def __init__(self):
            self.raw = self

        async def resolve(self, skport_id, **options):
            assert skport_id == owner.player.skport_id
            calls.append("resolve")
            return target

        async def indie_hard(self, resolved):
            assert resolved is target
            calls.append("monument")
            return {"indieHardGroups": [{"id": "event-1", "name": "Event", "dungeonGroups": []}]}

        async def crisis_contract(self, resolved):
            assert resolved is target
            calls.append("contract")
            return {
                "crisisContract": {
                    "status": {"id": "contract-1", "name": "Contract"},
                    "dungeon": {"id": "actual-stage", "name": "Actual stage", "recommendLevel": 42},
                }
            }

    class SDK:
        endfield = Game()

    first = await review.fetch_model(SDK(), "monument", owner)
    second = await review.fetch_model(SDK(), "contingency_contract", owner)
    assert first.events[0].id == "event-1" and second.current.stage_id == "actual-stage"
    assert second.current.stage_name == "Actual stage" and second.current.stage_recommended_level == 42
    assert calls == ["resolve", "monument", "resolve", "contract"]


def test_every_footer_keeps_owners_and_page_numbers_without_source_timestamps(monkeypatch):
    model = profile()
    context = replace(
        context_for(model),
        snapshot_at=datetime(2026, 11, 24, 12, 30, tzinfo=UTC),
        display_timezone="Asia/Kolkata",
        comparison_owner=OwnerIdentity("Second Owner", "98765"),
    )
    canvas = PageCanvas("Footer", context)
    output = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        output.append(str(value))
        return original(self, x, y, value, **options)

    monkeypatch.setattr(PageCanvas, "text", capture)
    canvas.finish(2, 7)
    drawn = "\n".join(output)
    assert "Main Owner" in drawn and "Second Owner" in drawn
    assert "UID 123456" in drawn and "UID 98765" in drawn
    assert "akef-cards · endfield-cards" in drawn and "02 / 07" in drawn
    assert "2026" not in drawn and "UTC" not in drawn and "IST" not in drawn
    canvas.image.close()
