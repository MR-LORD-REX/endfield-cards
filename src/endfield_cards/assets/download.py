"""Reusable async HTTP transport with bounded responses and redirect policy."""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Awaitable, Callable
from urllib.parse import urljoin, urlsplit

import aiohttp

from endfield_cards.config import DownloadConfig
from endfield_cards.errors import DownloadError, ResourceClosedError

URLPolicy = Callable[[str], bool | Awaitable[bool]]


class Downloader:
    """Own a lazily created session, or borrow one without closing it."""

    def __init__(
        self,
        config: DownloadConfig | None = None,
        *,
        session: aiohttp.ClientSession | None = None,
        url_policy: URLPolicy | None = None,
    ) -> None:
        self.config = config or DownloadConfig()
        self._session = session
        self._owned = session is None
        self._closed = False
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(self.config.concurrency)
        self.url_policy = url_policy

    async def _check_url(self, url: str) -> None:
        try:
            parsed = urlsplit(url)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username
                or parsed.password
            ):
                raise DownloadError("image URL must be HTTP(S) without embedded credentials")
            if self.url_policy is not None:
                accepted = self.url_policy(url)
                if inspect.isawaitable(accepted):
                    accepted = await accepted
                if not accepted:
                    raise DownloadError("image URL was rejected by the destination policy")
        except ValueError as exc:
            raise DownloadError("image URL is invalid") from exc

    async def _get_session(self) -> aiohttp.ClientSession:
        async with self._lock:
            if self._closed:
                raise ResourceClosedError("image downloader is closed")
            if self._session is None:
                self._session = aiohttp.ClientSession(headers={"User-Agent": "endfield-cards/2"})
            if self._session.closed:
                raise ResourceClosedError("the borrowed HTTP session is closed")
            return self._session

    async def fetch(self, url: str) -> bytes:
        """Validate every redirect and stop streaming at the configured byte limit."""
        if self._closed:
            raise ResourceClosedError("image downloader is closed")
        await self._check_url(url)
        async with self._semaphore:
            session = await self._get_session()
            current = url
            try:
                for redirect in range(self.config.max_redirects + 1):
                    async with session.get(
                        current,
                        allow_redirects=False,
                        timeout=aiohttp.ClientTimeout(total=self.config.timeout_seconds),
                    ) as response:
                        if response.status in {301, 302, 303, 307, 308}:
                            target = response.headers.get("Location")
                            if not target or redirect == self.config.max_redirects:
                                raise DownloadError("image response exceeds the redirect limit")
                            current = urljoin(current, target)
                            await self._check_url(current)
                            continue
                        if response.status != 200:
                            raise DownloadError(f"image request returned HTTP {response.status}")
                        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
                        if content_type and not (
                            content_type.startswith("image/") or content_type == "application/octet-stream"
                        ):
                            raise DownloadError("image response has an unsupported content type")
                        if (
                            response.content_length is not None
                            and response.content_length > self.config.max_bytes
                        ):
                            raise DownloadError("image response exceeds the source byte limit")
                        output = bytearray()
                        async for chunk in response.content.iter_chunked(65536):
                            output.extend(chunk)
                            if len(output) > self.config.max_bytes:
                                raise DownloadError("image response exceeds the source byte limit")
                        if not output:
                            raise DownloadError("image response is empty")
                        return bytes(output)
            except (TimeoutError, aiohttp.ClientError, OSError) as exc:
                raise DownloadError("image request failed or timed out") from exc
        raise DownloadError("image response exceeds the redirect limit")

    async def aclose(self) -> None:
        """Idempotently close only an owned session."""
        async with self._lock:
            self._closed = True
            if self._owned and self._session is not None and not self._session.closed:
                await self._session.close()
