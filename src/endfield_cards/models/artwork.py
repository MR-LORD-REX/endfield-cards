"""Custom artwork crop and retention policy."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PIL import Image


@dataclass(frozen=True)
class Artwork:
    source: str | Path | bytes | Image.Image
    fit: Literal["cover", "contain"] = "cover"
    focal_point: tuple[float, float] = (0.5, 0.35)
    allow_remote: bool = False
    retain: bool = False

    def __post_init__(self) -> None:
        if self.fit not in {"cover", "contain"}:
            raise ValueError("artwork fit must be cover or contain")
        if len(self.focal_point) != 2 or any(not 0 <= x <= 1 for x in self.focal_point):
            raise ValueError("focal point must contain two coordinates between zero and one")
