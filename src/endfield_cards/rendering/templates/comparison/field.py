"""Dark comparison with a blended scene, open owner headers and aligned data rails."""

from typing import Any

from endfield_cards.utils.drawing import PageCanvas

from ._shared import render_layout


def render(first: Any, second: Any, context: Any, second_context: Any, **options: Any) -> PageCanvas:
    return render_layout(first, second, context, second_context, dark=True, **options)
