"""Bounded image decoding and normalized caller-owned artwork."""

from __future__ import annotations

import io
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from endfield_cards.errors import ImageDecodeError


def decode_image(data: bytes, *, max_bytes: int = 12582912, max_pixels: int = 24000000) -> Image.Image:
    """Decode one image frame with EXIF orientation, rejecting excessive inputs."""
    if not data or len(data) > max_bytes:
        raise ImageDecodeError("image source is empty or exceeds the byte limit")
    try:
        with Image.open(io.BytesIO(data)) as original:
            if original.width * original.height > max_pixels:
                raise ImageDecodeError("image exceeds the decoded pixel limit")
            original.load()
            return ImageOps.exif_transpose(original).convert("RGBA")
    except ImageDecodeError:
        raise
    except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise ImageDecodeError("image source could not be decoded") from exc


def load_local(
    source: Image.Image | bytes | bytearray | str | Path,
    *,
    max_bytes: int = 12582912,
    max_pixels: int = 24000000,
) -> Image.Image:
    """Read local artwork in a worker; never mutate or return caller image pixels."""
    if isinstance(source, Image.Image):
        if source.width * source.height > max_pixels:
            raise ImageDecodeError("image exceeds the decoded pixel limit")
        return ImageOps.exif_transpose(source.copy()).convert("RGBA")
    if isinstance(source, bytes | bytearray):
        return decode_image(bytes(source), max_bytes=max_bytes, max_pixels=max_pixels)
    try:
        with Path(source).open("rb") as stream:
            data = stream.read(max_bytes + 1)
    except (OSError, TypeError, ValueError) as exc:
        raise ImageDecodeError("local artwork could not be read") from exc
    return decode_image(data, max_bytes=max_bytes, max_pixels=max_pixels)
