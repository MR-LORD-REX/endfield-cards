"""Specific card requests preserve selectors, SDK ownership and rendered snapshots."""

from __future__ import annotations

import io
from datetime import UTC, datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from PIL import Image
from skport import ClientConfig, Role
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    LiveStatus,
    PlayerCard,
    PlayerIdentity,
    ResourceMeter,
)

from endfield_cards import TEMPLATES, VARIANTS, CardResult, Cards, CardsConfig, OutputConfig
from endfield_cards.assets.store import AssetStore
from endfield_cards.errors import DataValidationError
from endfield_cards.models import CharacterListInfo, LiveInfo
from endfield_cards.rendering import RenderEngine


def player_card(skport_id: str, *, scope: str = "public") -> PlayerCard:
    owner = PlayerIdentity(name=f"Player {skport_id}", game_uid=f"game-{skport_id}", skport_id=skport_id)
    return PlayerCard(
        player=owner,
        source_scope=scope,
        characters=[
            CharacterBuild(
                owner=owner,
                identity=CharacterIdentity(skport_id=f"{skport_id}-opaque", str_id="same-operator"),
                name="Selected operator",
                showcase_index=0,
            )
        ],
    )


@pytest.fixture
def sdk():
    async def card(**ids):
        return player_card(str(ids["skport_id"]))

    async def character(**ids):
        return player_card(str(ids["skport_id"])).characters[0]

    async def owned_card(**ids):
        return player_card("owned", scope="owner")

    async def owned_character(**ids):
        return player_card("owned", scope="owner").characters[0]

    async def owned_characters(**ids):
        return player_card("owned", scope="owner").characters

    source_time = datetime(2026, 11, 25, 12, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    activity = LiveStatus(
        player=player_card("owned").player,
        server_time=source_time,
        sanity=ResourceMeter(key="sanity", current=25, maximum=100, recovery_at=source_time + timedelta(hours=2)),
    )
    game = SimpleNamespace(
        card=AsyncMock(side_effect=card),
        character=AsyncMock(side_effect=character),
        owned_card=AsyncMock(side_effect=owned_card),
        owned_character=AsyncMock(side_effect=owned_character),
        owned_characters=AsyncMock(side_effect=owned_characters),
        owned_activity=AsyncMock(return_value=activity),
        activity=AsyncMock(),
    )
    return SimpleNamespace(config=ClientConfig(), endfield=game, close=AsyncMock())


@pytest.fixture
def draws(monkeypatch):
    calls = []

    async def render(self, family, model, **options):
        calls.append((family, model, options))
        return [CardResult(b"routing-preview", options["output"].format, 10, 10, family, options["variant"])]

    async def compare(self, first, second, **options):
        calls.append(("compare", (first, second), options))
        return [CardResult(b"routing-preview", options["output"].format, 10, 10, "character", options["variant"])]

    monkeypatch.setattr(RenderEngine, "render", render)
    monkeypatch.setattr(RenderEngine, "render_compare", compare)
    return calls


@pytest.mark.asyncio
async def test_omitted_character_selector_selects_sdk_index_zero(sdk, draws):
    async with Cards(sdk) as cards:
        result = await cards.character_card("first")
    ids = sdk.endfield.character.await_args.kwargs
    assert ids["index"] == 0 and "char_id" not in ids and "name" not in ids
    assert result.model.identity.skport_id == "first-opaque"


@pytest.mark.parametrize(
    "selectors",
    [
        {"char_id": "opaque", "name": "Operator"},
        {"char_id": "opaque", "index": 0},
        {"name": "Operator", "index": 0},
        {"index": -1},
        {"index": True},
        {"char_id": " "},
        {"name": " "},
    ],
)
@pytest.mark.asyncio
async def test_invalid_character_selectors_fail_before_fetch(sdk, draws, selectors):
    async with Cards(sdk) as cards:
        with pytest.raises(DataValidationError):
            await cards.character_card("first", **selectors)
    sdk.endfield.character.assert_not_awaited()
    assert draws == []


@pytest.mark.asyncio
async def test_owner_profile_and_character_forward_explicit_token_role_and_language(sdk, draws):
    role = Role("game-owned", "server")
    async with Cards(sdk, config=CardsConfig(locale="ja")) as cards:
        profile = await cards.profile_card(token="owner-token", role=role)
        character = await cards.character_card(token="owner-token", role=role, char_id="owned-opaque")
    sdk.endfield.owned_card.assert_awaited_once_with(token="owner-token", role=role, lang="ja")
    sdk.endfield.owned_character.assert_awaited_once_with(
        token="owner-token", role=role, lang="ja", char_id="owned-opaque", full=True
    )
    sdk.endfield.card.assert_not_awaited()
    sdk.endfield.character.assert_not_awaited()
    assert profile.info.source_scope == "owner" and character.model.owner.skport_id == "owned"
    assert all(options["context"].locale == "ja" for _, _, options in draws)
    sdk.close.assert_not_awaited()


@pytest.mark.asyncio
async def test_owner_live_uses_authenticated_activity_and_profile_and_utc_context(sdk, draws):
    role = Role("game-owned", "server")
    config = CardsConfig(locale="ko", display_timezone="Asia/Calcutta")
    async with Cards(sdk, config=config) as cards:
        result = await cards.live_card(token="owner-token", role=role)
    sdk.endfield.owned_activity.assert_awaited_once_with(token="owner-token", role=role, lang="ko")
    sdk.endfield.owned_card.assert_awaited_once_with(token="owner-token", role=role, lang="ko")
    sdk.endfield.activity.assert_not_awaited()
    sdk.endfield.card.assert_not_awaited()
    context = draws[0][2]["context"]
    assert context.source_scope == "owner" and context.display_timezone == "UTC"
    assert draws[0][2]["profile"].source_scope == "owner"
    assert isinstance(result.info, LiveInfo) and result.info.owner.game_uid == "game-owned"
    assert result.info.server_time == datetime(2026, 11, 25, 6, 30, tzinfo=UTC)
    assert result.info.fully_replenished_at == datetime(2026, 11, 25, 8, 30, tzinfo=UTC)
    assert result.info.server_time.tzinfo is result.info.fully_replenished_at.tzinfo is UTC


@pytest.mark.asyncio
async def test_empty_owned_roster_obtains_identity_from_owned_profile(sdk, draws):
    sdk.endfield.owned_characters.side_effect = None
    sdk.endfield.owned_characters.return_value = []
    async with Cards(sdk) as cards:
        result = await cards.all_characters_card("owner-token")
    sdk.endfield.owned_characters.assert_awaited_once_with(token="owner-token", role=None, lang="en", full=True)
    sdk.endfield.owned_card.assert_awaited_once_with(token="owner-token", role=None, lang="en")
    sdk.endfield.card.assert_not_awaited()
    assert result.model == [] and isinstance(result.info, CharacterListInfo)
    assert result.info.characters == () and result.info.source_scope == "owner"
    assert result.info.owner.game_uid == "game-owned"
    assert draws[0][2]["context"].owner.game_uid == "game-owned"


@pytest.mark.parametrize("second_char_id", [None, "second-opaque"])
@pytest.mark.asyncio
async def test_comparison_resolves_second_account_by_name_or_explicit_opaque_id(sdk, draws, second_char_id):
    async with Cards(sdk) as cards:
        result = await cards.compare_card("first", "second", char_id="first-opaque", second_char_id=second_char_id)
    first_call, second_call = sdk.endfield.character.await_args_list
    assert first_call.kwargs["char_id"] == "first-opaque"
    assert second_call.kwargs["skport_id"] == "second"
    if second_char_id is None:
        assert second_call.kwargs["name"] == "Selected operator" and "char_id" not in second_call.kwargs
    else:
        assert second_call.kwargs["char_id"] == second_char_id and "name" not in second_call.kwargs
    assert [build.identity.skport_id for build in result.model] == ["first-opaque", "second-opaque"]
    assert result.card.template == 1 and draws[0][2]["variant"] == "dossier"


@pytest.mark.asyncio
async def test_numeric_catalogs_are_copy_safe_and_distinct_from_engine_names(sdk):
    async with Cards(sdk) as cards, RenderEngine() as engine:
        catalog = cards.templates
        assert catalog == cards.variants == TEMPLATES == VARIANTS
        assert catalog["character"] == (1, 2, 3, 4)
        assert engine.variants["character"] == ("field", "dossier", "terminal", "portrait")
        catalog["character"] = (99,)
        assert cards.templates["character"] == (1, 2, 3, 4)
        engine_catalog = engine.variants
        engine_catalog["character"] = ("changed",)
        assert engine.variants["character"][0] == "field"
    with pytest.raises(TypeError):
        TEMPLATES["profile"] = (99,)


@pytest.mark.asyncio
async def test_public_profile_smoke_encodes_images_and_isolates_cached_caller_data(sdk, monkeypatch):
    async def unexpected_download(self, url, **options):
        raise AssertionError(f"This supplied SDK profile has no remote images: {url}")

    monkeypatch.setattr(AssetStore, "get", unexpected_download)
    config = CardsConfig(output=OutputConfig(format="JPEG", quality=80))
    async with Cards(sdk, config=config) as cards:
        first = await cards.profile_card("first", template=1)
        repeated = await cards.profile_card("first", template=1)
        other = await cards.profile_card("second", template=1)
        assert cards.cache_stats["renders"]["hits"] >= 1
    with Image.open(io.BytesIO(first.card.data)) as decoded:
        assert decoded.format == "JPEG" and decoded.size == (first.card.width, first.card.height)
    assert first.card.data == repeated.card.data and first.card.data != other.card.data
    assert first.card.template == 1 and not first.card.issues
    assert first.info.characters[0].id == "first-opaque"
    assert other.info.owner.game_uid == "game-second"
    caller_model = first.model
    caller_model.characters[0].name = "Changed by caller"
    assert first.model.characters[0].name == repeated.model.characters[0].name == "Selected operator"
    assert repeated.info.characters[0].name == "Selected operator"
    decoded = first.card.to_pillow()
    try:
        decoded.paste("black", (0, 0, decoded.width, decoded.height))
        assert repeated.card.data == first.card.data
    finally:
        decoded.close()
    sdk.close.assert_not_awaited()
