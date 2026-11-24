"""Thread-safe, byte-bounded LRU storage with mutation isolation."""

from __future__ import annotations

import copy
import time
from collections import OrderedDict
from threading import RLock
from typing import Generic, TypeVar

from PIL import Image

T = TypeVar("T")


def _copy(value: T) -> T:
    if isinstance(value, Image.Image):
        return value.copy()  # type: ignore[return-value]
    if isinstance(value, bytes):
        return value
    return copy.deepcopy(value)


def _size(value: object) -> int:
    if isinstance(value, Image.Image):
        return value.width * value.height * len(value.getbands())
    if isinstance(value, bytes | bytearray | memoryview):
        return len(value)
    raise TypeError("provide size_bytes for non-image, non-byte cache values")


class ByteLRU(Generic[T]):
    """Store private copies; expired or oversized entries never exceed the budget."""

    def __init__(self, max_bytes: int, *, ttl_seconds: float = 3600) -> None:
        if max_bytes < 0 or ttl_seconds < 0:
            raise ValueError("cache budget and TTL must be nonnegative")
        self.max_bytes = max_bytes
        self.ttl_seconds = ttl_seconds
        self._values: OrderedDict[str, tuple[T, int, float]] = OrderedDict()
        self._bytes = 0
        self._hits = self._misses = self._evictions = 0
        self._lock = RLock()

    def get(self, key: str) -> T | None:
        """Return a caller-owned copy, or None for a missing/expired entry."""
        with self._lock:
            entry = self._values.get(key)
            if entry is None:
                self._misses += 1
                return None
            value, size, expires = entry
            if time.monotonic() >= expires:
                self._values.pop(key)
                self._bytes -= size
                self._misses += 1
                return None
            self._values.move_to_end(key)
            self._hits += 1
            return _copy(value)

    def put(self, key: str, value: T, *, size_bytes: int | None = None) -> bool:
        """Store a private copy and evict oldest values until it fits."""
        size = _size(value) if size_bytes is None else size_bytes
        if size < 0:
            raise ValueError("entry byte size must be nonnegative")
        with self._lock:
            if not self.max_bytes or not self.ttl_seconds or size > self.max_bytes:
                return False
            previous = self._values.pop(key, None)
            if previous is not None:
                self._bytes -= previous[1]
            while self._values and self._bytes + size > self.max_bytes:
                _, removed = self._values.popitem(last=False)
                self._bytes -= removed[1]
                self._evictions += 1
            self._values[key] = (_copy(value), size, time.monotonic() + self.ttl_seconds)
            self._bytes += size
            return True

    def clear(self) -> None:
        """Forget all values without changing the lifetime diagnostic counters."""
        with self._lock:
            self._values.clear()
            self._bytes = 0

    @property
    def stats(self) -> dict[str, int]:
        with self._lock:
            return {
                "entries": len(self._values),
                "bytes": self._bytes,
                "max_bytes": self.max_bytes,
                "hits": self._hits,
                "misses": self._misses,
                "evictions": self._evictions,
            }
