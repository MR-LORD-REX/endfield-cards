"""Own worker threads and retain admission until cancelled work has stopped."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any

from endfield_cards.errors import ResourceClosedError


class RenderExecutor:
    def __init__(self, workers: int = 2) -> None:
        self._workers = workers
        self._pool: ThreadPoolExecutor | None = None
        self._slots = asyncio.Semaphore(workers)
        self._closed = False

    async def run(self, function: Any, *args: Any, on_cancel: Any = None, **kwargs: Any) -> Any:
        if self._closed:
            raise ResourceClosedError("render executor is closed")
        async with self._slots:
            if self._closed:
                raise ResourceClosedError("render executor is closed")
            if self._pool is None:
                self._pool = ThreadPoolExecutor(
                    max_workers=self._workers, thread_name_prefix="endfield-cards"
                )
            future = asyncio.get_running_loop().run_in_executor(
                self._pool, partial(function, *args, **kwargs)
            )
            try:
                return await asyncio.shield(future)
            except asyncio.CancelledError:
                if on_cancel is not None:
                    on_cancel()
                try:
                    await future
                except Exception:
                    pass
                raise

    async def aclose(self) -> None:
        self._closed = True
        if self._pool is not None:
            pool, self._pool = self._pool, None
            await asyncio.to_thread(pool.shutdown, wait=True, cancel_futures=True)
