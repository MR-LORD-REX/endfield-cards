"""SDK-backed card requests; drawing and resource management live in RenderEngine."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine, Sequence
from copy import deepcopy
from dataclasses import replace
from functools import wraps
from pathlib import Path
from types import MappingProxyType
from typing import Any, Concatenate, Literal, ParamSpec, TypeVar, cast

from aiohttp import ClientSession
from PIL import Image
from skport import Role, SkportAPI, SkportClient
from skport.games.endfield.models import (
    CharacterBuild,
    ContractState,
    FactoryState,
    LiveStatus,
    MonumentState,
    PlayerCard,
    PullHistory,
    WikiPage,
)

from endfield_cards.adapters.skport import context_for, validate_owner
from endfield_cards.assets.download import URLPolicy
from endfield_cards.assets.store import AssetStore
from endfield_cards.config import CardsConfig, Locale
from endfield_cards.errors import (
    DataValidationError,
    FetchError,
    ResourceClosedError,
    UnsupportedVariantError,
)
from endfield_cards.models import (
    Artwork,
    CharacterListInfo,
    ContractInfo,
    LiveInfo,
    MonumentInfo,
    OwnerIdentity,
    RenderContext,
    RenderedCard,
)
from endfield_cards.rendering.engine import RenderEngine
from endfield_cards.rendering.registry import ensure_implemented
from endfield_cards.utils.selection import render_info

# Public template numbers stay stable when the internal named registry changes.
_STYLES = {
    "profile": ("overview", "operations", "identity"),
    "character": ("dossier", "terminal", "field", "portrait"),
    "compare": ("dossier", "field"),
    **dict.fromkeys(
        (
            "all_characters",
            "live",
            "factory",
            "exploration",
            "monument",
            "monument_detailed",
            "contingency_contract",
            "contingency_contract_detailed",
            "pulls",
            "wiki",
        ),
        ("light", "dark"),
    ),
}
TEMPLATES = MappingProxyType({name: tuple(range(1, len(styles) + 1)) for name, styles in _STYLES.items()})

Art = Artwork | str | Path | bytes | Image.Image
P = ParamSpec("P")
T = TypeVar("T")


def _request(
    method: Callable[Concatenate[Cards, P], Coroutine[Any, Any, T]],
) -> Callable[Concatenate[Cards, P], Coroutine[Any, Any, T]]:
    """Track the whole fetch/render request so closing cancels either phase."""

    @wraps(method)
    async def run(self: Cards, *args: P.args, **kwargs: P.kwargs) -> T:
        self._check_open()
        task = asyncio.current_task()
        if task is not None:
            self._active.add(task)
        try:
            return await method(self, *args, **kwargs)
        finally:
            if task is not None:
                self._active.discard(task)

    return run


def _style(family: str, template: int) -> str:
    if type(template) is not int or template not in TEMPLATES[family]:
        raise UnsupportedVariantError(f"{family} template must be one of {TEMPLATES[family]}")
    variant = _STYLES[family][template - 1]
    ensure_implemented("character" if family == "compare" else family, variant)
    return variant


def _selector(char_id: str | None, name: str | None, index: int | None) -> dict[str, Any]:
    if sum(value is not None for value in (char_id, name, index)) > 1:
        raise DataValidationError("Supply one of char_id, name or index")
    if char_id is not None:
        if not isinstance(char_id, str) or not char_id.strip():
            raise DataValidationError("char_id must be a nonempty string")
        return {"char_id": char_id}
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise DataValidationError("name must be a nonempty string")
        return {"name": name}
    if index is not None and (type(index) is not int or index < 0):
        raise DataValidationError("index must be a nonnegative integer")
    return {"index": 0 if index is None else index}


class Cards:
    """Fetch and create cards for any target using one injected SKPort SDK or API.

    Set locale, output and resource budgets once with CardsConfig. Injected SDK,
    API, AssetStore and session resources are borrowed. Use one client per loop.
    """

    def __init__(
        self,
        skport: SkportClient | None = None,
        *,
        api: SkportAPI | None = None,
        config: CardsConfig | None = None,
        asset_store: AssetStore | None = None,
        session: ClientSession | None = None,
        url_policy: URLPolicy | None = None,
    ) -> None:
        if (skport is None) == (api is None):
            raise ValueError("Supply exactly one of skport or api")
        if asset_store is not None and (session is not None or url_policy is not None):
            raise ValueError("session and url_policy belong to the supplied AssetStore")
        self.skport = skport if skport is not None else SkportClient(api=api)
        self._owns_sdk = skport is None
        self.config = config or CardsConfig(locale=cast(Locale, self.skport.config.lang.value))
        self._engine = RenderEngine(
            config=self.config, asset_store=asset_store, session=session, url_policy=url_policy
        )
        self._closed = False
        self._active: set[asyncio.Task[Any]] = set()
        self._close_task: asyncio.Task[None] | None = None

    @property
    def templates(self) -> dict[str, tuple[int, ...]]:
        """Available numeric templates for each card method (without the _card suffix)."""
        return dict(TEMPLATES)

    @property
    def variants(self) -> dict[str, tuple[int, ...]]:
        return self.templates

    @property
    def cache_stats(self) -> dict[str, Any]:
        return self._engine.cache_stats

    def _check_open(self) -> None:
        if self._closed:
            raise ResourceClosedError("Cards is closed")

    async def __aenter__(self) -> Cards:
        self._check_open()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._close_task is None:
            self._closed = True
            self._close_task = asyncio.create_task(self._close_resources())
        await asyncio.shield(self._close_task)

    close = aclose

    async def _close_resources(self) -> None:
        active = list(self._active)
        for task in active:
            task.cancel()
        if active:
            await asyncio.gather(*active, return_exceptions=True)
        try:
            await self._engine.aclose()
        finally:
            if self._owns_sdk:
                await self.skport.close()

    async def clear_cache(self, *, renders: bool = True, images: bool = True, disk: bool = True) -> None:
        self._check_open()
        await self._engine.clear_cache(renders=renders, images=images, disk=disk)

    def _target(
        self,
        skport_id: str | int | None,
        role_id: str | int | None,
        server_id: str | int | None,
        *,
        token: str | None = None,
        role: Role | str | None = None,
    ) -> dict[str, Any]:
        if (skport_id is None) == (token is None):
            raise DataValidationError("Supply exactly one of skport_id or token")
        if token is not None:
            if not isinstance(token, str) or not token.strip():
                raise DataValidationError("token must be a nonempty string")
            if role_id is not None or server_id is not None:
                raise DataValidationError("Owner requests select a role with role")
            return {"token": token, "role": role}
        if type(skport_id) not in (str, int) or not str(skport_id).strip():
            raise DataValidationError("skport_id must be a nonempty string or integer")
        if role is not None:
            raise DataValidationError("Public requests select a role with role_id and server_id")
        return {"skport_id": skport_id, "role_id": role_id, "server_id": server_id}

    async def _fetch(self, method: str, **ids: Any) -> Any:
        self._check_open()
        try:
            return await getattr(self.skport.endfield, method)(lang=self.config.locale, **ids)
        except Exception as exc:
            raise FetchError(f"SKPort could not fetch {method}") from exc

    def _context(
        self, model: Any, *, owner: Any = None, scope: str | None = None, live: bool = False
    ) -> RenderContext:
        context = context_for(model, owner, locale=self.config.locale, source_scope=scope)
        return replace(context, display_timezone="UTC" if live else self.config.display_timezone)

    async def _create(
        self,
        family: str,
        model: T,
        variant: str,
        template: int,
        *,
        owner: Any = None,
        scope: str | None = None,
        art: Art | None = None,
        **options: Any,
    ) -> RenderedCard[T, Any]:
        self._check_open()
        snapshot, options = deepcopy(model), deepcopy(options)
        context = self._context(snapshot, owner=owner, scope=scope, live=family == "activity")
        if (profile := options.get("profile")) is not None:
            validate_owner(profile, context)
        pages = await self._engine.render(
            family, snapshot, context=context, variant=variant, art=art, output=self.config.output, **options
        )
        return RenderedCard(
            [replace(page, variant=template) for page in pages],
            snapshot,
            render_info(family, snapshot, context, **options),
        )

    @_request
    async def profile_card(
        self,
        skport_id: str | int | None = None,
        *,
        template: Literal[1, 2, 3] = 1,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
        token: str | None = None,
        role: Role | str | None = None,
        details: bool = False,
    ) -> RenderedCard[PlayerCard, CharacterListInfo]:
        """Create a profile and return its exposed character selectors."""
        variant = _style("profile", template)
        ids = self._target(skport_id, role_id, server_id, token=token, role=role)
        model = await self._fetch("owned_card" if token is not None else "card", **ids)
        return await self._create("profile", model, variant, template, details=details)

    @_request
    async def character_card(
        self,
        skport_id: str | int | None = None,
        *,
        template: Literal[1, 2, 3, 4] = 1,
        char_id: str | None = None,
        name: str | None = None,
        index: int | None = None,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
        token: str | None = None,
        role: Role | str | None = None,
        full: bool = True,
        showcase_only: bool = False,
        art: Art | None = None,
        details: bool = False,
    ) -> RenderedCard[CharacterBuild, None]:
        """Create one operator card; choose by ID, name or index (default 0)."""
        variant = _style("character", template)
        ids = self._target(skport_id, role_id, server_id, token=token, role=role)
        selectors = _selector(char_id, name, index)
        if token is None:
            selectors["showcase_only"] = showcase_only
        elif showcase_only:
            raise DataValidationError("showcase_only is a public character selector")
        model = await self._fetch(
            "owned_character" if token is not None else "character", full=full, **ids, **selectors
        )
        return await self._create(
            "character",
            model,
            variant,
            template,
            art=art,
            details=details,
            scope="owner" if token is not None else "public",
        )

    @_request
    async def all_characters_card(
        self,
        token: str,
        *,
        template: Literal[1, 2] = 1,
        role: Role | str | None = None,
        full: bool = True,
        character_ids: Sequence[str] | None = None,
        details: bool = False,
    ) -> RenderedCard[list[CharacterBuild], CharacterListInfo]:
        """Create the explicit token owner's roster, optionally selecting operator IDs."""
        variant = _style("all_characters", template)
        if isinstance(character_ids, (str, bytes)):
            raise DataValidationError("character_ids must be a sequence of IDs, not a string")
        ids = self._target(None, None, None, token=token, role=role)
        model = await self._fetch("owned_characters", full=full, **ids)
        owner = model[0].owner if model else await self._fetch("owned_card", **ids)
        return await self._create(
            "roster",
            model,
            variant,
            template,
            owner=owner,
            scope="owner",
            character_ids=tuple(character_ids) if character_ids is not None else None,
            details=details,
        )

    @_request
    async def live_card(
        self,
        skport_id: str | int | None = None,
        *,
        template: Literal[1, 2] = 1,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
        token: str | None = None,
        role: Role | str | None = None,
        details: bool = False,
    ) -> RenderedCard[LiveStatus, LiveInfo]:
        """Create the resource/activity dashboard with source deadlines in UTC."""
        variant = _style("live", template)
        ids = self._target(skport_id, role_id, server_id, token=token, role=role)
        model = await self._fetch("owned_activity" if token is not None else "activity", **ids)
        profile = await self._fetch("owned_card" if token is not None else "card", **ids)
        return await self._create(
            "activity",
            model,
            variant,
            template,
            scope="owner" if token is not None else "public",
            profile=profile,
            details=details,
        )

    @_request
    async def factory_card(
        self,
        skport_id: str | int,
        *,
        template: Literal[1, 2] = 1,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
    ) -> RenderedCard[FactoryState, None]:
        """Create a factory/Dijiang card with regional funds, settlements and cabin crew."""
        variant = _style("factory", template)
        ids = self._target(skport_id, role_id, server_id)
        model = await self._fetch("factory", **ids)
        profile = await self._fetch("card", **ids)
        return await self._create("factory", model, variant, template, profile=profile)

    @_request
    async def exploration_card(
        self,
        skport_id: str | int,
        *,
        template: Literal[1, 2] = 1,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
    ) -> RenderedCard[FactoryState, None]:
        """Create an exploration card covering all supplied regions, areas and counters."""
        variant = _style("exploration", template)
        ids = self._target(skport_id, role_id, server_id)
        model = await self._fetch("factory", **ids)
        profile = await self._fetch("card", **ids)
        return await self._create("exploration", model, variant, template, profile=profile)

    @_request
    async def monument_card(
        self,
        skport_id: str | int,
        *,
        template: Literal[1, 2] = 1,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
        event_id: str | None = None,
        details: bool = False,
    ) -> RenderedCard[MonumentState, MonumentInfo]:
        """Create a Monument overview and return event/stage selectors."""
        variant = _style("monument", template)
        ids = self._target(skport_id, role_id, server_id)
        model = await self._fetch("monument", **ids)
        profile = await self._fetch("card", **ids)
        return await self._create(
            "monument", model, variant, template, profile=profile, event_id=event_id, details=details
        )

    @_request
    async def monument_detailed_card(
        self,
        skport_id: str | int,
        *,
        template: Literal[1, 2] = 1,
        event_id: str | None = None,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
    ) -> RenderedCard[MonumentState, MonumentInfo]:
        """Create a stage board for the selected event, defaulting to the active event."""
        variant = _style("monument_detailed", template)
        ids = self._target(skport_id, role_id, server_id)
        model = await self._fetch("monument", **ids)
        profile = await self._fetch("card", **ids)
        return await self._create(
            "monument_detail", model, variant, template, event_id=event_id, profile=profile
        )

    @_request
    async def contingency_contract_card(
        self,
        skport_id: str | int,
        *,
        template: Literal[1, 2] = 1,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
        contract_id: str | None = None,
        details: bool = False,
    ) -> RenderedCard[ContractState, ContractInfo]:
        """Create a Contract overview and return contract/run selectors."""
        variant = _style("contingency_contract", template)
        ids = self._target(skport_id, role_id, server_id)
        model = await self._fetch("contract", **ids)
        profile = await self._fetch("card", **ids)
        return await self._create(
            "contingency_contract",
            model,
            variant,
            template,
            profile=profile,
            contract_id=contract_id,
            details=details,
        )

    @_request
    async def contingency_contract_detailed_card(
        self,
        skport_id: str | int,
        *,
        template: Literal[1, 2] = 1,
        contract_id: str | None = None,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
    ) -> RenderedCard[ContractState, ContractInfo]:
        """Create the selected/current Contract's battle and indicator board."""
        variant = _style("contingency_contract_detailed", template)
        ids = self._target(skport_id, role_id, server_id)
        model = await self._fetch("contract", **ids)
        profile = await self._fetch("card", **ids)
        return await self._create(
            "contingency_contract_detail", model, variant, template, contract_id=contract_id, profile=profile
        )

    @_request
    async def compare_card(
        self,
        first_skport_id: str | int,
        second_skport_id: str | int,
        *,
        template: Literal[1, 2] = 1,
        char_id: str | None = None,
        name: str | None = None,
        index: int | None = None,
        second_char_id: str | None = None,
        role_id: str | int | None = None,
        server_id: str | int | None = None,
        second_role_id: str | int | None = None,
        second_server_id: str | int | None = None,
        art: Art | None = None,
        second_art: Art | None = None,
        details: bool = False,
    ) -> RenderedCard[tuple[CharacterBuild, CharacterBuild], None]:
        """Compare one operator from two players; opaque IDs may differ per account."""
        variant = _style("compare", template)
        first_ids = self._target(first_skport_id, role_id, server_id)
        second_ids = self._target(second_skport_id, second_role_id, second_server_id)
        selector = _selector(char_id, name, index)
        second_selector = _selector(second_char_id, None, None) if second_char_id is not None else None
        first = await self._fetch("character", full=True, **first_ids, **selector)
        # Resolve by name instead of reusing an account-specific character ID or index.
        second = await self._fetch(
            "character", full=True, **second_ids, **(second_selector or _selector(None, first.name, None))
        )
        first, second = deepcopy(first), deepcopy(second)
        context, second_context = self._context(first), self._context(second)
        pages = await self._engine.render_compare(
            first,
            second,
            context=context,
            second_context=second_context,
            variant=variant,
            art=art,
            second_art=second_art,
            output=self.config.output,
            details=details,
        )
        return RenderedCard([replace(page, variant=template) for page in pages], (first, second), None)

    @_request
    async def pulls_card(
        self,
        data: PullHistory,
        *,
        template: Literal[1, 2] = 1,
        owner: OwnerIdentity | None = None,
    ) -> RenderedCard[PullHistory, None]:
        """Create a supplied pull-history card; SKPort has no normalized fetch route yet."""
        variant = _style("pulls", template)
        return await self._create("pulls", data, variant, template, owner=owner, scope="supplied")

    @_request
    async def wiki_card(
        self,
        data: WikiPage,
        *,
        owner: OwnerIdentity,
        template: Literal[1, 2] = 1,
    ) -> RenderedCard[WikiPage, None]:
        """Create a supplied wiki-page card with its explicit display owner."""
        variant = _style("wiki", template)
        return await self._create("wiki", data, variant, template, owner=owner, scope="supplied")


EFCard = Cards
