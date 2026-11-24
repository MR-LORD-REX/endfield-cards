"""Translate SDK identity and source scope without owning authentication."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from endfield_cards.errors import DataValidationError, OwnerMismatchError
from endfield_cards.models import OwnerIdentity, RenderContext


def image_url(links: Any) -> str | None:
    """Return the SDK's preferred artwork candidate without guessing URLs."""
    if links is None:
        return None
    return links if isinstance(links, str) else getattr(links, "url", None)


def _identity(model: Any) -> Any:
    if isinstance(model, OwnerIdentity):
        return model
    if hasattr(model, "game_uid"):
        return model
    return getattr(model, "player", None) or getattr(model, "owner", None)


def owner_from(model: Any) -> OwnerIdentity:
    """Require a real game UID and in-game name, separate from social identity."""
    identity = _identity(model)
    if identity is None or not str(identity.game_uid or "").strip() or not str(identity.name or "").strip():
        raise DataValidationError(
            "Rendering requires the owner's in-game name and game UID", code="missing_owner"
        )
    if isinstance(identity, OwnerIdentity):
        return identity
    return OwnerIdentity(
        name=str(identity.name),
        game_uid=str(identity.game_uid),
        skport_id=str(identity.skport_id) if getattr(identity, "skport_id", None) else None,
    )


def validate_owner(model: Any, context: RenderContext) -> None:
    """Reject a mismatched owner before downloading any artwork."""
    expected = owner_from(context.owner)
    models = model if isinstance(model, Sequence) and not isinstance(model, (str, bytes)) else [model]
    for item in models:
        identity = _identity(item)
        if identity is not None:
            actual = owner_from(identity)
            if actual.game_uid != expected.game_uid:
                raise OwnerMismatchError(
                    "Model and render context have different game UIDs", code="owner_mismatch"
                )
            if actual.skport_id and expected.skport_id and actual.skport_id != expected.skport_id:
                raise OwnerMismatchError(
                    "Model and render context have different SKPort identities", code="owner_mismatch"
                )
        for character in getattr(item, "characters", ()):
            validate_owner(character, context)


def context_for(
    model: Any,
    owner: Any = None,
    *,
    locale: str = "en",
    source_scope: str | None = None,
) -> RenderContext:
    """Create validated per-call context for arbitrary profiles or supplied models."""
    context = RenderContext(
        owner=owner_from(owner if owner is not None else model),
        locale=locale,
        source_scope=str(source_scope or getattr(model, "source_scope", "public") or "public"),
        snapshot_at=getattr(model, "snapshot_at", None) or getattr(model, "server_time", None),
    )
    validate_owner(model, context)
    return context
