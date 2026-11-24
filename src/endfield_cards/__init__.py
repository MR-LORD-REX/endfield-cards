"""Endfield cards 2: no network calls, directories or handlers at import time."""

from endfield_cards._version import __version__
from endfield_cards.client import TEMPLATES, Cards, EFCard
from endfield_cards.config import CacheConfig, CardsConfig, DownloadConfig, Locale, OutputConfig, OutputFormat
from endfield_cards.errors import CardError
from endfield_cards.models import (
    Artwork,
    BatchItem,
    CardResult,
    CharacterListInfo,
    CharacterSelection,
    ContractInfo,
    ContractSelection,
    LiveInfo,
    MeterInfo,
    MonumentEventInfo,
    MonumentInfo,
    OwnerIdentity,
    RenderContext,
    RenderedCard,
    RenderInfo,
    RenderIssue,
    RenderRequest,
    StageSelection,
)

VARIANTS = TEMPLATES

__all__ = [
    "Artwork",
    "BatchItem",
    "CacheConfig",
    "CardError",
    "CardResult",
    "CharacterListInfo",
    "CharacterSelection",
    "ContractInfo",
    "ContractSelection",
    "LiveInfo",
    "Locale",
    "MeterInfo",
    "MonumentEventInfo",
    "MonumentInfo",
    "Cards",
    "CardsConfig",
    "DownloadConfig",
    "EFCard",
    "OutputConfig",
    "OutputFormat",
    "OwnerIdentity",
    "RenderContext",
    "RenderIssue",
    "RenderedCard",
    "RenderInfo",
    "RenderRequest",
    "StageSelection",
    "TEMPLATES",
    "VARIANTS",
    "__version__",
]
