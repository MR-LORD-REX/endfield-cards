"""Warm light comparison with separate owner/art headers and dark weapon bands."""

from typing import Any

from endfield_cards.utils.drawing import PageCanvas

from ._shared import render_layout


def render(first: Any, second: Any, context: Any, second_context: Any, **options: Any) -> PageCanvas:
    return render_layout(first, second, context, second_context, dark=False, **options)
