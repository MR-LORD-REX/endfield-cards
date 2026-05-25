from typing import Dict, Tuple, Optional
from collections import OrderedDict
from pathlib import Path

from PIL import Image
import asyncio
import aiohttp
import io

from .asset_map import asset_mapping, asset_lit

assets_base_path = Path(__file__).parent.parent.parent / "assets"


class AssetsRegistry:
    def __init__(self, mapping: Dict[str, Path]):
        self.mapping = mapping

    def get(self, key: str) -> Optional[Path]:
        path = self.mapping.get(key)
        if path is None:
            print(f"Asset with key '{key}' not found in registry.")
        return path


class AssetCache:
    def __init__(self, max_raw: int = 200, max_sized: int = 200):
        self._raw: OrderedDict[str, Image.Image] = OrderedDict()
        self._sized: OrderedDict[str, Image.Image] = OrderedDict()
        self.max_raw = max_raw
        self.max_sized = max_sized
        self.enabled: bool = True

    def get_raw(self, key: str) -> Optional[Image.Image]:
        if not self.enabled:
            return None
        if key in self._raw:
            self._raw.move_to_end(key)
            return self._raw[key]
        return None

    def set_raw(self, key: str, image: Image.Image):
        if not self.enabled:
            return
        self._raw[key] = image
        self._raw.move_to_end(key)
        if len(self._raw) > self.max_raw:
            self._raw.popitem(last=False)

    def get_sized(self, key: str, size: Tuple[int, int]) -> Optional[Image.Image]:
        if not self.enabled:
            return None
        sized_key = f"{key}_{size[0]}x{size[1]}"
        if sized_key in self._sized:
            self._sized.move_to_end(sized_key)
            return self._sized[sized_key]
        return None

    def set_sized(self, key: str, size: Tuple[int, int], image: Image.Image):
        if not self.enabled:
            return
        sized_key = f"{key}_{size[0]}x{size[1]}"
        self._sized[sized_key] = image
        self._sized.move_to_end(sized_key)
        if len(self._sized) > self.max_sized:
            self._sized.popitem(last=False)


class AssetLoader:
    def __init__(self, registry: AssetsRegistry, cache: AssetCache):
        self.registry = registry
        self.cache = cache

    async def load(self, key: str) -> Optional[Image.Image]:
        cached = self.cache.get_raw(key)
        if cached:
            return cached

        path = self.registry.get(key)
        if not path:
            return None

        image = await asyncio.to_thread(self._load_sync, path)
        if image:
            self.cache.set_raw(key, image)
        return image

    def _load_sync(self, path: Path) -> Optional[Image.Image]:
        return Image.open(path).convert("RGBA")


class AssetProcessor:
    async def process(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        return await asyncio.to_thread(self._resize, image, size)

    def _resize(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        return image.resize(size, Image.LANCZOS)


class AssetManager:
    def __init__(
        self,
        registry: AssetsRegistry,
        cache: AssetCache,
        loader: AssetLoader,
        processor: AssetProcessor,
        session: aiohttp.ClientSession | None = None,
    ):
        self.registry = registry
        self.cache = cache
        self.loader = loader
        self.processor = processor
        self._inflight: Dict[str, asyncio.Task] = {}
        self.session = session
        self._session_owner = session is None
        self._connector: aiohttp.TCPConnector | None = None

    @property
    def cache_enabled(self) -> bool:
        return self.cache.enabled

    @cache_enabled.setter
    def cache_enabled(self, value: bool):
        self.cache.enabled = value

    async def get_asset(self, key: asset_lit, size: Tuple[int, int] | None = None) -> Optional[Image.Image]:
        if size:
            cached = self.cache.get_sized(key, size)
            if cached:
                return cached
        else:
            cached = self.cache.get_raw(key)
            if cached:
                return cached

        inflight_key = f"{key}_{size[0]}x{size[1]}" if size else key
        if inflight_key in self._inflight:
            return await self._inflight[inflight_key]

        task = asyncio.create_task(self._load_and_process(key, size))
        self._inflight[inflight_key] = task

        try:
            return await task
        finally:
            self._inflight.pop(inflight_key, None)

    async def _load_and_process(self, key: str, size: Tuple[int, int] | None) -> Optional[Image.Image]:
        raw = await self.loader.load(key)
        if raw is None:
            return None

        if size is None:
            return raw

        sized = await self.processor.process(raw, size)
        self.cache.set_sized(key, size, sized)
        return sized

    async def _ensure_session(self, timeout: float = 20.0) -> None:
        if self.session is None:
            self._connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
            self.session = aiohttp.ClientSession(
                connector=self._connector,
                timeout=aiohttp.ClientTimeout(total=timeout)
            )

    async def get_asset_from_url(self, url: str, size: Tuple[int, int], timeout: float = 20.0) -> Optional[Image.Image]:
        await self._ensure_session(timeout)

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    raw_data = await response.read()
                    image = await asyncio.to_thread(Image.open, io.BytesIO(raw_data))
                    return await self.processor.process(image, size)
                else:
                    print(f"Failed to fetch image from URL: {url} with status {response.status}")
                    return Image.new("RGBA", size, (0, 0, 0, 0))
        except asyncio.TimeoutError:
            print(f"Timeout fetching image from URL: {url}")
            return None
        except Exception as e:
            print(f"Error fetching image from URL: {url} - {e}")
            return None

    async def close(self):
        if self.session is not None and self._session_owner:
            await asyncio.sleep(0.25)
            await self.session.close()
            self.session = None
        if self._connector is not None:
            await self._connector.close()
            self._connector = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


registry = AssetsRegistry(asset_mapping)
cache = AssetCache(max_raw=50, max_sized=50)
loader = AssetLoader(registry, cache)
processor = AssetProcessor()
asset_manager = AssetManager(registry, cache, loader, processor)