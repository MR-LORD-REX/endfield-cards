"""Advanced model rendering with bounded resources and optional SDK fetching."""

from __future__ import annotations

import asyncio
import hashlib
from collections.abc import AsyncGenerator, AsyncIterator, Iterable
from dataclasses import replace
from typing import Any, cast

from skport import SkportClient

from endfield_cards._version import __version__
from endfield_cards.adapters.skport import context_for, validate_owner
from endfield_cards.assets.store import AssetStore
from endfield_cards.cache import ByteLRU, cache_key
from endfield_cards.config import CardsConfig, OutputConfig
from endfield_cards.errors import CardError, FetchError, RenderError, ResourceClosedError
from endfield_cards.models import (
    Artwork,
    BatchItem,
    CardResult,
    RenderContext,
    RenderIssue,
    RenderRequest,
)
from endfield_cards.models.rendered import (
    CharacterListInfo,
    ContractInfo,
    LiveInfo,
    MonumentInfo,
    RenderedCard,
    RenderInfo,
)
from endfield_cards.rendering.encoding import encode
from endfield_cards.rendering.executor import RenderExecutor
from endfield_cards.rendering.pipeline import LazyAssets
from endfield_cards.rendering.registry import VARIANTS, pick


def _snapshot(model: Any) -> Any:
    if hasattr(model, "model_copy"):
        return model.model_copy(deep=True)
    if isinstance(model, (list, tuple)):
        return [_snapshot(item) for item in model]
    import copy

    return copy.deepcopy(model)


def _next_page(iterator: Any, output: OutputConfig) -> tuple[bytes, int, int] | None:
    try:
        image = next(iterator)
    except StopIteration:
        return None
    try:
        return encode(image, output), image.width, image.height
    finally:
        image.close()


def _source_issues(model: Any) -> list[RenderIssue]:
    """Retain SDK issues for returned collections as well as their containers."""
    result: list[RenderIssue] = []
    for item in model if isinstance(model, (list, tuple)) else [model]:
        result.extend(RenderIssue(issue.code, str(issue.message)) for issue in getattr(item, "issues", []))
        result.extend(_source_issues(getattr(item, "characters", ())))
    return result


def _validated_options(family: str, context: RenderContext, options: dict[str, Any]) -> dict[str, Any]:
    if (
        family
        in {
            "factory",
            "exploration",
            "activity",
            "monument",
            "monument_detail",
            "contingency_contract",
            "contingency_contract_detail",
        }
        and options.get("profile") is not None
    ):
        options = dict(options)
        options["profile"] = _snapshot(options["profile"])
        validate_owner(options["profile"], context)
    return options


class RenderEngine:
    """Render supplied models for arbitrary owners with reusable bounded resources.

    SDK and AssetStore injections are borrowed. A passed aiohttp session is
    borrowed by the internally owned store. Use one client per event loop.
    """

    def __init__(
        self,
        *,
        config: CardsConfig | None = None,
        skport: SkportClient | None = None,
        asset_store: AssetStore | None = None,
        session: Any = None,
        url_policy: Any = None,
    ) -> None:
        self.config = config or CardsConfig()
        if asset_store is not None and (session is not None or url_policy is not None):
            raise ValueError("session and url_policy belong to the supplied AssetStore")
        self.skport = skport
        self.assets = asset_store or AssetStore(
            self.config.cache, self.config.download, session=session, url_policy=url_policy
        )
        self._owns_assets = asset_store is None
        self._executor = RenderExecutor(self.config.render_workers)
        self._admission = asyncio.Semaphore(self.config.admitted_jobs)
        self._renders: ByteLRU[tuple[CardResult, ...]] = ByteLRU(
            self.config.cache.encoded_bytes if self.config.cache.enabled else 0,
            ttl_seconds=self.config.cache.ttl_seconds,
        )
        self._flights: dict[str, asyncio.Task[list[CardResult]]] = {}
        self._closed = False
        self._generation = 0
        self._active: set[asyncio.Task[Any]] = set()
        self._close_task: asyncio.Task[None] | None = None
        self._resource_revision: str | None = None

    @property
    def variants(self) -> dict[str, tuple[str, ...]]:
        return dict(VARIANTS)

    @property
    def cache_stats(self) -> dict[str, Any]:
        return {
            "renders": self._renders.stats,
            "assets": self.assets.stats,
            "active": len(self._active),
            "in_flight": len(self._flights),
        }

    def _check_open(self) -> None:
        if self._closed:
            raise ResourceClosedError("RenderEngine is closed")

    async def __aenter__(self) -> RenderEngine:
        self._check_open()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._close_task is None:
            self._closed = True
            self._generation += 1
            self._close_task = asyncio.create_task(self._close_resources())
        await asyncio.shield(self._close_task)

    close = aclose

    async def _close_resources(self) -> None:
        active = list(self._active | set(self._flights.values()))
        for task in active:
            task.cancel()
        if active:
            await asyncio.gather(*active, return_exceptions=True)
        await self._executor.aclose()
        if self._owns_assets:
            await self.assets.aclose()
        self._renders.clear()

    async def clear_cache(self, *, renders: bool = True, images: bool = True, disk: bool = True) -> None:
        self._check_open()
        self._generation += 1
        if renders:
            self._renders.clear()
        if images or disk:
            await self.assets.clear_cache(memory=images, disk=disk)

    async def render(
        self,
        family: str,
        model: Any,
        *,
        context: RenderContext | None = None,
        owner: Any = None,
        variant: str | None = None,
        art: Artwork | Any = None,
        output: OutputConfig | None = None,
        **options: Any,
    ) -> list[CardResult]:
        """Return separately encoded pages; identity validation precedes asset I/O."""
        self._check_open()
        family, variant, _ = pick(family, variant)
        snapshot = _snapshot(model)
        context = context or context_for(snapshot, owner, locale=self.config.locale)
        validate_owner(snapshot, context)
        options = _validated_options(family, context, options)
        artwork = art if isinstance(art, Artwork) else Artwork(art) if art is not None else None
        output = output or OutputConfig()
        cacheable = self.config.cache.enabled and artwork is None
        if self._resource_revision is None:

            def resource_revision() -> str:
                from importlib.resources import files

                return hashlib.sha256(
                    files("endfield_cards").joinpath("assets/resources/manifest.json").read_bytes()
                ).hexdigest()

            self._resource_revision = await asyncio.to_thread(resource_revision)
        key = cache_key(
            __version__, self._resource_revision, family, variant, snapshot, context, output, options
        )
        if cacheable:
            cached = self._renders.get(key)
            if cached is not None:
                return list(cached)
            flight_key = f"{self._generation}:{key}"
            task = self._flights.get(flight_key)
            if task is None:
                generation = self._generation
                task = asyncio.create_task(
                    self._collect(family, snapshot, context, variant, artwork, output, options)
                )
                self._flights[flight_key] = task
                task.add_done_callback(
                    lambda completed: self._finish_render(flight_key, key, generation, completed)
                )
            return list(await asyncio.shield(task))
        return await self._collect(family, snapshot, context, variant, artwork, output, options)

    def _finish_render(
        self, flight_key: str, key: str, generation: int, task: asyncio.Task[list[CardResult]]
    ) -> None:
        self._flights.pop(flight_key, None)
        if task.cancelled():
            return
        exception = task.exception()
        if exception is None and not self._closed and generation == self._generation:
            results = task.result()
            if not any(result.issues for result in results):
                self._renders.put(key, tuple(results), size_bytes=sum(len(result.data) for result in results))

    async def _collect(
        self,
        family: str,
        model: Any,
        context: RenderContext,
        variant: str,
        artwork: Artwork | None,
        output: OutputConfig,
        options: dict[str, Any],
    ) -> list[CardResult]:
        pages = [
            page async for page in self._iterate(family, model, context, variant, artwork, output, options)
        ]
        issues = tuple(dict.fromkeys(issue for page in pages for issue in page.issues))
        return [replace(page, pages=len(pages), issues=issues) for page in pages]

    async def iter_pages(
        self,
        family: str,
        model: Any,
        *,
        context: RenderContext | None = None,
        owner: Any = None,
        variant: str | None = None,
        art: Any = None,
        output: OutputConfig | None = None,
        **options: Any,
    ) -> AsyncIterator[CardResult]:
        """Yield encoded pages; heavy families draw each page as it is requested.

        Streaming results use pages=0 (unknown until exhaustion). The embedded
        footer uses the template's planned total. Close an abandoned iterator.
        """
        self._check_open()
        family, variant, _ = pick(family, variant)
        snapshot = _snapshot(model)
        context = context or context_for(snapshot, owner, locale=self.config.locale)
        validate_owner(snapshot, context)
        options = _validated_options(family, context, options)
        artwork = art if isinstance(art, Artwork) else Artwork(art) if art is not None else None
        iterator = self._iterate(
            family, snapshot, context, variant, artwork, output or OutputConfig(), options
        )
        try:
            async for page in iterator:
                yield page
        finally:
            await iterator.aclose()

    async def _iterate(
        self,
        family: str,
        model: Any,
        context: RenderContext,
        variant: str,
        artwork: Artwork | None,
        output: OutputConfig,
        options: dict[str, Any],
    ) -> AsyncGenerator[CardResult, None]:
        task = asyncio.current_task()
        if task is not None:
            self._active.add(task)
        iterator = None
        try:
            async with self._admission:
                self._check_open()
                _, _, module = pick(family, variant)
                overrides = {}
                if artwork is not None:
                    overrides["custom_art"] = await self.assets.load(artwork)
                issues = _source_issues(model)
                if (
                    family
                    in {
                        "factory",
                        "exploration",
                        "activity",
                        "monument",
                        "monument_detail",
                        "contingency_contract",
                        "contingency_contract_detail",
                    }
                    and (profile := options.get("profile")) is not None
                ):
                    issues.extend(
                        RenderIssue(issue.code, str(issue.message))
                        for issue in getattr(profile, "issues", [])
                    )
                assets = LazyAssets(
                    self.assets, asyncio.get_running_loop(), issues=issues, overrides=overrides
                )
                draw: Any = getattr(module, "iter_render", module.render)
                kwargs = dict(variant=variant, assets=assets, **options)
                if family == "character":
                    kwargs["artwork"] = artwork
                iterator = await self._executor.run(
                    lambda: iter(draw(model, context, **kwargs)), on_cancel=assets.cancel_pending
                )
                page = 0
                while True:
                    self._check_open()
                    value = await self._executor.run(
                        _next_page, iterator, output, on_cancel=assets.cancel_pending
                    )
                    if value is None:
                        break
                    page += 1
                    data, width, height = value
                    if task is not None:
                        self._active.discard(task)
                    yield CardResult(
                        data,
                        output.format,
                        width,
                        height,
                        family,
                        variant,
                        page=page,
                        pages=0,
                        issues=tuple(issues),
                    )
                    if task is not None:
                        self._active.add(task)
        except CardError:
            raise
        except (TypeError, ValueError, AttributeError, OSError) as exc:
            raise RenderError(f"{family} card could not be rendered") from exc
        finally:
            if iterator is not None and hasattr(iterator, "close"):
                await asyncio.to_thread(iterator.close)
            if task is not None:
                self._active.discard(task)

    async def render_batch(self, requests: Iterable[RenderRequest]) -> list[BatchItem]:
        """Keep input order and item failures while scheduling a bounded chunk."""
        results: list[BatchItem] = []
        pending: list[tuple[int, RenderRequest]] = []

        async def one(index: int, request: RenderRequest) -> BatchItem:
            try:
                pages = await self.render(
                    request.family, request.model, context=request.context, variant=request.variant
                )
                return BatchItem(index, tuple(pages))
            except CardError as exc:
                return BatchItem(index, error=exc)

        for index, request in enumerate(requests):
            pending.append((index, request))
            if len(pending) == self.config.admitted_jobs:
                results.extend(await asyncio.gather(*(one(i, item) for i, item in pending)))
                pending.clear()
        if pending:
            results.extend(await asyncio.gather(*(one(i, item) for i, item in pending)))
        return results

    async def fetch(self, family: str, **ids: Any) -> Any:
        """Delegate public/explicit-owner fetching to an injected SDK client."""
        self._check_open()
        if self.skport is None:
            raise FetchError("fetching requires an injected SkportClient", code="missing_sdk")
        canonical, _, _ = pick(family)
        method = {
            "profile": "card",
            "character": "character",
            "roster": "characters",
            "activity": "activity",
            "factory": "factory",
            "exploration": "factory",
            "monument": "monument",
            "monument_detail": "monument",
            "contingency_contract": "contract",
            "contingency_contract_detail": "contract",
        }.get(canonical)
        if method is None:
            raise FetchError(
                "pulls and wiki currently require supplied normalized models", code="supplied_model_required"
            )
        if "token" in ids and method in {"card", "character", "characters"}:
            method = "owned_" + method
        game = getattr(self.skport, "endfield", self.skport)
        try:
            return await getattr(game, method)(**ids)
        except Exception as exc:
            raise FetchError(f"SDK could not fetch {canonical}") from exc

    async def render_compare(
        self,
        first: Any,
        second: Any,
        *,
        context: RenderContext | None = None,
        second_context: RenderContext | None = None,
        variant: str = "field",
        art: Any = None,
        second_art: Any = None,
        output: OutputConfig | None = None,
        details: bool = False,
    ) -> list[CardResult]:
        """Compare the same canonical operator from two explicit owner models."""
        from endfield_cards.rendering.templates import compare

        self._check_open()
        _, variant, _ = pick("character", variant)
        first, second = _snapshot(first), _snapshot(second)
        context = context or context_for(first, locale=self.config.locale)
        second_context = second_context or context_for(second, locale=self.config.locale)
        validate_owner(first, context)
        validate_owner(second, second_context)
        compare.validate_pair(first, second)
        output = output or OutputConfig()
        artwork = art if isinstance(art, Artwork) else Artwork(art) if art is not None else None
        second_artwork = (
            second_art
            if isinstance(second_art, Artwork)
            else Artwork(second_art)
            if second_art is not None
            else None
        )
        task = asyncio.current_task()
        if task is not None:
            self._active.add(task)
        try:
            async with self._admission:
                self._check_open()
                issues = [
                    RenderIssue(issue.code, str(issue.message))
                    for model in (first, second)
                    for issue in getattr(model, "issues", [])
                ]
                assets = LazyAssets(self.assets, asyncio.get_running_loop(), issues=issues)
                if artwork:
                    assets["custom_art"] = await self.assets.load(artwork)
                if second_artwork:
                    assets["second_custom_art"] = await self.assets.load(second_artwork)

                def draw() -> list[CardResult]:
                    images = compare.iter_render(
                        first,
                        second,
                        context,
                        second_context,
                        variant=variant,
                        assets=assets,
                        artwork=artwork,
                        second_artwork=second_artwork,
                        details=details,
                    )
                    results = []
                    for index, image in enumerate(images):
                        try:
                            results.append(
                                CardResult(
                                    encode(image, output),
                                    output.format,
                                    image.width,
                                    image.height,
                                    "character",
                                    variant,
                                    index + 1,
                                    0,
                                )
                            )
                        finally:
                            image.close()
                    return [
                        replace(result, pages=len(results), issues=tuple(assets.issues)) for result in results
                    ]

                return await self._executor.run(draw, on_cancel=assets.cancel_pending)
        except CardError:
            raise
        except (TypeError, ValueError, AttributeError, OSError) as exc:
            raise RenderError("comparison card could not be rendered") from exc
        finally:
            if task is not None:
                self._active.discard(task)

    async def render_with_data(
        self,
        family: str,
        model: Any,
        *,
        context: RenderContext | None = None,
        owner: Any = None,
        variant: str | None = None,
        art: Any = None,
        output: OutputConfig | None = None,
        **options: Any,
    ) -> RenderedCard[Any, RenderInfo]:
        """Return images, a private SDK model and typed downstream selection data."""
        from endfield_cards.utils.selection import bundle_render

        self._check_open()
        family, variant, _ = pick(family, variant)
        snapshot, options = _snapshot(model), _snapshot(options)
        context = context or context_for(snapshot, owner, locale=self.config.locale)
        if family == "activity":
            context = replace(context, display_timezone="UTC")
        options = _validated_options(family, context, options)
        pages = await self.render(
            family, snapshot, context=context, variant=variant, art=art, output=output, **options
        )
        return bundle_render(family, snapshot, pages, context, **options)

    async def render_profile_with_data(
        self, model: Any, **kwargs: Any
    ) -> RenderedCard[Any, CharacterListInfo]:
        return cast(
            RenderedCard[Any, CharacterListInfo], await self.render_with_data("profile", model, **kwargs)
        )

    async def render_roster_with_data(
        self, model: Any, **kwargs: Any
    ) -> RenderedCard[Any, CharacterListInfo]:
        return cast(
            RenderedCard[Any, CharacterListInfo], await self.render_with_data("roster", model, **kwargs)
        )

    async def render_live_with_data(self, model: Any, **kwargs: Any) -> RenderedCard[Any, LiveInfo]:
        return cast(RenderedCard[Any, LiveInfo], await self.render_with_data("activity", model, **kwargs))

    async def render_monument_with_data(self, model: Any, **kwargs: Any) -> RenderedCard[Any, MonumentInfo]:
        return cast(RenderedCard[Any, MonumentInfo], await self.render_with_data("monument", model, **kwargs))

    async def render_contingency_contract_with_data(
        self, model: Any, **kwargs: Any
    ) -> RenderedCard[Any, ContractInfo]:
        return cast(
            RenderedCard[Any, ContractInfo],
            await self.render_with_data("contingency_contract", model, **kwargs),
        )

    async def render_profile(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("profile", model, **kwargs)

    async def render_character(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("character", model, **kwargs)

    async def render_roster(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("roster", model, **kwargs)

    async def render_activity(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("activity", model, **kwargs)

    render_live = render_activity

    async def render_factory(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("factory", model, **kwargs)

    async def render_exploration(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("exploration", model, **kwargs)

    async def render_monument(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("monument", model, **kwargs)

    async def render_monument_detail(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("monument_detail", model, **kwargs)

    render_monument_event = render_monument_detail

    async def render_contingency_contract(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("contingency_contract", model, **kwargs)

    async def render_contingency_contract_detail(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("contingency_contract_detail", model, **kwargs)

    render_contract = render_contingency_contract
    render_contract_detail = render_contingency_contract_detail

    async def render_pulls(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("pulls", model, **kwargs)

    async def render_wiki(self, model: Any, **kwargs: Any) -> list[CardResult]:
        return await self.render("wiki", model, **kwargs)
