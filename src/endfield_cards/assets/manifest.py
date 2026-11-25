"""Semantic access to bundled resources with lazy integrity verification."""

from __future__ import annotations

import hashlib
import json
from contextlib import ExitStack
from importlib.resources import as_file, files
from pathlib import Path, PurePosixPath
from threading import RLock
from types import MappingProxyType
from typing import Any

from endfield_cards.errors import AssetError


class Manifest:
    """Resolve installed assets by semantic key; never use source checkout paths."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = (
            root.resolve() if root is not None else files("endfield_cards").joinpath("assets/resources")
        )
        self._contexts = ExitStack()
        self._lock = RLock()
        self._extracted: dict[str, Path] = {}
        self._verified: dict[str, tuple[int, int]] = {}
        try:
            document = json.loads(self._root.joinpath("manifest.json").read_text(encoding="utf-8"))
            if document["schema_version"] != 1:
                raise ValueError("Unknown manifest schema")
            assets = document["assets"]
            aliases = document.get("aliases", {})
            entries = {key: MappingProxyType(dict(value)) for key, value in assets.items()}
            for key, target in aliases.items():
                entries[key] = entries[target]
            self.entries = MappingProxyType(entries)
            self.aliases = MappingProxyType(dict(aliases))
            self.keys = tuple(assets)
            self.watermark = document["watermark"]
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise AssetError(
                "The installed asset manifest is invalid", code="asset_manifest_invalid"
            ) from exc

    def path(self, key: str) -> Path:
        """Return a verified resource path, including wheels installed outside this checkout."""
        with self._lock:
            try:
                metadata = self.entries[key]
            except KeyError as exc:
                raise AssetError(f"No bundled asset for {key!r}", code="asset_not_found") from exc
            relative = PurePosixPath(metadata["path"])
            if relative.is_absolute() or ".." in relative.parts or "\\" in str(relative):
                raise AssetError("Resource path escapes the installed manifest", code="asset_path_invalid")
            canonical = self.aliases.get(key, key)
            path = self._extracted.get(canonical)
            if path is None:
                resource = self._root.joinpath(*relative.parts)
                path = (
                    resource
                    if isinstance(resource, Path)
                    else self._contexts.enter_context(as_file(resource))
                )
                self._extracted[canonical] = path
            try:
                if isinstance(self._root, Path) and not path.resolve().is_relative_to(self._root.resolve()):
                    raise AssetError("Resource path escapes the installed package", code="asset_path_invalid")
                stat = path.stat()
                signature = (stat.st_mtime_ns, stat.st_size)
                if self._verified.get(canonical) != signature:
                    data = path.read_bytes()
                    if (
                        len(data) != metadata["bytes"]
                        or hashlib.sha256(data).hexdigest() != metadata["sha256"]
                    ):
                        raise AssetError(
                            "Bundled resource failed integrity verification", code="asset_integrity"
                        )
                    self._verified[canonical] = signature
                return path
            except OSError as exc:
                raise AssetError("Bundled resource cannot be read", code="asset_read_failed") from exc

    def close(self) -> None:
        """Release temporary extraction contexts for zip-backed installations."""
        with self._lock:
            self._contexts.close()
            self._extracted.clear()
            self._verified.clear()

    def __enter__(self) -> Manifest:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


_default: Manifest | None = None
_default_lock = RLock()


def resource_path(key: str) -> Path:
    """Resolve a package symbol lazily without creating import-time side effects."""
    global _default
    with _default_lock:
        if _default is None:
            _default = Manifest()
        return _default.path(key)
