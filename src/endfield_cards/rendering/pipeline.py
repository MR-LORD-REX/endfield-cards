"""Lazy asset requests bridge async I/O and worker-only Pillow drawing."""

import asyncio
import logging
from concurrent.futures import CancelledError, Future
from threading import Event, RLock
from typing import Any

from PIL import Image

from endfield_cards.errors import AssetError, ResourceClosedError
from endfield_cards.models import RenderIssue

logger = logging.getLogger("endfield_cards")


class _BridgeState:
    def __init__(self) -> None:
        self.pending: set[Future[Any]] = set()
        self.lock = RLock()
        self.cancelled = Event()


class LazyAssets(dict[str, Image.Image]):
    """Request only images actually used by the current page, without retaining copies."""

    def __init__(
        self,
        store: Any,
        loop: asyncio.AbstractEventLoop,
        *,
        issues: list[RenderIssue] | None = None,
        overrides: dict[str, Image.Image] | None = None,
        state: _BridgeState | None = None,
    ) -> None:
        super().__init__(overrides or {})
        self.store, self.loop = store, loop
        self.issues = issues if issues is not None else []
        self._failed: set[str] = set()
        self._state = state or _BridgeState()

    def __bool__(self) -> bool:
        return True

    def get(self, key: Any, default: Any = None) -> Any:
        if key in self:
            return super().get(key, default)
        if not isinstance(key, str) or not key.startswith(("http://", "https://")) or key in self._failed:
            return default
        with self._state.lock:
            if self._state.cancelled.is_set():
                raise ResourceClosedError("render asset requests have been cancelled")
            future = asyncio.run_coroutine_threadsafe(self.store.get(key), self.loop)
            self._state.pending.add(future)
        try:
            return future.result()
        except CancelledError as exc:
            raise ResourceClosedError("render asset waiter has been cancelled") from exc
        except AssetError as exc:
            self._failed.add(key)
            self.issues.append(RenderIssue(exc.code, "An optional source image could not be loaded."))
            logger.debug("optional image fallback: %s", exc.code)
            return default
        finally:
            with self._state.lock:
                self._state.pending.discard(future)

    def cancel_pending(self) -> None:
        """Release only this renderer's waiters; shared source flights stay alive."""
        with self._state.lock:
            self._state.cancelled.set()
            for future in list(self._state.pending):
                future.cancel()

    def fork(self) -> "LazyAssets":
        return LazyAssets(self.store, self.loop, issues=self.issues, overrides=dict(self), state=self._state)
