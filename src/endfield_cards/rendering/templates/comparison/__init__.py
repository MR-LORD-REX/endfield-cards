"""Layouts for comparison mode; showcase style names remain compatible."""

from typing import Any

from endfield_cards.errors import UnsupportedVariantError
from endfield_cards.utils.drawing import PageCanvas


def render_canvas(
    first: Any, second: Any, context: Any, second_context: Any, *, variant: str = "field", **options: Any
) -> PageCanvas:
    if variant in {"field", "terminal"}:
        from .field import render
    elif variant in {"dossier", "portrait"}:
        from .dossier import render
    else:
        raise UnsupportedVariantError(f"unknown comparison variant {variant!r}")
    return render(first, second, context, second_context, **options)
