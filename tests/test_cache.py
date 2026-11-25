from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

from endfield_cards.cache import ByteLRU, DiskCache, cache_key


def test_full_url_identity_and_canonical_models() -> None:
    assert cache_key("https://a.example/path/art.png?a=1") != cache_key("https://b.example/path/art.png?a=1")
    assert cache_key("https://a.example/path/art.png?a=1") != cache_key("https://a.example/path/art.png?a=2")
    assert cache_key({"a": 1, "b": 2}) == cache_key({"b": 2, "a": 1})


@pytest.mark.asyncio
async def test_nested_missing_meter_and_supplied_zero_do_not_share_render_cache():
    from skport.games.endfield.models import FactoryState, PlayerIdentity, ResourceMeter
    from skport.games.endfield.models.world import RegionProgress

    from endfield_cards.rendering import RenderEngine

    owner = PlayerIdentity(name="Owner", game_uid="game", skport_id="social")
    missing = FactoryState(player=owner, regions=[RegionProgress(name="Region", funds=ResourceMeter())])
    observed = missing.model_copy(deep=True)
    observed.regions[0].funds = ResourceMeter(current=0, maximum=0)
    assert missing.model_dump(mode="json") == observed.model_dump(mode="json")
    assert cache_key(missing) != cache_key(observed)
    assert cache_key(observed) == cache_key(observed.model_copy(deep=True))
    async with RenderEngine() as renderer:
        unknown_page = (await renderer.render_factory(missing))[0]
        zero_page = (await renderer.render_factory(observed))[0]
        assert unknown_page.data != zero_page.data
        assert (await renderer.render_factory(observed))[0].data == zero_page.data
        assert renderer.cache_stats["renders"]["hits"] >= 1


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


@pytest.mark.asyncio
async def test_busy_atomic_replacement_is_optional_and_cleans_temporary_file(tmp_path, monkeypatch):
    disk = DiskCache(tmp_path)
    assert await disk.put("image", b"original")

    def busy_destination(source, destination):
        raise PermissionError("another process holds the cache destination open")

    monkeypatch.setattr("endfield_cards.cache.disk.os.replace", busy_destination)
    assert not await disk.put("image", b"updated")
    assert await disk.get("image") == b"original"
    assert list(tmp_path.glob(".source-*.tmp")) == []


@pytest.mark.skipif(sys.platform != "win32", reason="Windows forbids replacing an open reader's path")
@pytest.mark.asyncio
async def test_external_windows_reader_does_not_fail_a_cache_publication(tmp_path):
    disk = DiskCache(tmp_path)
    assert await disk.put("image", b"original")
    reader_code = (
        "import sys; "
        "source = open(sys.argv[1], 'rb'); "
        "print('ready', flush=True); "
        "sys.stdin.readline(); "
        "source.close()"
    )
    reader = subprocess.Popen(
        [sys.executable, "-c", reader_code, str(disk._path("image"))],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        assert reader.stdout is not None and reader.stdout.readline().strip() == "ready"
        assert not await disk.put("image", b"updated")
        assert list(tmp_path.glob(".source-*.tmp")) == []
    finally:
        reader.communicate("\n", timeout=10)
    assert reader.returncode == 0
    assert await disk.get("image") == b"original"
    assert await disk.put("image", b"updated")
    assert await disk.get("image") == b"updated"


@pytest.mark.asyncio
async def test_eviction_skips_an_entry_removed_after_enumeration(tmp_path, monkeypatch):
    disk = DiskCache(tmp_path)
    assert await disk.put("expired", b"older bytes")
    expired = disk._path("expired")
    original_stat = Path.stat
    raced = False

    def concurrent_expiry(path, *args, **kwargs):
        nonlocal raced
        if path == expired and not raced:
            raced = True
            expired.unlink()
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", concurrent_expiry)
    assert await disk.put("fresh", b"fresh bytes")
    assert raced
    assert await disk.get("fresh") == b"fresh bytes"
    assert list(tmp_path.glob(".source-*.tmp")) == []


@pytest.mark.asyncio
async def test_eviction_continues_after_a_busy_entry(tmp_path, monkeypatch):
    disk = DiskCache(tmp_path, max_bytes=2048)
    assert await disk.put("busy", b"busy bytes")
    assert await disk.put("old", b"old bytes")
    busy, old = disk._path("busy"), disk._path("old")
    os.utime(busy, (1, 1))
    os.utime(old, (2, 2))
    disk.max_bytes = busy.stat().st_size + 10
    original_unlink = Path.unlink

    def concurrent_reader(path, *args, **kwargs):
        if path == busy:
            raise PermissionError("another process is reading this entry")
        return original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", concurrent_reader)
    assert await disk.put("fresh", b"new bytes")
    assert await disk.size() <= disk.max_bytes
    assert busy.exists() and not old.exists()


@pytest.mark.asyncio
async def test_size_survives_concurrent_expiry(tmp_path, monkeypatch):
    disk = DiskCache(tmp_path)
    assert await disk.put("expired", b"older bytes")
    expired = disk._path("expired")
    original_stat = Path.stat
    raced = False

    def concurrent_expiry(path, *args, **kwargs):
        nonlocal raced
        if path == expired and not raced:
            raced = True
            expired.unlink()
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", concurrent_expiry)
    assert await disk.size() == 0
    assert raced
