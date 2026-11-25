"""Checksummed source-byte cache using atomic, Windows-compatible replacement."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from threading import RLock

from endfield_cards.cache.keys import cache_key


class _DirectoryState:
    def __init__(self) -> None:
        self.lock = RLock()
        self.generation = 0


_DIRECTORY_STATES: dict[str, _DirectoryState] = {}
_DIRECTORY_LOCKS_GUARD = RLock()


def _directory_state(directory: Path) -> _DirectoryState:
    key = os.path.normcase(os.path.abspath(directory))
    with _DIRECTORY_LOCKS_GUARD:
        return _DIRECTORY_STATES.setdefault(key, _DirectoryState())


def default_cache_directory() -> Path:
    """Resolve a user cache path without creating directories on import."""
    cwd=Path.cwd()
    cache_path= cwd / ".cache" / "endfield-cards" / "images"
    os.makedirs(cache_path,exist_ok=True)
    return cache_path


class DiskCache:
    """Persist bounded source bytes; never trust an incomplete or modified file."""

    def __init__(
        self, directory: str | Path | None = None, *, max_bytes: int = 536870912, ttl_seconds: float = 3600
    ) -> None:
        if max_bytes < 0 or ttl_seconds < 0:
            raise ValueError("cache budget and TTL must be nonnegative")
        self.directory = Path(directory) if directory is not None else default_cache_directory()
        self.max_bytes = max_bytes
        self.ttl_seconds = ttl_seconds
        self._state = _directory_state(self.directory)
        self._lock = self._state.lock

    @property
    def generation(self) -> int:
        with self._lock:
            return self._state.generation

    def _path(self, key: str) -> Path:
        return self.directory / (cache_key("disk-source-v1", key) + ".cache")

    async def get(self, key: str, *, max_bytes: int | None = None) -> bytes | None:
        return await asyncio.to_thread(self._get, key, max_bytes)

    def _get(self, key: str, max_bytes: int | None) -> bytes | None:
        with self._lock:
            path = self._path(key)
            limit = self.max_bytes if max_bytes is None else min(max_bytes, self.max_bytes)
            try:
                if not self.max_bytes or not self.ttl_seconds or path.stat().st_size > self.max_bytes:
                    return None
                with path.open("rb") as source:
                    line = source.readline(1024)
                    metadata = json.loads(line)
                    if not isinstance(metadata.get("bytes"), int) or metadata["bytes"] > limit:
                        raise ValueError("cached source exceeds the admission limit")
                    data = source.read(limit + 1)
                if (
                    metadata.get("version") != 1
                    or metadata.get("key") != key
                    or len(data) != metadata.get("bytes")
                    or len(data) > limit
                    or time.time() >= metadata.get("expires_at", 0)
                    or hashlib.sha256(data).hexdigest() != metadata.get("sha256")
                ):
                    path.unlink(missing_ok=True)
                    return None
                os.utime(path, None)
                return data
            except FileNotFoundError:
                return None
            except (OSError, ValueError, TypeError, AttributeError):
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
                return None

    async def put(self, key: str, data: bytes, *, generation: int | None = None) -> bool:
        """Publish when possible; optional persistence must not break a valid download."""
        return await asyncio.to_thread(self._put, key, data, generation)

    def _put(self, key: str, data: bytes, generation: int | None) -> bool:
        metadata = {
            "version": 1,
            "key": key,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "expires_at": time.time() + self.ttl_seconds,
        }
        header = json.dumps(metadata, separators=(",", ":")).encode("utf-8") + b"\n"
        if not self.max_bytes or not self.ttl_seconds or len(data) + len(header) > self.max_bytes:
            return False
        with self._lock:
            if generation is not None and generation != self._state.generation:
                return False
            temporary: str | None = None
            try:
                self.directory.mkdir(parents=True, exist_ok=True)
                descriptor, temporary = tempfile.mkstemp(prefix=".source-", suffix=".tmp", dir=self.directory)
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(header)
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, self._path(key))
                temporary = None
                self._trim()
                return True
            except OSError:
                # Another process may hold the destination open on Windows or
                # remove an entry during eviction. Its lock is independent of
                # this process's lock; keep the caller's downloaded bytes usable.
                return False
            finally:
                if temporary is not None:
                    try:
                        Path(temporary).unlink(missing_ok=True)
                    except OSError:
                        pass

    def _trim(self) -> None:
        entries = []
        for path in self.directory.glob("*.cache"):
            try:
                metadata = path.stat()
            except OSError:
                # Expired reads and evictions in other processes can remove a
                # path between enumeration and stat. Snapshot each path once.
                continue
            entries.append((path, metadata.st_size, metadata.st_mtime))
        entries.sort(key=lambda entry: entry[2])
        total = sum(size for _, size, _ in entries)
        for path, size, _ in entries:
            if total <= self.max_bytes:
                break
            try:
                path.unlink(missing_ok=True)
            except OSError:
                # Skip a busy reader and keep trying other eviction candidates.
                continue
            total -= size

    async def clear(self) -> None:
        await asyncio.to_thread(self._clear)

    def _clear(self) -> None:
        with self._lock:
            self._state.generation += 1
            if self.directory.exists():
                for path in self.directory.glob("*.cache"):
                    path.unlink(missing_ok=True)

    async def size(self) -> int:
        return await asyncio.to_thread(self._size)

    def _size(self) -> int:
        with self._lock:
            if not self.directory.exists():
                return 0
            total = 0
            for path in self.directory.glob("*.cache"):
                try:
                    total += path.stat().st_size
                except OSError:
                    continue
            return total
