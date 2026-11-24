from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from endfield_cards.cache import ByteLRU, DiskCache, cache_key


def test_full_url_identity_and_canonical_models() -> None:
    assert cache_key("https://a.example/path/art.png?a=1") != cache_key("https://b.example/path/art.png?a=1")
    assert cache_key("https://a.example/path/art.png?a=1") != cache_key("https://a.example/path/art.png?a=2")
    assert cache_key({"a": 1, "b": 2}) == cache_key({"b": 2, "a": 1})


def test_memory_budget_lru_and_mutation_isolation() -> None:
    memory: ByteLRU[Image.Image] = ByteLRU(32)
    image = Image.new("RGBA", (2, 2), "red")
    assert memory.put("one", image)
    image.putpixel((0, 0), (0, 0, 0, 0))
    hit = memory.get("one")
    assert hit is not None and hit.getpixel((0, 0)) == (255, 0, 0, 255)
    hit.putpixel((0, 0), (0, 0, 0, 0))
    assert memory.get("one").getpixel((0, 0)) == (255, 0, 0, 255)
    memory.put("two", image)
    memory.get("one")
    memory.put("three", image)
    assert memory.get("two") is None
    assert memory.stats["bytes"] == 32
    assert not memory.put("oversized", Image.new("RGBA", (3, 3)))
    assert memory.stats["bytes"] == 32


def test_memory_ttl_and_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [100.0]
    monkeypatch.setattr("endfield_cards.cache.memory.time.monotonic", lambda: now[0])
    memory: ByteLRU[bytes] = ByteLRU(8, ttl_seconds=2)
    memory.put("entry", b"bytes")
    now[0] = 102.0
    assert memory.get("entry") is None
    assert memory.stats["bytes"] == 0
    assert not ByteLRU(0).put("off", b"bytes")


@pytest.mark.asyncio
async def test_disk_checksum_corruption_expiry_and_generation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    directory = tmp_path / "lazy"
    now = [100.0]
    monkeypatch.setattr("endfield_cards.cache.disk.time.time", lambda: now[0])
    disk = DiskCache(directory, max_bytes=1024, ttl_seconds=5)
    assert not directory.exists()
    generation = disk.generation
    assert await disk.put("source", b"valid", generation=generation)
    assert await disk.get("source") == b"valid"
    file = next(directory.glob("*.cache"))
    file.write_bytes(file.read_bytes()[:-1] + b"X")
    assert await disk.get("source") is None
    assert not file.exists()
    await disk.put("source", b"valid")
    now[0] = 106.0
    assert await disk.get("source") is None
    await disk.clear()
    assert not await disk.put("stale", b"late-result", generation=generation)
    assert await disk.size() == 0


@pytest.mark.asyncio
async def test_disk_byte_bound_and_cache_off(tmp_path: Path) -> None:
    disk = DiskCache(tmp_path / "bounded", max_bytes=600)
    for number in range(5):
        await disk.put(str(number), b"x" * 64)
    assert await disk.size() <= 600
    off = DiskCache(tmp_path / "off", max_bytes=0)
    assert not await off.put("source", b"data")
    assert await off.get("source") is None
    assert not off.directory.exists()


@pytest.mark.asyncio
async def test_shared_disk_clients_do_not_republish_after_clear(tmp_path: Path) -> None:
    first = DiskCache(tmp_path)
    second = DiskCache(tmp_path)
    generation = first.generation
    await second.clear()
    assert first.generation == second.generation
    assert not await first.put("stale", b"before-clear", generation=generation)
    assert await first.get("stale") is None
