"""Compatibility entry points for comparison mode of character cards."""

from endfield_cards.rendering.templates.character.compare import (
    iter_render,
    render,
    validate_pair,
)

__all__ = ["validate_pair", "iter_render", "render"]
