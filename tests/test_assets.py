from __future__ import annotations

import asyncio
import io
from pathlib import Path

import aiohttp
import pytest
from aiohttp import web
from PIL import Image

from endfield_cards.assets.download import Downloader
from endfield_cards.assets.images import decode_image
from endfield_cards.assets.store import AssetStore
from endfield_cards.config import CacheConfig, DownloadConfig
from endfield_cards.errors import DownloadError, ImageDecodeError, ResourceClosedError
from endfield_cards.models.artwork import Artwork


def png(color: str = "red", size: tuple[int, int] = (3, 3)) -> bytes:
    output = io.BytesIO()
    Image.new("RGBA", size, color).save(output, "PNG")
    return output.getvalue()


def test_decode_limits_and_custom_pixels() -> None:
    source = png()
    assert decode_image(source).size == (3, 3)
    with pytest.raises(ImageDecodeError):
        decode_image(source, max_bytes=len(source) - 1)
    with pytest.raises(ImageDecodeError):
        decode_image(source, max_pixels=8)
    with pytest.raises(ImageDecodeError):
        decode_image(b"not an image")


@pytest.mark.asyncio
async def test_single_flight_cancellation_and_clear_invalidates(tmp_path: Path) -> None:
    store = AssetStore(CacheConfig(directory=tmp_path, disk_bytes=1024))
    entered = asyncio.Event()
    release = asyncio.Event()
    calls = 0

    async def fetch(url: str) -> bytes:
        nonlocal calls
        calls += 1
        entered.set()
        await release.wait()
        return png()

    store.downloader.fetch = fetch
    first = asyncio.create_task(store.get("https://example.test/art.png"))
    second = asyncio.create_task(store.get("https://example.test/art.png"))
    await entered.wait()
    first.cancel()
    with pytest.raises(asyncio.CancelledError):
        await first
    await store.clear_cache()
    release.set()
    image = await second
    assert image.size == (3, 3) and calls == 1
    assert store.stats["decoded"]["entries"] == 0
    assert not list(tmp_path.glob("*.cache"))
    await store.get("https://example.test/art.png")
    assert calls == 2
    await store.aclose()


@pytest.mark.asyncio
async def test_cache_off_and_art_retention_and_path_changes(tmp_path: Path) -> None:
    store = AssetStore(CacheConfig(enabled=False, directory=tmp_path / "off"))
    calls = 0

    async def fetch(url: str) -> bytes:
        nonlocal calls
        calls += 1
        return png()

    store.downloader.fetch = fetch
    await store.get("https://example.test/art.png")
    await store.get("https://example.test/art.png")
    assert calls == 2 and not (tmp_path / "off").exists()
    source = Image.new("RGBA", (3, 3), "red")
    output = await store.load(source)
    output.putpixel((0, 0), (0, 0, 0, 0))
    assert source.getpixel((0, 0)) == (255, 0, 0, 255)
    file = tmp_path / "custom.png"
    file.write_bytes(png("red"))
    assert (await store.load(file)).getpixel((0, 0)) == (255, 0, 0, 255)
    file.write_bytes(png("blue"))
    assert (await store.load(file)).getpixel((0, 0)) == (0, 0, 255, 255)
    with pytest.raises(ImageDecodeError):
        await store.load("https://example.test/art.png")
    await store.aclose()
    with pytest.raises(ResourceClosedError):
        await store.get("https://example.test/art.png")


@pytest.mark.asyncio
async def test_http_bounds_redirect_policy_and_borrowed_session(tmp_path: Path) -> None:
    app = web.Application()

    async def image_response(request: web.Request) -> web.Response:
        return web.Response(body=png(), content_type="image/png")

    async def oversized_response(request: web.Request) -> web.Response:
        return web.Response(body=b"x" * 1000, content_type="image/png")

    async def invalid_response(request: web.Request) -> web.Response:
        return web.Response(text="not image", content_type="text/html")

    async def redirect_response(request: web.Request) -> web.Response:
        raise web.HTTPFound("/image")

    app.router.add_get("/image", image_response)
    app.router.add_get("/oversized", oversized_response)
    app.router.add_get("/invalid", invalid_response)
    app.router.add_get("/redirect", redirect_response)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    base = f"http://127.0.0.1:{runner.addresses[0][1]}"
    try:
        async with aiohttp.ClientSession() as session:
            store = AssetStore(
                CacheConfig(directory=tmp_path, disk_bytes=0), DownloadConfig(max_bytes=200), session=session
            )
            assert (await store.get(base + "/image")).size == (3, 3)
            with pytest.raises(DownloadError):
                await store.get(base + "/oversized")
            with pytest.raises(DownloadError):
                await store.get(base + "/invalid")
            await store.aclose()
            assert not session.closed
            downloader = Downloader(DownloadConfig(max_redirects=0), session=session)
            with pytest.raises(DownloadError):
                await downloader.fetch(base + "/redirect")
            await downloader.aclose()
            denied = Downloader(session=session, url_policy=lambda url: not url.endswith("/image"))
            with pytest.raises(DownloadError):
                await denied.fetch(base + "/redirect")
            await denied.aclose()
        owned = Downloader()
        assert await owned.fetch(base + "/image") == png()
        await owned.aclose()
        assert owned._session.closed
    finally:
        await runner.cleanup()


@pytest.mark.asyncio
async def test_custom_remote_retention_defaults_off(tmp_path: Path) -> None:
    store = AssetStore(CacheConfig(directory=tmp_path))
    calls = 0

    async def fetch(url: str) -> bytes:
        nonlocal calls
        calls += 1
        return png()

    store.downloader.fetch = fetch
    art = Artwork("https://example.test/custom.png", allow_remote=True)
    await store.load(art)
    await store.load(art)
    assert calls == 2
    assert not list(tmp_path.glob("*.cache"))
    await store.aclose()


@pytest.mark.asyncio
async def test_close_continues_when_waiter_is_cancelled(tmp_path: Path) -> None:
    store = AssetStore(CacheConfig(directory=tmp_path))
    entered = asyncio.Event()
    release = asyncio.Event()
    finished = asyncio.Event()

    async def close_downloader() -> None:
        entered.set()
        await release.wait()
        finished.set()

    store.downloader.aclose = close_downloader
    closing = asyncio.create_task(store.aclose())
    await entered.wait()
    closing.cancel()
    with pytest.raises(asyncio.CancelledError):
        await closing
    release.set()
    await store.aclose()
    assert finished.is_set()


def test_bundled_icons_are_verified_and_return_private_pixels(tmp_path: Path) -> None:
    store = AssetStore(CacheConfig(directory=tmp_path))
    icon = store.local("stat.Atk", (24, 24))
    original = icon.copy()
    icon.paste((255, 0, 0, 0), (0, 0, icon.width, icon.height))
    assert store.local("stat.Atk", (24, 24)).tobytes() == original.tobytes()
    assert not tmp_path.exists() or not list(tmp_path.glob("*.cache"))
