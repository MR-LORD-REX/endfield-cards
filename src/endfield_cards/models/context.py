"""Per-request identity and locale; never shared account state."""

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from endfield_cards.errors import DataValidationError
from endfield_cards.i18n import normalize_locale
from endfield_cards.models.identity import OwnerIdentity


@dataclass(frozen=True)
class RenderContext:
    owner: OwnerIdentity
    locale: str = "en"
    source_scope: str = "public"
    snapshot_at: datetime | None = None
    display_timezone: str = "UTC"
    comparison_owner: OwnerIdentity | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.owner, OwnerIdentity):
            raise DataValidationError("RenderContext requires an OwnerIdentity", code="missing_owner")
        if self.comparison_owner is not None and not isinstance(self.comparison_owner, OwnerIdentity):
            raise DataValidationError("comparison_owner must be an OwnerIdentity")
        object.__setattr__(self, "locale", normalize_locale(self.locale))
        ZoneInfo(self.display_timezone)
        if self.source_scope not in {"public", "owner", "supplied"}:
            raise ValueError("source_scope must be public, owner or supplied")
