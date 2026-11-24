"""Output budgets are enforced without silently discarding content."""

import io

from PIL import Image

from endfield_cards.config import OutputConfig
from endfield_cards.errors import EncodingError


def encode(image: Image.Image, output: OutputConfig) -> bytes:
    stream = io.BytesIO()
    pixels = image.convert("RGB") if output.format == "JPEG" else image
    options = {"quality": output.quality} if output.format in {"JPEG", "WEBP"} else {}
    try:
        pixels.save(stream, format=output.format, **options)
    except (OSError, ValueError) as exc:
        raise EncodingError("the card could not be encoded") from exc
    data = stream.getvalue()
    if output.max_bytes is not None and len(data) > output.max_bytes:
        raise EncodingError(
            "encoded card exceeds max_bytes; choose JPEG/WEBP or raise the output budget",
            code="output_budget_exceeded",
        )
    return data
