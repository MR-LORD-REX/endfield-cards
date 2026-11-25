"""SDK orchestration is public; drawing remains an independent engine concern."""

from __future__ import annotations

import asyncio
import inspect
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from skport import ClientConfig, Language, SkportAPI, SkportClient
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    ContractState,
    CrisisContract,
    FactoryState,
    LiveStatus,
    MonumentEvent,
    MonumentState,
    PlayerCard,
    PlayerIdentity,
    PullHistory,
    WikiPage,
    WikiSummary,
)

from endfield_cards import CardResult, Cards, CardsConfig, EFCard, OutputConfig
from endfield_cards.errors import (
    CardNotImplementedError,
    DataValidationError,
    FetchError,
    OwnerMismatchError,
    ResourceClosedError,
    UnsupportedVariantError,
)
from endfield_cards.models import (
    CharacterListInfo,
    ContractInfo,
    LiveInfo,
    MonumentInfo,
    OwnerIdentity,
    RenderedCard,
)
from endfield_cards.rendering.engine import RenderEngine


def profile(skport_id: str = "first", *, scope: str = "public") -> PlayerCard:
    owner = PlayerIdentity(name=f"Owner {skport_id}", game_uid=f"game-{skport_id}", skport_id=skport_id)
    return PlayerCard(
        player=owner,
        source_scope=scope,
        characters=[
            CharacterBuild(
                identity=CharacterIdentity(skport_id="opaque-character", str_id="canonical-character"),
                owner=owner,
                name="Character",
                showcase_index=3,
            )
        ],
    )


@pytest.fixture
def sdk() -> SimpleNamespace:
    async def public_card(**ids):
        return profile(str(ids["skport_id"]))

    async def character(**ids):
        return profile(str(ids["skport_id"])).characters[0]

    async def owned_card(**ids):
        return profile("owner", scope="owner")

    async def owned_characters(**ids):
        return profile("owner", scope="owner").characters

    async def activity(**ids):
        return LiveStatus(player=profile(str(ids.get("skport_id") or "owner")).player)

    async def factory(**ids):
        return FactoryState(player=profile(str(ids.get("skport_id") or "owner")).player)

    async def monument(**ids):
        return MonumentState(
            player=profile(str(ids.get("skport_id") or "owner")).player,
            events=[MonumentEvent(id="event", name="Event")],
        )

    async def contract(**ids):
        return ContractState(
            player=profile(str(ids.get("skport_id") or "owner")).player,
            current=CrisisContract(id="contract", name="Contract"),
        )

    game = SimpleNamespace(
        card=AsyncMock(side_effect=public_card),
        character=AsyncMock(side_effect=character),
        owned_card=AsyncMock(side_effect=owned_card),
        owned_characters=AsyncMock(side_effect=owned_characters),
        activity=AsyncMock(side_effect=activity),
        factory=AsyncMock(side_effect=factory),
        monument=AsyncMock(side_effect=monument),
        contract=AsyncMock(side_effect=contract),
    )
    return SimpleNamespace(endfield=game, config=ClientConfig(), close=AsyncMock())


@pytest.fixture
def draws(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, object, dict]]:
    calls = []

    async def draw(self, family, model, **options):
        calls.append((family, model, options))
        output = options["output"]
        return [CardResult(b"encoded-image", output.format, 16, 16, family, options["variant"])]

    monkeypatch.setattr(RenderEngine, "render", draw)
    return calls


def test_public_facade_requires_sdk_and_does_not_expose_rendering_methods():
    with pytest.raises((TypeError, ValueError)):
        Cards()
    assert EFCard is Cards
    assert not any(name.startswith("render") for name in dir(Cards))
    constructor = inspect.signature(Cards)
    assert "token" not in constructor.parameters and "tokens" not in constructor.parameters


def test_public_facade_rejects_ambiguous_sdk_and_api_injections(sdk):
    with pytest.raises((TypeError, ValueError)):
        Cards(skport=sdk, api=object())


@pytest.mark.asyncio
async def test_profile_fetches_explicit_target_and_returns_copy_safe_typed_bundle(sdk, draws):
    async with Cards(skport=sdk) as cards:
        result = await cards.profile_card("first", template=1)
        second = await cards.profile_card("second", template=3)
    assert isinstance(result, RenderedCard) and isinstance(result.info, CharacterListInfo)
    assert result.card.data == b"encoded-image" and result.info.characters[0].id == "opaque-character"
    assert result.card.variant == result.card.template == 1
    assert second.card.variant == second.card.template == 3
    assert result.model.player.skport_id == "first" and second.model.player.skport_id == "second"
    copy = result.model
    copy.characters[0].name = "Changed"
    assert result.model.characters[0].name == "Character"
    assert result.info.characters[0].name == "Character"
    assert [call.kwargs["skport_id"] for call in sdk.endfield.card.await_args_list] == ["first", "second"]
    assert [options["context"].owner.skport_id for _, _, options in draws] == ["first", "second"]
    assert [options["variant"] for _, _, options in draws] == ["overview", "identity"]
    sdk.close.assert_not_awaited()


@pytest.mark.asyncio
async def test_sdk_snapshot_with_mixed_owners_is_rejected_before_rendering(sdk, draws):
    model = profile("first")
    model.characters[0].owner = profile("second").player
    sdk.endfield.card.side_effect = None
    sdk.endfield.card.return_value = model
    async with Cards(skport=sdk) as cards:
        with pytest.raises(OwnerMismatchError):
            await cards.profile_card("first")
    assert draws == []


@pytest.mark.parametrize(
    "method,args,options,family,variants,info_type",
    [
        (
            "profile_card",
            ("first",),
            {},
            "profile",
            ("overview", "operations", "identity"),
            CharacterListInfo,
        ),
        (
            "character_card",
            ("first",),
            {"char_id": "opaque-character"},
            "character",
            ("dossier", "terminal", "field", "portrait"),
            type(None),
        ),
        ("all_characters_card", ("owner-token",), {}, "roster", ("light", "dark"), CharacterListInfo),
        ("live_card", ("first",), {}, "activity", ("light", "dark"), LiveInfo),
        ("factory_card", ("first",), {}, "factory", ("light", "dark"), type(None)),
        ("exploration_card", ("first",), {}, "exploration", ("light", "dark"), type(None)),
        ("monument_card", ("first",), {}, "monument", ("light", "dark"), MonumentInfo),
        (
            "monument_detailed_card",
            ("first",),
            {"event_id": "event"},
            "monument_detail",
            ("light", "dark"),
            MonumentInfo,
        ),
        (
            "contingency_contract_card",
            ("first",),
            {},
            "contingency_contract",
            ("light", "dark"),
            ContractInfo,
        ),
        (
            "contingency_contract_detailed_card",
            ("first",),
            {"contract_id": "contract"},
            "contingency_contract_detail",
            ("light", "dark"),
            ContractInfo,
        ),
        ("pulls_card", (PullHistory(player=profile().player),), {}, "pulls", ("light", "dark"), type(None)),
        (
            "wiki_card",
            (WikiPage(summary=WikiSummary(id="entry", name="Article")),),
            {"owner": OwnerIdentity("Owner", "game-first", "first")},
            "wiki",
            ("light", "dark"),
            type(None),
        ),
    ],
)
@pytest.mark.asyncio
async def test_numeric_templates_map_to_named_engine_styles(
    sdk, draws, method, args, options, family, variants, info_type
):
    async with Cards(skport=sdk) as cards:
        for template, variant in enumerate(variants, 1):
            if family == "wiki":
                with pytest.raises(CardNotImplementedError):
                    await getattr(cards, method)(*args, template=template, **options)
                assert draws == []
                continue
            result = await getattr(cards, method)(*args, template=template, **options)
            assert isinstance(result, RenderedCard) and isinstance(result.info, info_type)
            assert result.card.family == family and result.card.variant == result.card.template == template
            assert draws[-1][0] == family and draws[-1][2]["variant"] == variant


@pytest.mark.parametrize(
    "method,args,options",
    [
        ("profile_card", ("first",), {}),
        ("character_card", ("first",), {}),
        ("all_characters_card", ("owner-token",), {}),
        ("live_card", ("first",), {}),
        ("factory_card", ("first",), {}),
        ("exploration_card", ("first",), {}),
        ("monument_card", ("first",), {}),
        ("monument_detailed_card", ("first",), {}),
        ("contingency_contract_card", ("first",), {}),
        ("contingency_contract_detailed_card", ("first",), {}),
        ("compare_card", ("first", "second"), {}),
        ("pulls_card", (None,), {}),
        ("wiki_card", (None,), {"owner": OwnerIdentity("Owner", "game-first")}),
    ],
)
@pytest.mark.parametrize("template", [0, 5, True, False, "1", 1.0])
@pytest.mark.asyncio
async def test_invalid_templates_fail_before_sdk_or_rendering_io(sdk, draws, method, args, options, template):
    async with Cards(skport=sdk) as cards:
        with pytest.raises(UnsupportedVariantError):
            await getattr(cards, method)(*args, template=template, **options)
    assert draws == []
    assert all(value.await_count == 0 for value in vars(sdk.endfield).values())


@pytest.mark.asyncio
async def test_output_and_locale_are_configured_at_construction(sdk, draws):
    output = OutputConfig(format="WEBP", quality=82)
    async with Cards(skport=sdk, config=CardsConfig(locale="ja", output=output)) as cards:
        result = await cards.profile_card("first")
    assert result.card.format == "WEBP"
    assert draws[0][2]["output"] == output and draws[0][2]["context"].locale == "ja"
    assert sdk.endfield.card.await_args.kwargs["lang"] == "ja"
    for method in dir(Cards):
        if method.endswith("_card"):
            parameters = inspect.signature(getattr(Cards, method)).parameters
            assert "output" not in parameters and "locale" not in parameters and "lang" not in parameters
            assert not any(
                parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in parameters.values()
            )


@pytest.mark.asyncio
async def test_omitting_cards_config_inherits_sdk_locale(sdk, draws):
    sdk.config = ClientConfig(lang=Language.JA)
    async with Cards(sdk) as cards:
        await cards.profile_card("first")
    assert draws[0][2]["context"].locale == "ja"
    assert sdk.endfield.card.await_args.kwargs["lang"] == "ja"


@pytest.mark.asyncio
async def test_api_injection_closes_created_facade_and_borrows_api(sdk, draws, monkeypatch):
    api = SkportAPI(["test-account-token"])
    close_api = AsyncMock(wraps=api.close)
    monkeypatch.setattr(api, "close", close_api)
    monkeypatch.setattr(SkportClient, "endfield", property(lambda self: sdk.endfield))
    closed = []
    close_facade = SkportClient.close

    async def close(self):
        closed.append(self)
        await close_facade(self)

    monkeypatch.setattr(SkportClient, "close", close)
    try:
        async with Cards(api=api) as cards:
            assert (await cards.profile_card("first")).model.player.skport_id == "first"
        close_api.assert_not_awaited()
        assert len(closed) == 1
    finally:
        await api.close()


@pytest.mark.parametrize("template,variant", [(1, "dossier"), (2, "field")])
@pytest.mark.asyncio
async def test_compare_fetches_two_builds_and_returns_both_model_copies(sdk, monkeypatch, template, variant):
    calls = []

    async def compare(self, first, second, **options):
        calls.append((first, second, options))
        return [CardResult(b"compare-image", "PNG", 16, 16, "character", options["variant"])]

    monkeypatch.setattr(RenderEngine, "render_compare", compare)
    async with Cards(skport=sdk) as cards:
        result = await cards.compare_card("first", "second", name="Character", template=template)
    assert result.card.data == b"compare-image" and result.card.variant == result.card.template == template
    assert result.info is None
    assert [build.owner.skport_id for build in result.model] == ["first", "second"]
    assert calls[0][2]["variant"] == variant
    assert [call.kwargs["skport_id"] for call in sdk.endfield.character.await_args_list] == [
        "first",
        "second",
    ]
    copy = result.model
    copy[0].name = "Changed"
    assert result.model[0].name == "Character"


@pytest.mark.asyncio
async def test_full_roster_uses_explicit_owner_route_and_preserves_scope(sdk, draws, monkeypatch):
    monkeypatch.setenv("TOKEN", "ambient-credential-not-for-this-call")
    async with Cards(skport=sdk) as cards:
        result = await cards.all_characters_card("owner-token")
        assert result.info.source_scope == "owner"
        assert result.info.owner.skport_id == "owner"
        sdk.endfield.card.assert_not_awaited()
        sdk.endfield.owned_characters.assert_awaited_once()
        assert sdk.endfield.owned_characters.await_args.kwargs["token"] == "owner-token"
        with pytest.raises((TypeError, ValueError, DataValidationError, FetchError)):
            await cards.all_characters_card(None)
    assert sdk.endfield.owned_characters.await_count == 1


@pytest.mark.asyncio
async def test_sdk_failure_keeps_cause_and_closed_client_rejects_before_fetch(sdk, draws):
    failure = RuntimeError("offline")
    sdk.endfield.card.side_effect = failure
    cards = Cards(skport=sdk)
    with pytest.raises(FetchError) as caught:
        await cards.profile_card("first")
    assert caught.value.__cause__ is failure and draws == []
    await cards.aclose()
    await cards.aclose()
    with pytest.raises(ResourceClosedError):
        await cards.profile_card("second")
    assert sdk.endfield.card.await_count == 1
    sdk.close.assert_not_awaited()


@pytest.mark.asyncio
async def test_call_cancellation_reaches_sdk_and_leaves_borrowed_client_usable(sdk, draws):
    entered, cancelled = asyncio.Event(), asyncio.Event()

    async def pending(**ids):
        entered.set()
        try:
            await asyncio.Future()
        finally:
            cancelled.set()

    sdk.endfield.card.side_effect = pending
    async with Cards(skport=sdk) as cards:
        request = asyncio.create_task(cards.profile_card("first"))
        await asyncio.wait_for(entered.wait(), 1)
        request.cancel()
        with pytest.raises(asyncio.CancelledError):
            await request
        assert cancelled.is_set() and draws == []
        sdk.endfield.card.side_effect = None
        sdk.endfield.card.return_value = profile("second")
        assert (await cards.profile_card("second")).model.player.skport_id == "second"
    sdk.close.assert_not_awaited()


@pytest.mark.asyncio
async def test_closing_public_client_cancels_pending_fetch_and_closes_engine(sdk, draws, monkeypatch):
    entered, cancelled = asyncio.Event(), asyncio.Event()
    closed = []
    close_engine = RenderEngine.aclose

    async def pending(**ids):
        entered.set()
        try:
            await asyncio.Future()
        finally:
            cancelled.set()

    async def close(self):
        closed.append(self)
        await close_engine(self)

    monkeypatch.setattr(RenderEngine, "aclose", close)
    sdk.endfield.card.side_effect = pending
    cards = Cards(skport=sdk)
    request = asyncio.create_task(cards.profile_card("first"))
    await asyncio.wait_for(entered.wait(), 1)
    await asyncio.wait_for(cards.aclose(), 1)
    with pytest.raises(asyncio.CancelledError):
        await request
    assert cancelled.is_set() and draws == [] and len(closed) == 1
    sdk.close.assert_not_awaited()
