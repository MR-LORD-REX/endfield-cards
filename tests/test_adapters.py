"""Identity boundaries apply to every call and every character in a roster."""

import pytest
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    PlayerCard,
    PlayerIdentity,
    WikiPage,
    WikiSummary,
)

from endfield_cards.adapters.skport import context_for, owner_from, validate_owner
from endfield_cards.errors import DataValidationError, OwnerMismatchError
from endfield_cards.models import OwnerIdentity, RenderContext


def test_social_id_cannot_replace_missing_game_uid():
    with pytest.raises(DataValidationError, match="game UID"):
        owner_from(PlayerIdentity(skport_id="social-only", name="Owner"))


def test_context_tracks_model_scope_without_conflating_roster_counts():
    model = PlayerCard(
        player=PlayerIdentity(skport_id="s1", game_uid="g1", name="One"), source_scope="public"
    )
    context = context_for(model)
    assert context.owner.game_uid == "g1"
    assert context.source_scope == "public"
    assert context_for(model, source_scope="owner").source_scope == "owner"


def test_mixed_owner_roster_rejected():
    context = RenderContext(OwnerIdentity("One", "g1", "s1"))
    builds = [
        CharacterBuild(
            identity=CharacterIdentity(skport_id="c1"),
            owner=PlayerIdentity(skport_id="s2", game_uid="g2", name="Two"),
        )
    ]
    with pytest.raises(OwnerMismatchError):
        validate_owner(builds, context)


def test_rendering_context_does_not_bind_subsequent_owner():
    a = PlayerIdentity(skport_id="s1", game_uid="g1", name="One")
    b = PlayerIdentity(skport_id="s2", game_uid="g2", name="Two")
    assert context_for(a).owner != context_for(b).owner


def test_wiki_requires_explicit_owner_context():
    page = WikiPage(summary=WikiSummary(id="article", name="Reference"))
    with pytest.raises(DataValidationError):
        context_for(page)
    assert context_for(page, OwnerIdentity("One", "g1"), source_scope="supplied").source_scope == "supplied"
