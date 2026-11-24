"""Immutable encoded results and explicit atomic file output."""

import io
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from endfield_cards.errors import CardError
from endfield_cards.models.context import RenderContext


@dataclass(frozen=True)
class RenderIssue:
    code: str
    message: str


@dataclass(frozen=True)
class CardResult:
    data: bytes
    format: str
    width: int
    height: int
    family: str
    variant: str
    page: int = 1
    pages: int = 1
    issues: tuple[RenderIssue, ...] = ()

    def to_pillow(self) -> Image.Image:
        """Decode fresh pixels; mutations cannot alter cached results."""
        with Image.open(io.BytesIO(self.data)) as image:
            return image.convert("RGBA")

    def save(self, path: str | Path) -> Path:
        """Write exactly these bytes through an atomic replacement."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(self.data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, target)
        finally:
            Path(temporary).unlink(missing_ok=True)
        return target


@dataclass(frozen=True)
class RenderRequest:
    family: str
    model: object
    context: RenderContext | None = None
    variant: str | None = None


@dataclass(frozen=True)
class BatchItem:
    index: int
    results: tuple[CardResult, ...] = ()
    error: CardError | None = None
