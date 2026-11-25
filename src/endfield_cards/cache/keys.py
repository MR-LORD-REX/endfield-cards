"""Content-addressed keys covering all caller-supplied inputs."""

from __future__ import annotations

import dataclasses
import hashlib
import json
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any


def _field_presence(value: Any) -> Any:
    """Retain nested SDK field presence where an absent value differs from supplied zero."""
    if hasattr(value, "model_fields_set"):
        children = {
            name: presence
            for name in type(value).model_fields
            if (presence := _field_presence(getattr(value, name))) is not None
        }
        return {"supplied": sorted(value.model_fields_set), "children": children}
    if isinstance(value, dict):
        children = {
            str(key): presence
            for key, item in value.items()
            if (presence := _field_presence(item)) is not None
        }
        return children or None
    if isinstance(value, list | tuple):
        sequence = [_field_presence(item) for item in value]
        return sequence if any(item is not None for item in sequence) else None
    return None


def _normalize(value: Any) -> Any:
    if isinstance(value, bytes | bytearray | memoryview):
        return {"bytes_sha256": hashlib.sha256(value).hexdigest()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, Enum):
        return _normalize(value.value)
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {f.name: _normalize(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if hasattr(value, "model_dump"):
        return {"model": _normalize(value.model_dump(mode="json")), "presence": _field_presence(value)}
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_normalize(v) for v in value]
    if isinstance(value, set | frozenset):
        return sorted((_normalize(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise TypeError(f"unsupported cache key input: {type(value).__name__}")


def cache_key(*parts: Any) -> str:
    """Hash canonical inputs, including the entire URL rather than its filename."""
    payload = json.dumps(_normalize(parts), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
