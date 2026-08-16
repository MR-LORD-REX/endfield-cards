from typing import Dict, Tuple, Optional
from collections import OrderedDict
from pathlib import Path

from PIL import Image
import asyncio
import aiohttp
import io
import logging
import os

import json

from .asset_map import asset_mapping, asset_lit
from ...errors import AssetError

logger = logging.getLogger(__name__)


assets_base_path = Path(__file__).parent.parent.parent / "assets"

cwd=Path().cwd()

class AssetsRegistry:
    def __init__(self, mapping: Dict[str, Path]):
        self.mapping = mapping

    def get(self, key: str) -> Optional[Path]:
        path = self.mapping.get(key)
        if path is None:
            logger.warning(f"Asset with key '{key}' not found in registry.")
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
            error = AssetError(
                message=f"Asset key not found in registry",
                asset_name=key,
                context={"key": key}
            )
            error.log()
            return None

        try:
            image = await asyncio.to_thread(self._load_sync, path)
            if image:
                self.cache.set_raw(key, image)
                logger.debug(f"Successfully loaded asset: {key} from {path}")
            else:
                logger.warning(f"Asset loading returned None: {key} from {path}")
            return image
        except Exception as e:
            error = AssetError(
                message=f"Failed to load asset from disk: {e}",
                asset_name=key,
                original_error=e,
                context={"key": key, "path": str(path)}
            )
            error.log()
            return None

    def _load_sync(self, path: Path) -> Optional[Image.Image]:
        try:
            return Image.open(path).convert("RGBA")
        except Exception as e:
            logger.error(f"Error opening image file {path}: {e}")
            raise


class AssetProcessor:
    async def process(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        return await asyncio.to_thread(self._resize, image, size)

    def _resize(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        return image.resize(size)


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
        self.proxies = None
        self.debug = False
        self.local_cache=True
        self.cache_path = cwd / ".endfield_cache"
        try:
            with open("proxies.json") as f:
                self.proxies = json.load(f)
        except Exception as e:
            self.proxies = None
        os.makedirs(self.cache_path, exist_ok=True)
    
    def set_debug(self, debug: bool):
        """Set debug mode. When True, debug logs will be shown."""
        self.debug = debug
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

    @property
    def cache_enabled(self) -> bool:
        return self.cache.enabled

    @cache_enabled.setter
    def cache_enabled(self, value: bool):
        self.cache.enabled = value
        
    def load_downloaded_cache(self, cache_file: Path)->Optional[Image.Image]:
        with open(cache_file, "rb") as f:
            try:
                return Image.open(f).convert("RGBA")
            except Exception as e:
                logger.error(f"Error opening cached image file {cache_file}: {e}")
                return None
            
    def clear_all_local_assets(self):
        if self.cache_path.exists() and self.cache_path.is_dir():
            for file in self.cache_path.iterdir():
                try:
                    file.unlink()
                    logger.debug(f"Deleted cached asset: {file}")
                except Exception as e:
                    logger.error(f"Error deleting cached asset {file}: {e}")
        else:
            logger.info("No local cache directory found to clear.")

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
        try:
            raw = await self.loader.load(key)
            if raw is None:
                logger.warning(f"Failed to load raw asset: {key}")
                return None

            if size is None:
                return raw
            try:
                sized = await self.processor.process(raw, size)
                self.cache.set_sized(key, size, sized)
                logger.debug(f"Successfully processed asset: {key} to size {size}")
                return sized
            except Exception as e:
                error = AssetError(
                    message=f"Failed to process asset: {e}",
                    asset_name=key,
                    original_error=e,
                    context={"key": key, "size": size}
                )
                error.log()
                return None
        except Exception as e:
            logger.error(f"Unexpected error in _load_and_process for {key}: {e}")
            return None

    async def _ensure_session(self, timeout: float = 20.0) -> None:
        if self.session is None:
            self._connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
            self.session = aiohttp.ClientSession(
                connector=self._connector,
                timeout=aiohttp.ClientTimeout(total=timeout)
            )

    async def get_asset_from_url(self, url: str, size: Tuple[int, int], timeout: float = 50.0) -> Optional[Image.Image]:
        if self.local_cache:
            key=url.replace("https://enka.network/ui/ef/", "").split("/")[-1]
            key_without_ext = key.rsplit(".", 1)[0] if "." in key else key
            cache_file = self.cache_path / f"{key_without_ext}_{size[0]}x{size[1]}.png"
            if os.path.exists(cache_file):
                try:
                    image = await asyncio.to_thread(self.load_downloaded_cache, cache_file)
                    if image:
                        logger.debug(f"Loaded image from local cache: {key}")
                        return image
                except Exception as e:
                    logger.error(f"Error loading image from local cache {key}: {e}")
                    
        await self._ensure_session(timeout)
        proxies_to_try = [None] 
        if self.proxies and isinstance(self.proxies, list):
            proxies_to_try.extend(self.proxies)

        for attempt, proxy_url in enumerate(proxies_to_try):
            try:
                if proxy_url:
                    connector_kwargs = {
                        "timeout": aiohttp.ClientTimeout(total=timeout)
                    }
                    request_kwargs = {"proxy": proxy_url}
                    request_type = f"proxy[{attempt}]"
                else:
                    request_kwargs = {}
                    request_type = "direct"
                async with self.session.get(url, **request_kwargs) as response:
                    if response.status == 200:
                        raw_data = await response.read()
                        image = await asyncio.to_thread(Image.open, io.BytesIO(raw_data))
                        processed = await self.processor.process(image, size)
                        key_without_ext = key.rsplit(".", 1)[0] if "." in key else key
                        cache_file = self.cache_path / f"{key_without_ext}_{size[0]}x{size[1]}.png"
                        processed.save(cache_file)
                        logger.debug(f"Successfully fetched image from URL ({request_type}): {url}")
                        return processed.convert("RGBA")
                    elif response.status in {404}:
                        logger.warning(f"Image not found at URL ({request_type}): {url} (status {response.status})")
                        return None
                    else:
                        logger.warning(
                            f"Failed to fetch image from URL ({request_type}): {url} "
                            f"with status {response.status}"
                        )
                        continue
            except asyncio.TimeoutError:
                logger.warning(
                    f"Timeout fetching image from URL ({request_type}): {url} "
                    f"(attempt {attempt + 1}/{len(proxies_to_try)})"
                )
                continue
            except Exception as e:
                logger.warning(
                    f"Error fetching image from URL ({request_type}): {url} - {e} "
                    f"(attempt {attempt + 1}/{len(proxies_to_try)})"
                )
                continue

        error = AssetError(
            message=f"Failed to fetch image from URL after {len(proxies_to_try)} attempts (direct + proxies)",
            asset_name=url,
            context={
                "url": url,
                "attempts": len(proxies_to_try),
                "proxies_available": len(self.proxies) if self.proxies else 0
            }
        )
        error.log()
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