"""
Decoder for Enka Network's reference-index compressed __data.json format.

The API returns a flat array where every integer VALUE inside dicts and lists
is an index back into that same array — effectively a shared-reference DAG.
Primitive leaves (str, bool, float, int at a leaf position) are actual data.

Example:
    data[0] = {"playerInfo": 1, "uid": 14}
    data[1] = {"businessCard": 2, "charData": 76}
    data[14] = "4225399080"
    →  decoded[0] = {"playerInfo": {"businessCard": ..., "charData": ...}, "uid": "4225399080"}
"""

from __future__ import annotations
from typing import Any

from .errors import DecodeError


class DataDecoder:
    """
    Decodes the reference-index __data.json returned by the Enka Network API.

    Usage::

        decoder = DataDecoder(raw_json)
        decoded = decoder.decode()   # → fully resolved dict starting at data[0]
    """

    def __init__(self, raw: dict) -> None:
        try:
            # The payload is:  { "type": "data", "nodes": [ skip, { "data": [...] } ] }
            self._data: list[Any] = raw["nodes"][1]["data"]
        except (KeyError, IndexError, TypeError) as exc:
            raise DecodeError(
                f"Unexpected API response shape — could not locate nodes[1].data: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def decode(self) -> dict:
        """
        Return the fully resolved document starting from data[0].
        data[0] is always the root object containing playerInfo and uid.
        """
        try:
            return self._resolve(self._data[0])
        except RecursionError as exc:
            raise DecodeError("Circular reference detected in data array") from exc
        except (IndexError, KeyError, TypeError) as exc:
            raise DecodeError(f"Failed to resolve data array: {exc}") from exc

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _resolve(self, node: Any) -> Any:
        """
        Recursively resolve a node:
        - dict  → resolve each VALUE as an index into self._data
        - list  → resolve each integer ELEMENT as an index; pass-through others
        - other → return as-is (actual primitive data)
        """
        if isinstance(node, dict):
            return {key: self._resolve(self._data[idx]) for key, idx in node.items()}

        if isinstance(node, list):
            result = []
            for item in node:
                if isinstance(item, int):
                    result.append(self._resolve(self._data[item]))
                else:
                    # Non-integer list elements are direct values (defensive)
                    result.append(self._resolve(item))
            return result

        # Primitive leaf — actual data value (str / bool / int / float / None)
        return node
