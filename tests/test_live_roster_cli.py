"""Owner live/roster review uses literal TOKEN input and preserves source identity."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    LiveStatus,
    PlayerCard,
    PlayerIdentity,
)

from endfield_cards.errors import OwnerMismatchError
from endfield_cards.models import CardResult


@pytest.fixture
def review(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "tools"))
    return importlib.import_module("render_live_roster")


def owner_roster() -> PlayerCard:
    player = PlayerIdentity(skport_id="owner-main", game_uid="12345", name="Main Owner")
    return PlayerCard(
        player=player,
        source_scope="owner",
        roster_complete=True,
        characters=[
            CharacterBuild(
                identity=CharacterIdentity(skport_id="opaque-character", str_id="canonical-character"),
                owner=player,
                name="Observed operator",
            )
        ],
    )


@pytest.mark.parametrize(
    "line,expected",
    [
        ("TOKEN=literal-token", "literal-token"),
        ("export TOKEN = 'literal-token' # comment", "literal-token"),
        ('TOKEN="literal-token"', "literal-token"),
        ("TOKEN=literal-token # comment", "literal-token"),
        ("TOKEN='$(do-not-execute)'", "$(do-not-execute)"),
    ],
)
def test_dotenv_token_is_literal_and_never_changes_process_environment(
    review, tmp_path, monkeypatch, line, expected
):
    path = tmp_path / ".env"
    path.write_text("IGNORED=value\n" + line + "\n", encoding="utf-8")
    monkeypatch.delenv("TOKEN", raising=False)
    assert review.token_from_env_file(path) == expected
    assert "TOKEN" not in review.os.environ


@pytest.mark.parametrize("value", ["", "'private value'", "'private-value", '"private-value" trailing'])
def test_invalid_dotenv_errors_never_echo_private_content(review, tmp_path, value):
    path = tmp_path / ".env"
    path.write_text("TOKEN=" + value, encoding="utf-8")
    with pytest.raises(ValueError) as error:
        review.token_from_env_file(path)
    assert "private" not in str(error.value)


def test_explicit_env_file_selects_main_account_before_existing_environment_token(
    review, monkeypatch, tmp_path
):
    path = tmp_path / ".env"
    path.write_text("TOKEN=main-account", encoding="utf-8")
    monkeypatch.setenv("TOKEN", "different-account")
    arguments = review.parser().parse_args(["--env-file", str(path)])
    assert review.load_account_token(arguments) == "main-account"
    token_file = tmp_path / "token.txt"
    token_file.write_text("explicit-account", encoding="utf-8")
    arguments.token_file = token_file
    assert review.load_account_token(arguments) == "explicit-account"


def test_roster_requires_owner_scope_and_matching_character_owner(review):
    model = owner_roster()
    review.verify_owner_roster(model)
    model.source_scope = "public"
    with pytest.raises(ValueError, match="owner roster"):
        review.verify_owner_roster(model)
    model.source_scope = "owner"
    model.characters[0].owner = PlayerIdentity(skport_id="other", game_uid="wrong", name="Other")
    with pytest.raises(OwnerMismatchError):
        review.verify_owner_roster(model)
    model.characters = []
    model.player.skport_id = "../outside"
    with pytest.raises(ValueError, match="output-directory"):
        review.verify_owner_roster(model)


async def test_two_supplied_snapshots_render_without_authentication_or_new_snapshot_files(
    review, monkeypatch, tmp_path
):
    roster = owner_roster()
    live = LiveStatus(player=roster.player)
    paths = {"roster": tmp_path / "roster.json", "live": tmp_path / "live.json"}
    paths["roster"].write_text(roster.model_dump_json(), encoding="utf-8")
    paths["live"].write_text(live.model_dump_json(), encoding="utf-8")

    def unexpected(*args, **kwargs):
        pytest.fail("Supplied normalized snapshots must not initialize authentication")

    class Renderer:
        def __init__(self, *, config, skport):
            assert skport is None

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            pass

        async def render(self, family, model, **kwargs):
            assert kwargs["variant"] == "dark"
            if family == "activity":
                assert kwargs["profile"].player == roster.player
                assert kwargs["context"].source_scope == "owner"
            return [CardResult(b"observed-image", "JPEG", 100, 80, family, "dark", 1, 1)]

    monkeypatch.setattr(review, "SkportClient", unexpected)
    monkeypatch.setattr(review, "RenderEngine", Renderer)
    report = await review.main(
        [
            "--roster-snapshot",
            str(paths["roster"]),
            "--live-snapshot",
            str(paths["live"]),
            "--variant",
            "dark",
            "--output-dir",
            str(tmp_path / "outputs"),
        ]
    )
    output = tmp_path / "outputs/owner-main"
    assert sorted(path.name for path in output.glob("*.jpg")) == ["live-dark.jpg", "roster-dark.jpg"]
    assert not (output / "roster.json").exists() and not (output / "live.json").exists()
    assert len(report["images"]) == 2
    assert all(source["source_mode"] == "saved-snapshot" for source in report["sources"].values())


async def test_live_fetch_uses_explicit_owner_endpoint_without_per_character_fanout_and_closes_sdk(
    review, monkeypatch, tmp_path, capsys
):
    roster = owner_roster()
    calls = []
    instances = []
    token = "private-main-token-do-not-print"
    monkeypatch.setattr(review, "load_account_token", lambda args: token)

    class SDK:
        def __init__(self, *, tokens, config):
            assert tokens == [token]
            assert config.calculate_stats is False and config.cache is False
            self.endfield = self
            self.closed = False
            instances.append(self)

        async def warm(self):
            pass

        async def owned_card(self, **kwargs):
            assert kwargs["token"] == token
            calls.append(kwargs.copy())
            if kwargs.get("raw"):
                return {
                    "detail": {"dungeon": {"curStamina": 1000, "maxStamina": 360}, "currentTs": 1788000000}
                }
            return roster

        async def close(self):
            self.closed = True

    monkeypatch.setattr(review, "SkportClient", SDK)
    report = await review.main(["--fetch-only", "--output-dir", str(tmp_path)])
    assert len(calls) == 2 and calls[1]["raw"] is True
    assert instances[0].closed
    assert report["sources"]["roster"]["source_scope"] == "owner"
    assert report["images"] == []
    saved = LiveStatus.model_validate_json((tmp_path / "owner-main/live.json").read_text(encoding="utf-8"))
    assert saved.sanity.current == 1000 and saved.sanity.maximum == 360
    assert token not in capsys.readouterr().out
    assert token not in "".join(
        path.read_text(encoding="utf-8") for path in (tmp_path / "owner-main").glob("*.json")
    )


async def test_mismatched_snapshot_owners_are_rejected_before_render(review, monkeypatch, tmp_path):
    roster = owner_roster()
    live = LiveStatus(player=PlayerIdentity(skport_id="other", game_uid="222", name="Other"))
    paths = tmp_path / "roster.json", tmp_path / "live.json"
    paths[0].write_text(roster.model_dump_json(), encoding="utf-8")
    paths[1].write_text(live.model_dump_json(), encoding="utf-8")

    def unexpected(*args, **kwargs):
        pytest.fail("Identity mismatch must fail before rendering/authentication")

    monkeypatch.setattr(review, "SkportClient", unexpected)
    monkeypatch.setattr(review, "RenderEngine", unexpected)
    with pytest.raises(ValueError, match="same owner"):
        await review.main(["--roster-snapshot", str(paths[0]), "--live-snapshot", str(paths[1])])
