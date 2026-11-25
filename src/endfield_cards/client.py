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
    CardNotImplementedError,
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
    method: Callable[Concatenate[EF_Cards, P], Coroutine[Any, Any, T]],
) -> Callable[Concatenate[EF_Cards, P], Coroutine[Any, Any, T]]:
    """Track the whole fetch/render request so closing cancels either phase."""

    @wraps(method)
    async def run(self: EF_Cards, *args: P.args, **kwargs: P.kwargs) -> T:
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


class EF_Cards:
    """Fetch Endfield data through SKPort and create cards with numeric templates.

    Configure language, image format and rendering budgets once at construction.
    Each ``*_card()`` method accepts a target and returns a ``RenderedCard`` with
    encoded images, a copy of the SDK model and optional navigation metadata.
    Use ``async with EF_Cards(...)`` to release resources when finished.

    SKPort manages tokens, player IDs, account visibility and game calculations.
    See https://mr-lord-rex.github.io/skport-py/ for authentication and data setup.
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
        """Create a card client using exactly one of ``skport`` or ``api``.

        Args:
            skport: Existing ``SkportClient`` to use for data requests.
            api: Existing ``SkportAPI``; the client creates its own SDK wrapper.
            config: Card language, output format, timezone and resource budgets.
                Defaults to ``CardsConfig`` with the SDK's language.
            asset_store: Optional shared image store. Its lifetime stays with you.
            session: Optional shared HTTP session when no asset store is supplied.
            url_policy: Optional allowed image URL policy for the created store.

        Raises:
            ValueError: Both or neither data clients were supplied, or shared
                image resources conflict. Injected SDKs, APIs and sessions stay
                open when this client closes.
        """
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
        """Return template numbers keyed by method name without ``_card``.

        Pulls and wiki numbers are reserved; those methods are not implemented.
        """
        return dict(TEMPLATES)

    @property
    def variants(self) -> dict[str, tuple[int, ...]]:
        """Return ``templates``; retained as a compatibility alias."""
        return self.templates

    @property
    def cache_stats(self) -> dict[str, Any]:
        """Return current render, image and optional disk cache statistics."""
        return self._engine.cache_stats

    def _check_open(self) -> None:
        if self._closed:
            raise ResourceClosedError("EF_Cards is closed")

    async def __aenter__(self) -> EF_Cards:
        """Return this client for an ``async with`` block."""
        self._check_open()
        return self

    async def __aexit__(self, *exc: object) -> None:
        """Close this client's resources when its context ends."""
        await self.aclose()

    async def aclose(self) -> None:
        """Cancel pending requests and release owned render resources.

        Safe to call more than once. Injected SDKs, APIs and image resources are
        borrowed and remain open. ``close()`` is an alias of this async method.
        """
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
        """Clear selected caches without closing the client.

        Args:
            renders: Remove cached encoded cards.
            images: Remove cached decoded source images.
            disk: Remove this client's optional image disk cache.

        Returns:
            None after the selected caches have been cleared.
        """
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
        """Fetch a player profile and create an overview of their operators.

        Args:
            skport_id: Public SKPORT ID; omit when using ``token``.
            template: Profile layout number, 1 through 3.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.
            token: Owner account token, supplied instead of ``skport_id``.
            role: Owner role selector from SKPort, used only with ``token``.
            details: Append supplementary pages when True.

        Returns:
            ``RenderedCard`` containing encoded pages, the fetched ``PlayerCard``
            in ``model``, and ``CharacterListInfo`` in ``info``. Character IDs in
            ``info.characters`` can select a subsequent character card. Public
            profiles show exposed operators, not the complete owned collection.
        """
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
        """Fetch one operator build and create a card of its stats and loadout.

        Args:
            skport_id: Public SKPORT ID; omit when using ``token``.
            template: Character layout number, 1 through 4.
            char_id: Opaque operator ID returned by the SDK or profile ``info``.
            name: Localized operator name, used instead of ``char_id`` or ``index``.
            index: Zero-based SDK operator index. Defaults to 0 when no selector
                is supplied; provide only one of ``char_id``, ``name`` or ``index``.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.
            token: Owner token, supplied instead of ``skport_id``.
            role: Owner role selector used only with ``token``.
            full: Fetch the operator's full detail data when True.
            showcase_only: Select from public showcase operators only.
            art: Optional ``Artwork``, path, image bytes or Pillow image.
            details: Append supplementary build pages when True.

        Returns:
            ``RenderedCard`` with encoded images and a copy of ``CharacterBuild``
            in ``model``. ``info`` is None. Weapon capsules show confirmed base
            levels in white and essence bonuses in yellow.
        """
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
        """Fetch an authenticated owner's operators and create a roster board.

        Args:
            token: Owner account token; this method requires owner access.
            template: Roster layout number, 1 or 2.
            role: Optional SDK owner role selector.
            full: Fetch full operator details when True.
            character_ids: Optional sequence of opaque IDs to include on the board.
            details: Append supplementary build pages when True.

        Returns:
            ``RenderedCard`` with roster images, the fetched list of
            ``CharacterBuild`` models, and ``CharacterListInfo`` selectors in
            ``info``. Large rosters can return multiple images in ``cards``.
            Filtering the board does not discard the fetched source models.
        """
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
        """Fetch current resources and activities and create a status dashboard.

        Args:
            skport_id: Public SKPORT ID; omit when using ``token``.
            template: Dashboard layout number, 1 or 2.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.
            token: Owner token, supplied instead of ``skport_id``.
            role: Owner role selector used only with ``token``.
            details: Append supplementary activity pages when True.

        Returns:
            ``RenderedCard`` with dashboard images, ``LiveStatus`` in ``model``
            and resource meters, deadlines and activity selectors in ``LiveInfo``.
            Live timestamps are displayed in UTC, including recovery deadlines.
        """
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
        """Fetch factory data and create a factory and Dijiang status card.

        Args:
            skport_id: Public SKPORT ID of the player.
            template: Factory layout number, 1 or 2.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.

        Returns:
            ``RenderedCard`` showing regional funds, settlements, Dijiang cabins
            and crew. ``model`` contains the complete SDK ``FactoryState`` and
            ``info`` is None. Use ``exploration_card`` for exploration progress.
        """
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
        """Fetch world progress and create an exploration card for every area.

        Args:
            skport_id: Public SKPORT ID of the player.
            template: Exploration layout number, 1 or 2.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.

        Returns:
            ``RenderedCard`` covering supplied regions, areas and exploration
            counters. ``model`` is the complete SDK ``FactoryState``; ``info``
            is None. Factory and Dijiang status belong to ``factory_card``.
        """
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
        """Fetch Monument records and create an overview of events and clears.

        Args:
            skport_id: Public SKPORT ID of the player.
            template: Monument overview layout number, 1 or 2.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.
            event_id: Optional event ID from ``info.events`` to limit the overview.
            details: Append supplementary record pages when True.

        Returns:
            ``RenderedCard`` with overview images, the complete ``MonumentState``
            in ``model`` and event/stage selectors in ``MonumentInfo``. Use an
            event's ID with ``monument_detailed_card`` to inspect its stages.
        """
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
        """Create a detailed Monument board with stage clears, times and teams.

        Args:
            skport_id: Public SKPORT ID of the player.
            template: Detailed Monument layout number, 1 or 2.
            event_id: Event ID from ``MonumentInfo.events``. When omitted, selects
                an active event, otherwise the latest supplied event.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.

        Returns:
            ``RenderedCard`` with the selected event's stage images, the complete
            ``MonumentState`` in ``model`` and ``MonumentInfo`` in ``info``.
        """
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
        """Fetch Contingency Contract data and create a score/activity overview.

        Args:
            skport_id: Public SKPORT ID of the player.
            template: Contract overview layout number, 1 or 2.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.
            contract_id: Optional contract ID from ``info.contracts``. Defaults
                to the current contract, otherwise the first supplied contract.
            details: Append supplementary contract record pages when True.

        Returns:
            ``RenderedCard`` with overview images, the complete ``ContractState``
            in ``model`` and contracts, missions and run selectors in ``ContractInfo``.
        """
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
        """Create a detailed Contingency Contract board with battles and indicators.

        Args:
            skport_id: Public SKPORT ID of the player.
            template: Detailed Contract layout number, 1 or 2.
            contract_id: Contract ID from ``ContractInfo.contracts``. Defaults
                to the current contract, otherwise the first supplied contract.
            role_id: Optional public game account role ID.
            server_id: Optional public server ID, paired with ``role_id``.

        Returns:
            ``RenderedCard`` with the selected contract's battle images, the
            complete ``ContractState`` in ``model`` and ``ContractInfo`` in ``info``.
        """
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
        """Fetch one operator from two public profiles and compare their builds.

        Args:
            first_skport_id: Public SKPORT ID for the first build.
            second_skport_id: Public SKPORT ID for the second build.
            template: Comparison layout number, 1 or 2.
            char_id: Opaque operator ID on the first profile.
            name: Localized operator name instead of ``char_id`` or ``index``.
            index: Zero-based first-profile operator index; defaults to 0. Supply
                only one of ``char_id``, ``name`` or ``index``.
            second_char_id: Optional second-profile operator ID. When omitted,
                the second operator is selected by the first operator's name.
            role_id: Optional first-profile public game account role ID.
            server_id: Optional first-profile public server ID.
            second_role_id: Optional second-profile public role ID.
            second_server_id: Optional second-profile public server ID.
            art: Optional artwork override for the first build.
            second_art: Optional artwork override for the second build.
            details: Append supplementary build pages when True.

        Returns:
            ``RenderedCard`` with comparison images and a ``(first, second)``
            tuple of full ``CharacterBuild`` models. ``info`` is None. Opaque
            operator IDs are account-specific and are not reused across players.
        """
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
        data: PullHistory | None = None,
        *,
        template: Literal[1, 2] = 1,
        owner: OwnerIdentity | None = None,
    ) -> RenderedCard[PullHistory, None]:
        """Reserved for pull-history cards; currently raises before rendering.

        Args:
            data: SDK ``PullHistory`` reserved for a future implementation.
            template: Reserved template number, 1 or 2.
            owner: Optional display owner reserved for supplied data.

        Raises:
            CardNotImplementedError: Pulls cards are not implemented. No SDK
                requests, image downloads or rendering are started.
        """
        _style("pulls", template)
        raise CardNotImplementedError(f"pulls_card(template={template}) is not implemented yet")

    @_request
    async def wiki_card(
        self,
        data: WikiPage | None = None,
        *,
        owner: OwnerIdentity | None = None,
        template: Literal[1, 2] = 1,
    ) -> RenderedCard[WikiPage, None]:
        """Reserved for wiki cards; currently raises before rendering.

        Args:
            data: SDK ``WikiPage`` reserved for a future implementation.
            owner: Explicit display owner reserved for supplied wiki data.
            template: Reserved template number, 1 or 2.

        Raises:
            CardNotImplementedError: Wiki cards are not implemented. No SDK
                requests, image downloads or rendering are started.
        """
        _style("wiki", template)
        raise CardNotImplementedError(f"wiki_card(template={template}) is not implemented yet")


# Older imports continue to work; EF_Cards is the primary public client.
Cards = EF_Cards
EFCard = EF_Cards
