"""Central image resources, downloads, caches and ownership boundaries."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import aiohttp
from PIL import Image

from endfield_cards.assets.download import Downloader, URLPolicy
from endfield_cards.assets.images import decode_image, load_local
from endfield_cards.assets.manifest import Manifest
from endfield_cards.cache import ByteLRU, DiskCache, cache_key
from endfield_cards.config import CacheConfig, DownloadConfig
from endfield_cards.errors import ImageDecodeError, ResourceClosedError


class AssetStore:
    """Share downloaded images safely while every returned image belongs to its caller."""

    def __init__(
        self,
        cache: CacheConfig | None = None,
        download: DownloadConfig | None = None,
        *,
        session: aiohttp.ClientSession | None = None,
        url_policy: URLPolicy | None = None,
    ) -> None:
        self.cache_config = cache or CacheConfig()
        self.download_config = download or DownloadConfig()
        self._memory: ByteLRU[Image.Image] = ByteLRU(
            self.cache_config.decoded_bytes if self.cache_config.enabled else 0,
            ttl_seconds=self.cache_config.ttl_seconds,
        )
        self._disk = DiskCache(
            self.cache_config.directory,
            max_bytes=self.cache_config.disk_bytes if self.cache_config.enabled else 0,
            ttl_seconds=self.cache_config.ttl_seconds,
        )
        self.downloader = Downloader(self.download_config, session=session, url_policy=url_policy)
        self._manifest: Manifest | None = None
        self._flights: dict[str, asyncio.Task[Image.Image]] = {}
        self._generation = 0
        self._closed = False
        self._close_task: asyncio.Task[None] | None = None
        self._load_slots = asyncio.Semaphore(self.download_config.concurrency)
        decode_slots = max(1, self.cache_config.decoded_bytes // (self.download_config.max_pixels * 4))
        self._decode_slots = asyncio.Semaphore(min(2, decode_slots))

    def _assert_open(self) -> None:
        if self._closed:
            raise ResourceClosedError("asset store is closed")

    async def get(self, url: str, *, retain: bool = True) -> Image.Image:
        """Fetch one image, coalescing concurrent callers without sharing mutable pixels."""
        self._assert_open()
        key = cache_key("image-source-v1", url)
        if self.cache_config.enabled and retain:
            cached = self._memory.get(key)
            if cached is not None:
                return cached
        flight_key = f"{self._generation}:{int(retain)}:{key}"
        task = self._flights.get(flight_key)
        if task is None:
            task = asyncio.create_task(
                self._load_url(url, key, retain, self._generation, self._disk.generation)
            )
            self._flights[flight_key] = task
            task.add_done_callback(lambda completed: self._finish_flight(flight_key, completed))
        result = await asyncio.shield(task)
        self._assert_open()
        return result.copy()

    def _finish_flight(self, key: str, task: asyncio.Task[Image.Image]) -> None:
        if self._flights.get(key) is task:
            self._flights.pop(key, None)
        if not task.cancelled():
            task.exception()

    async def _decode(self, data: bytes) -> Image.Image:
        return await self._image_worker(decode_image, data)

    async def _image_worker(self, function: Any, source: Any) -> Image.Image:
        async with self._decode_slots:
            task = asyncio.create_task(
                asyncio.to_thread(
                    function,
                    source,
                    max_bytes=self.download_config.max_bytes,
                    max_pixels=self.download_config.max_pixels,
                )
            )
            try:
                return await asyncio.shield(task)
            except asyncio.CancelledError:
                await task
                raise

    async def _load_url(
        self, url: str, key: str, retain: bool, generation: int, disk_generation: int
    ) -> Image.Image:
        async with self._load_slots:
            return await self._load_source(url, key, retain, generation, disk_generation)

    async def _load_source(
        self, url: str, key: str, retain: bool, generation: int, disk_generation: int
    ) -> Image.Image:
        cacheable = self.cache_config.enabled and retain
        if cacheable:
            stored = await self._disk.get(key, max_bytes=self.download_config.max_bytes)
            if stored is not None:
                try:
                    image = await self._decode(stored)
                except ImageDecodeError:
                    stored = None
                else:
                    if generation == self._generation and not self._closed:
                        self._memory.put(key, image)
                    return image
        data = await self.downloader.fetch(url)
        image = await self._decode(data)
        if cacheable and generation == self._generation and not self._closed:
            await self._disk.put(key, data, generation=disk_generation)
            if generation == self._generation and not self._closed:
                self._memory.put(key, image)
        return image

    async def load(self, artwork: Any) -> Image.Image:
        """Load Artwork or a local source; remote custom art requires explicit opt-in."""
        self._assert_open()
        source = getattr(artwork, "source", artwork)
        if isinstance(source, str) and source.lower().startswith(("http://", "https://")):
            if not getattr(artwork, "allow_remote", False):
                raise ImageDecodeError("remote custom artwork requires allow_remote=True")
            return await self.get(source, retain=bool(getattr(artwork, "retain", False)))
        async with self._load_slots:
            return await self._image_worker(load_local, source)

    def local(self, key: str, size: tuple[int, int] | None = None) -> Image.Image:
        """Decode a verified bundled icon; use from rendering worker threads."""
        self._assert_open()
        if self._manifest is None:
            self._manifest = Manifest()
        image_key = cache_key("local-icon-v1", key, size)
        cached = self._memory.get(image_key) if self.cache_config.enabled else None
        if cached is not None:
            return cached
        image = load_local(
            Path(self._manifest.path(key)),
            max_bytes=self.download_config.max_bytes,
            max_pixels=self.download_config.max_pixels,
        )
        if size is not None:
            image.thumbnail(size, Image.Resampling.LANCZOS)
        if self.cache_config.enabled:
            self._memory.put(image_key, image)
        return image.copy()

    async def clear_cache(self, *, memory: bool = True, disk: bool = True) -> None:
        """Invalidate in-flight publications and independently clear cache scopes."""
        self._assert_open()
        self._generation += 1
        if memory:
            self._memory.clear()
        if disk:
            await self._disk.clear()

    @property
    def stats(self) -> dict[str, Any]:
        return {
            "decoded": self._memory.stats,
            "in_flight": len(self._flights),
            "enabled": self.cache_config.enabled,
            "closed": self._closed,
        }

    async def aclose(self) -> None:
        """Cancel owned downloads and close the transport exactly once."""
        if self._close_task is None:
            self._closed = True
            self._generation += 1
            self._close_task = asyncio.create_task(self._close_resources())
        await asyncio.shield(self._close_task)

    async def _close_resources(self) -> None:
        tasks = list(self._flights.values())
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        await self.downloader.aclose()
        self._memory.clear()

    async def __aenter__(self) -> AssetStore:
        self._assert_open()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()
