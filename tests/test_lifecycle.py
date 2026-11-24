from __future__ import annotations

import asyncio
import io
from dataclasses import dataclass
from threading import Event
from types import SimpleNamespace

import pytest
from PIL import Image

from endfield_cards import Cards
from endfield_cards.assets.store import AssetStore
from endfield_cards.config import CacheConfig, CardsConfig
from endfield_cards.errors import DownloadError, OwnerMismatchError, RenderError, ResourceClosedError
from endfield_cards.models import OwnerIdentity, RenderContext


@dataclass(frozen=True)
class Source:
    owner: OwnerIdentity
    marker: int = 1


def fake_template(monkeypatch: pytest.MonkeyPatch, draw: object) -> None:
    module = SimpleNamespace(iter_render=draw, render=draw)
    monkeypatch.setattr(
        "endfield_cards.client.pick", lambda family, variant=None: (family, variant or "field", module)
    )


@pytest.mark.asyncio
async def test_render_cache_isolates_owners_and_rejects_mismatch_before_drawing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    def draw(model: Source, context: RenderContext, **kwargs: object) -> object:
        calls.append(context.owner.game_uid)
        yield Image.new("RGBA", (10, 10), "red" if context.owner.game_uid == "10001" else "blue")

    fake_template(monkeypatch, draw)
    first = Source(OwnerIdentity("One", "10001"))
    second = Source(OwnerIdentity("Two", "10002"))
    async with Cards() as cards:
        one = await cards.render_character(first)
        two = await cards.render_character(second)
        assert one[0].data != two[0].data
        cached = await cards.render_character(first)
        assert cached == one and calls == ["10001", "10002"]
        altered = cached[0].to_pillow()
        altered.paste((0, 0, 0, 0), (0, 0, 10, 10))
        assert (await cards.render_character(first))[0].to_pillow().getpixel((0, 0)) == (255, 0, 0, 255)
        with pytest.raises(OwnerMismatchError):
            await cards.render_character(first, context=RenderContext(second.owner))
        assert calls == ["10001", "10002"]


@pytest.mark.asyncio
async def test_render_single_flight_survives_waiter_cancellation(monkeypatch: pytest.MonkeyPatch) -> None:
    entered, release = Event(), Event()
    calls = 0

    def draw(model: Source, context: RenderContext, **kwargs: object) -> object:
        nonlocal calls
        calls += 1
        entered.set()
        assert release.wait(5)
        yield Image.new("RGBA", (10, 10), "red")

    fake_template(monkeypatch, draw)
    source = Source(OwnerIdentity("One", "10001"))
    async with Cards() as cards:
        first = asyncio.create_task(cards.render_character(source))
        second = asyncio.create_task(cards.render_character(source))
        assert await asyncio.to_thread(entered.wait, 3)
        first.cancel()
        with pytest.raises(asyncio.CancelledError):
            await first
        release.set()
        assert len(await second) == 1
        assert calls == 1


@pytest.mark.asyncio
async def test_borrowed_assets_and_sdk_are_not_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    closed = []
    assets = AssetStore(CacheConfig(enabled=False))
    sdk = SimpleNamespace(aclose=lambda: closed.append("sdk"))
    cards = Cards(asset_store=assets, skport=sdk)
    await cards.aclose()
    await cards.aclose()
    assert not assets.stats["closed"] and closed == []
    await assets.aclose()
    with pytest.raises(ResourceClosedError):
        await cards.render_character(Source(OwnerIdentity("One", "10001")))


@pytest.mark.asyncio
async def test_closing_with_suspended_page_iterator_preserves_consumer_task(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    closed = []

    def draw(model: Source, context: RenderContext, **kwargs: object) -> object:
        try:
            yield Image.new("RGBA", (10, 10), "red")
            yield Image.new("RGBA", (10, 10), "blue")
        finally:
            closed.append("generator")

    fake_template(monkeypatch, draw)
    cards = Cards(config=CardsConfig(cache=CacheConfig(enabled=False)))
    iterator = cards.iter_pages("character", Source(OwnerIdentity("One", "10001")))
    await anext(iterator)
    await cards.aclose()
    await iterator.aclose()
    assert closed == ["generator"]


@pytest.mark.asyncio
async def test_closing_active_uncached_render_releases_generator(monkeypatch: pytest.MonkeyPatch) -> None:
    entered, release = Event(), Event()
    closed = []

    def draw(model: Source, context: RenderContext, **kwargs: object) -> object:
        try:
            entered.set()
            assert release.wait(5)
            yield Image.new("RGBA", (10, 10), "red")
        finally:
            closed.append("generator")

    fake_template(monkeypatch, draw)
    cards = Cards(config=CardsConfig(cache=CacheConfig(enabled=False)))
    rendering = asyncio.create_task(cards.render_character(Source(OwnerIdentity("One", "10001"))))
    assert await asyncio.to_thread(entered.wait, 3)
    closing = asyncio.create_task(cards.aclose())
    release.set()
    await closing
    with pytest.raises(asyncio.CancelledError):
        await rendering
    assert closed == ["generator"]


@pytest.mark.asyncio
async def test_comparison_participates_in_active_shutdown(monkeypatch: pytest.MonkeyPatch) -> None:
    from endfield_cards.rendering.templates import compare

    entered, release = Event(), Event()

    def draw(*args: object, **kwargs: object) -> list[Image.Image]:
        entered.set()
        assert release.wait(5)
        return [Image.new("RGBA", (10, 10), "red")]

    fake_template(monkeypatch, draw)
    monkeypatch.setattr(compare, "validate_pair", lambda first, second: None)
    monkeypatch.setattr(compare, "iter_render", lambda *args, **kwargs: iter(draw(*args, **kwargs)))
    cards = Cards(config=CardsConfig(cache=CacheConfig(enabled=False)))
    rendering = asyncio.create_task(
        cards.render_compare(Source(OwnerIdentity("One", "10001")), Source(OwnerIdentity("Two", "10002")))
    )
    assert await asyncio.to_thread(entered.wait, 3)
    closing = asyncio.create_task(cards.aclose())
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    release.set()
    await closing
    with pytest.raises(asyncio.CancelledError):
        await rendering


@pytest.mark.asyncio
async def test_comparison_closes_encoded_source_images(monkeypatch: pytest.MonkeyPatch) -> None:
    from endfield_cards.rendering.templates import compare

    pixels = [Image.new("RGBA", (10, 10), "red"), Image.new("RGBA", (10, 10), "blue")]
    fake_template(monkeypatch, lambda *args, **kwargs: [])
    monkeypatch.setattr(compare, "validate_pair", lambda first, second: None)
    monkeypatch.setattr(compare, "iter_render", lambda *args, **kwargs: iter(pixels))
    async with Cards(config=CardsConfig(cache=CacheConfig(enabled=False))) as cards:
        results = await cards.render_compare(
            Source(OwnerIdentity("One", "10001")), Source(OwnerIdentity("Two", "10002"))
        )
        assert len(results) == 2
    for image in pixels:
        with pytest.raises(ValueError):
            image.getpixel((0, 0))


@pytest.mark.asyncio
async def test_comparison_translates_template_failure_and_preserves_cause(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from endfield_cards.rendering.templates import compare

    def failed(*args: object, **kwargs: object) -> object:
        raise ValueError("invalid template source")

    fake_template(monkeypatch, failed)
    monkeypatch.setattr(compare, "validate_pair", lambda first, second: None)
    monkeypatch.setattr(compare, "iter_render", failed)
    async with Cards(config=CardsConfig(cache=CacheConfig(enabled=False))) as cards:
        with pytest.raises(RenderError) as exc:
            await cards.render_compare(
                Source(OwnerIdentity("One", "10001")), Source(OwnerIdentity("Two", "10002"))
            )
        assert isinstance(exc.value.__cause__, ValueError)


@pytest.mark.asyncio
async def test_optional_image_failure_is_reported_once_and_does_not_poison_render_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_url = "https://example.test/optional.png"
    calls = 0

    def draw(model: Source, context: RenderContext, **kwargs: object) -> object:
        images = kwargs["assets"]
        source = images.get(source_url)
        again = images.get(source_url)
        assert (source is None) == (again is None)
        yield source.copy() if source is not None else Image.new("RGBA", (10, 10), "gray")

    async def fetch(url: str) -> bytes:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise DownloadError("HTTP 503")
        buffer = io.BytesIO()
        Image.new("RGBA", (10, 10), "blue").save(buffer, "PNG")
        return buffer.getvalue()

    fake_template(monkeypatch, draw)
    assets = AssetStore(CacheConfig(disk_bytes=0))
    assets.downloader.fetch = fetch
    cards = Cards(asset_store=assets)
    source = Source(OwnerIdentity("One", "10001"))
    try:
        first = await cards.render_character(source)
        assert len(first[0].issues) == 1 and first[0].issues[0].code == "download_failed"
        assert calls == 1
        second = await cards.render_character(source)
        assert second[0].issues == () and calls == 2
        assert first[0].data != second[0].data
        third = await cards.render_character(source)
        assert third == second and calls == 2
    finally:
        await cards.aclose()
        await assets.aclose()


@pytest.mark.asyncio
async def test_cache_off_remote_decode_uses_live_worker_bridge_without_persistence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def draw(model: Source, context: RenderContext, **kwargs: object) -> object:
        image = kwargs["assets"].get("https://example.test/uncached.png")
        yield image.copy()

    async def fetch(url: str) -> bytes:
        nonlocal calls
        calls += 1
        buffer = io.BytesIO()
        Image.new("RGBA", (20, 20), "red").save(buffer, "PNG")
        return buffer.getvalue()

    fake_template(monkeypatch, draw)
    config = CardsConfig(cache=CacheConfig(enabled=False, decoded_bytes=0, disk_bytes=0))
    async with Cards(config=config) as cards:
        cards.assets.downloader.fetch = fetch
        source = Source(OwnerIdentity("One", "10001"))
        first = await asyncio.wait_for(cards.render_character(source), timeout=3)
        second = await asyncio.wait_for(cards.render_character(source), timeout=3)
        assert first == second and calls == 2
        assert cards.cache_stats["renders"]["bytes"] == 0
        assert cards.cache_stats["assets"]["decoded"]["bytes"] == 0


@pytest.mark.asyncio
async def test_close_cancels_lazy_waiter_without_closing_borrowed_shared_download(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entered, release = asyncio.Event(), asyncio.Event()
    source_url = "https://example.test/shared.png"

    def draw(model: Source, context: RenderContext, **kwargs: object) -> object:
        image = kwargs["assets"].get(source_url)
        yield image.copy()

    async def fetch(url: str) -> bytes:
        entered.set()
        await release.wait()
        buffer = io.BytesIO()
        Image.new("RGBA", (10, 10), "blue").save(buffer, "PNG")
        return buffer.getvalue()

    fake_template(monkeypatch, draw)
    assets = AssetStore(CacheConfig(enabled=False))
    assets.downloader.fetch = fetch
    cards = Cards(config=CardsConfig(cache=CacheConfig(enabled=False)), asset_store=assets)
    rendering = asyncio.create_task(cards.render_character(Source(OwnerIdentity("One", "10001"))))
    await entered.wait()
    shared = asyncio.create_task(assets.get(source_url))
    closing = asyncio.create_task(cards.aclose())
    timed_out = False
    try:
        await asyncio.wait_for(asyncio.shield(closing), timeout=1)
    except TimeoutError:
        timed_out = True
    finally:
        release.set()
        await closing
        with pytest.raises(asyncio.CancelledError):
            await rendering
        assert (await shared).size == (10, 10)
        assert not assets.stats["closed"]
        await assets.aclose()
    assert not timed_out, "render close waited for an unrelated shared HTTP flight"
