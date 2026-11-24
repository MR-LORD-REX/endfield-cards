"""Comparison review commands preserve explicit target ownership and source mode."""

from __future__ import annotations

import argparse
import importlib
import io
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image
from skport.games.endfield.models import CharacterBuild, CharacterIdentity, PlayerCard, PlayerIdentity

from endfield_cards.errors import DataValidationError
from endfield_cards.models import CardResult


@pytest.fixture
def review(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "tools"))
    return importlib.import_module("render_compare")


def build(target: str, uid: str, name: str) -> CharacterBuild:
    return CharacterBuild(
        identity=CharacterIdentity(skport_id="same-opaque-id", str_id="chr_same", template_id=30),
        owner=PlayerIdentity(skport_id=target, game_uid=uid, name=name),
        name="Character Same",
        level=60,
        max_level=80,
    )


def test_pair_output_includes_both_owners_and_rejects_unsafe_components(review):
    first, second = build("owner-a", "111", "One"), build("owner-b", "222", "Two")
    assert review.output_pair(first, second) == ("owner-a", "owner-b", "chr_same")
    assert review.output_pair(first, first) == ("owner-a", "owner-a", "chr_same")
    first.owner.skport_id = "../outside"
    with pytest.raises(ValueError, match="output-directory"):
        review.output_pair(first, second)


@pytest.mark.parametrize(
    "options",
    [
        [],
        ["--first-skport-id", "owner-a"],
        ["--name", "Character Same"],
        ["--first-skport-id", "owner-a", "--name", "Character Same", "--first-character-id", "opaque"],
    ],
)
def test_live_selection_requires_target_and_one_selector(review, options):
    with pytest.raises(ValueError):
        review.selection_for(review.parser().parse_args(options), "first")


async def test_missing_character_owner_name_uses_verified_profile_and_copies_model(review):
    model = build("owner-a", "111", "")
    profile = PlayerCard(player=PlayerIdentity(skport_id="owner-a", game_uid="111", name="Game Name"))
    calls = []

    async def character(**kwargs):
        calls.append(kwargs)
        return model

    async def card(**kwargs):
        assert kwargs == {"skport_id": "owner-a"}
        return profile

    sdk = SimpleNamespace(endfield=SimpleNamespace(character=character, card=card))
    selection = argparse.Namespace(skport_id="owner-a", character_id="same-opaque-id", name=None)
    result = await review.fetch_character(sdk, selection)
    assert result.owner.name == "Game Name"
    assert model.owner.name == ""
    assert calls == [{"skport_id": "owner-a", "full": True, "char_id": "same-opaque-id"}]
    profile.player.game_uid = "other-game-owner"
    with pytest.raises(ValueError, match="different game owners"):
        await review.fetch_character(sdk, selection)


async def test_two_live_targets_one_image_safe_reports_and_client_cleanup(
    review, monkeypatch, tmp_path, capsys
):
    models = {"owner-a": build("owner-a", "111", "One"), "owner-b": build("owner-b", "222", "Two")}
    calls = []
    instances = []
    private_token = "private-token-must-not-escape"
    monkeypatch.setattr(review, "load_tokens", lambda path: [private_token])

    class SDK:
        def __init__(self, *, tokens, config):
            assert tokens == [private_token]
            assert config.calculate_stats is True and config.cache is False
            self.endfield = self
            self.closed = False
            instances.append(self)

        async def warm(self):
            pass

        async def character(self, **kwargs):
            calls.append(kwargs)
            return models[kwargs["skport_id"]]

        async def close(self):
            self.closed = True

    class Renderer:
        def __init__(self, *, config, skport):
            assert skport is instances[0]

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            pass

        async def render_compare(self, first, second, **kwargs):
            assert first.owner.game_uid == "111" and second.owner.game_uid == "222"
            assert kwargs["context"].owner.name == "One" and kwargs["second_context"].owner.name == "Two"
            assert kwargs["details"] is False and kwargs["variant"] == "terminal"
            assert kwargs["art"] is None and kwargs["second_art"] is None
            output = io.BytesIO()
            with Image.new("RGB", (16, 10), "yellow") as pixels:
                pixels.save(output, format="PNG")
            return [CardResult(output.getvalue(), "PNG", 16, 10, "character", "terminal")]

    monkeypatch.setattr(review, "SkportClient", SDK)
    monkeypatch.setattr(review, "Cards", Renderer)
    report = await review.main(
        [
            "--first-skport-id",
            "owner-a",
            "--second-skport-id",
            "owner-b",
            "--name",
            "Character Same",
            "--variant",
            "terminal",
            "--format",
            "PNG",
            "--output-dir",
            str(tmp_path),
        ]
    )
    assert calls == [
        {"skport_id": "owner-a", "full": True, "name": "Character Same"},
        {"skport_id": "owner-b", "full": True, "name": "Character Same"},
    ]
    assert instances[0].closed
    output = tmp_path / "owner-a/owner-b/chr_same"
    assert (output / "compare-terminal.png").is_file()
    assert (output / "first-character.json").is_file() and (output / "second-character.json").is_file()
    assert report["images"] == 1 and report["detail_images"] == []
    assert report["first"]["source_mode"] == "live-api" and report["first"]["fetched_at"]
    assert not (output / "details").exists()
    assert private_token not in capsys.readouterr().out
    assert all(private_token not in path.read_text() for path in output.glob("*.json"))


async def test_snapshot_pair_mismatch_stops_before_auth_or_render(review, monkeypatch, tmp_path):
    first, second = build("owner-a", "111", "One"), build("owner-b", "222", "Two")
    second.identity.str_id = "chr_other"
    snapshots = [tmp_path / "first.json", tmp_path / "second.json"]
    for path, model in zip(snapshots, (first, second), strict=True):
        path.write_text(model.model_dump_json(), encoding="utf-8")

    def unexpected(*args, **kwargs):
        pytest.fail("Supplied snapshots must not initialize authentication or render mismatched operators")

    monkeypatch.setattr(review, "SkportClient", unexpected)
    monkeypatch.setattr(review, "Cards", unexpected)
    with pytest.raises(DataValidationError, match="same canonical"):
        await review.main(
            [
                "--first-snapshot",
                str(snapshots[0]),
                "--second-snapshot",
                str(snapshots[1]),
                "--output-dir",
                str(tmp_path / "outputs"),
            ]
        )
    assert not (tmp_path / "outputs").exists()


async def test_explicit_details_keeps_snapshot_sources_and_separate_exports(review, monkeypatch, tmp_path):
    models = [build("owner-a", "111", "One"), build("owner-b", "222", "Two")]
    snapshots = [tmp_path / "first.json", tmp_path / "second.json"]
    for path, model in zip(snapshots, models, strict=True):
        path.write_text(model.model_dump_json(), encoding="utf-8")

    def unexpected(*args, **kwargs):
        pytest.fail("Two supplied snapshots must not initialize authentication")

    class Renderer:
        def __init__(self, *, config, skport):
            assert skport is None

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            pass

        async def render_compare(self, first, second, **kwargs):
            assert kwargs["details"] is True
            return [
                CardResult(b"explicit-image", "JPEG", 16, 10, "character", "field", page, 3)
                for page in range(1, 4)
            ]

    monkeypatch.setattr(review, "SkportClient", unexpected)
    monkeypatch.setattr(review, "Cards", Renderer)
    report = await review.main(
        [
            "--first-snapshot",
            str(snapshots[0]),
            "--second-snapshot",
            str(snapshots[1]),
            "--details",
            "--output-dir",
            str(tmp_path / "outputs"),
        ]
    )
    output = tmp_path / "outputs/owner-a/owner-b/chr_same"
    assert report["images"] == 3 and len(report["detail_images"]) == 2
    assert report["first"]["source_mode"] == "saved-snapshot" and report["first"]["fetched_at"] is None
    assert sorted(path.name for path in (output / "details").glob("*.jpg")) == [
        "compare-field-02.jpg",
        "compare-field-03.jpg",
    ]
    assert len(list(output.glob("*.jpg"))) == 1
    assert not (output / "first-character.json").exists()
