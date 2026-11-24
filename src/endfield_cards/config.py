"""Immutable budgets; constructing configuration performs no I/O."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class CacheConfig:
    enabled: bool = True
    decoded_bytes: int = 128 * 1024 * 1024
    encoded_bytes: int = 32 * 1024 * 1024
    disk_bytes: int = 512 * 1024 * 1024
    ttl_seconds: float = 3600
    directory: Path | None = None

    def __post_init__(self) -> None:
        if min(self.decoded_bytes, self.encoded_bytes, self.disk_bytes, self.ttl_seconds) < 0:
            raise ValueError("cache budgets and TTL must be nonnegative")
        if self.directory is not None:
            object.__setattr__(self, "directory", Path(self.directory))


@dataclass(frozen=True)
class DownloadConfig:
    concurrency: int = 8
    timeout_seconds: float = 20
    max_bytes: int = 12 * 1024 * 1024
    max_pixels: int = 24_000_000
    max_redirects: int = 3

    def __post_init__(self) -> None:
        if min(self.concurrency, self.timeout_seconds, self.max_bytes, self.max_pixels) <= 0:
            raise ValueError("download limits must be positive")
        if self.max_redirects < 0:
            raise ValueError("max_redirects must be nonnegative")


@dataclass(frozen=True)
class OutputConfig:
    format: str = "PNG"
    quality: int = 90
    max_bytes: int | None = None

    def __post_init__(self) -> None:
        normalized = self.format.upper().replace("JPG", "JPEG")
        if normalized not in {"PNG", "JPEG", "WEBP"}:
            raise ValueError("output format must be PNG, JPEG or WEBP")
        if not 1 <= self.quality <= 100:
            raise ValueError("quality must be between 1 and 100")
        if self.max_bytes is not None and self.max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        object.__setattr__(self, "format", normalized)


@dataclass(frozen=True)
class CardsConfig:
    cache: CacheConfig = field(default_factory=CacheConfig)
    download: DownloadConfig = field(default_factory=DownloadConfig)
    render_workers: int = 2
    admitted_jobs: int = 8
    locale: str = "en"

    def __post_init__(self) -> None:
        if min(self.render_workers, self.admitted_jobs) <= 0:
            raise ValueError("render budgets must be positive")
