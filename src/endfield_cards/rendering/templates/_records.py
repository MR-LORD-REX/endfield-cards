"""Measured text flow and bounded panels shared by informational cards."""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from PIL import Image, ImageOps

from endfield_cards.adapters.skport import image_url
from endfield_cards.assets.fonts import FontManager
from endfield_cards.rendering.components import PageCanvas

_fonts = FontManager()
SIGNAL = "#FFC800"


def stamp(value: datetime | None) -> str:
    """Keep the source date and timezone rather than the host timezone."""
    return value.isoformat(sep=" ", timespec="minutes") if value else "Not supplied"


def number(value: Any) -> str:
    if value is None:
        return "—"
    return f"{value:,.0f}" if isinstance(value, (int, float)) and float(value).is_integer() else str(value)


def meter_text(meter: Any) -> str:
    return f"{number(meter.current)} / {number(meter.maximum)}"


def duration(value: float | None) -> str:
    if value is None:
        return "Not supplied"
    minutes, seconds = divmod(value, 60)
    return f"{int(minutes):02d}:{seconds:05.2f}"


def text_lines(value: Any, width: int, *, locale: str = "en", size: int = 24) -> list[str]:
    """Wrap on measured glyph width, retaining all text including long CJK lines."""
    plain = re.sub(r"<[^>]*>", "", str(value or ""))
    font = _fonts.get(size, locale=locale, text=plain)
    result: list[str] = []
    for paragraph in plain.splitlines() or [""]:
        if not paragraph:
            result.append("")
            continue
        line = ""
        for char in paragraph:
            candidate = line + char
            if line and font.getlength(candidate) > width:
                space = line.rfind(" ")
                if space > len(line) // 2:
                    result.append(line[:space])
                    line = line[space + 1 :] + char
                else:
                    result.append(line)
                    line = char
            else:
                line = candidate
        result.append(line)
    return result


def fit_label(
    value: Any, width: int, *, locale: str = "en", size: int = 29, max_lines: int = 2, minimum: int = 18
) -> tuple[str, int, bool]:
    """Fit a tile label; callers preserve shortened source text in detail records."""
    lines = text_lines(value, width, locale=locale, size=size)
    while size > minimum and len(lines) > max_lines:
        size -= 1
        lines = text_lines(value, width, locale=locale, size=size)
    shortened = len(lines) > max_lines
    if shortened:
        lines = lines[:max_lines]
        font = _fonts.get(size, locale=locale, text=str(value))
        while lines[-1] and font.getlength(lines[-1] + "…") > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"
    return "\n".join(lines), size, shortened


def photo(
    canvas: PageCanvas,
    url: str | None,
    box: tuple[int, int, int, int],
    assets: dict | None,
    *,
    contain: bool = False,
) -> bool:
    image = assets.get(url) if assets is not None else None
    if image is None:
        return False
    x, y, right, bottom = box
    target = (right - x, bottom - y)
    fitted = (
        ImageOps.contain(image.convert("RGBA"), target)
        if contain
        else ImageOps.fit(image.convert("RGBA"), target, centering=(0.5, 0.3))
    )
    if contain:
        x += (target[0] - fitted.width) // 2
        y += (target[1] - fitted.height) // 2
    canvas.image.alpha_composite(fitted, (x, y))
    return True


def progress(canvas: PageCanvas, ratio: float, x: int, y: int, width: int, height: int = 12) -> None:
    canvas.draw.rounded_rectangle((x, y, x + width, y + height), radius=height // 2, fill="#4B4D53")
    filled = int(width * min(1.0, max(0.0, ratio)))
    if filled:
        canvas.draw.rounded_rectangle((x, y, x + filled, y + height), radius=height // 2, fill=SIGNAL)


@dataclass
class Record:
    """One section whose contents can continue on subsequent bounded pages."""

    title: str
    lines: list[str] = field(default_factory=list)
    icon: str | None = None
    images: list[tuple[str | None, str]] = field(default_factory=list)


def record_urls(records: list[Record]) -> set[str]:
    return {url for record in records for url, _ in record.images if url}


def plan_records(
    context: Any,
    records: list[Record],
    *,
    size: tuple[int, int] = (1600, 1100),
    columns: int = 2,
) -> list[list[Any]]:
    """Plan lightweight page blocks without allocating any decoded page image."""
    width, height = size
    gap, pad, top, limit = 24, 56, 180, height - 104
    column_width = (width - 2 * pad - gap * (columns - 1)) // columns
    line_height = 32
    max_lines = max(1, (limit - top - 136) // line_height)
    prepared = []
    for record in records:
        full_title = text_lines(record.title or "Record", column_width - 90, locale=context.locale, size=29)
        title_lines = full_title[:2]
        body = [
            part
            for line in record.lines
            for part in text_lines(line, column_width - 48, locale=context.locale)
        ]
        if len(full_title) > 2:
            body = full_title[2:] + body
        header_height = 30 * len(title_lines) + 28
        capacity = max(
            1,
            min(max_lines, (limit - top - header_height - (130 if record.images else 0) - 30) // line_height),
        )
        chunks = [body[i : i + capacity] for i in range(0, len(body), capacity)] or [[]]
        for index, chunk in enumerate(chunks):
            images = record.images if index == 0 else []
            prepared.append((record, title_lines, chunk, images, index > 0))
    if not prepared:
        prepared = [
            (
                Record("No records supplied"),
                ["No records supplied"],
                ["This snapshot does not contain this section."],
                [],
                False,
            )
        ]
    pages: list[list[Any]] = [[]]
    column = 0
    y = top
    for record, title_lines, lines, images, continued in prepared:
        block_height = max(
            130, 44 + len(title_lines) * 34 + len(lines) * line_height + (130 if images else 0)
        )
        if y + block_height > limit:
            if column + 1 < columns:
                column += 1
                y = top
            else:
                pages.append([])
                column = 0
                y = top
        x = pad + column * (column_width + gap)
        pages[-1].append((record, title_lines, lines, images, continued, x, y, block_height))
        y += block_height + gap
    return pages


def record_page_count(
    context: Any, records: list[Record], *, size: tuple[int, int] = (1600, 1100), columns: int = 2
) -> int:
    """Report exact page count using the same measured layout as rendering."""
    return len(plan_records(context, records, size=size, columns=columns))


def iter_records(
    title: str,
    context: Any,
    records: list[Record],
    *,
    variant: str = "light",
    assets: dict | None = None,
    size: tuple[int, int] = (1600, 1100),
    columns: int = 2,
    page_offset: int = 0,
    total_pages: int | None = None,
) -> Iterator[Image.Image]:
    """Draw one bounded page at a time using lightweight, measured layout metadata."""
    pages = plan_records(context, records, size=size, columns=columns)
    column_width = (size[0] - 112 - 24 * (columns - 1)) // columns
    line_height = 32
    for page, blocks in enumerate(pages, 1):
        canvas = PageCanvas(title, context, dark=variant == "dark", size=size, assets=assets)
        for record, title_lines, lines, images, continued, x, y, block_height in blocks:
            canvas.panel((x, y, x + column_width, y + block_height))
            tx = x + 24
            if record.icon:
                canvas.icon(record.icon, tx, y + 23, size=32)
                tx += 44
            for j, line in enumerate(title_lines):
                canvas.text(tx, y + 22 + j * 34, line, size=29, bold=True, width=column_width - (tx - x) - 20)
            yy = y + 32 + len(title_lines) * 34
            if continued:
                canvas.text(x + column_width - 132, y + 6, "CONTINUED", size=13, fill=SIGNAL)
            if images:
                # Pictures supplement explicit names in the text; no data depends on a download.
                for i, (url, name) in enumerate(images):
                    px = x + 24 + i * 114
                    if px + 94 > x + column_width - 24:
                        break
                    photo(canvas, url, (px, yy, px + 94, yy + 94), assets, contain=False)
                    caption, caption_size, _ = fit_label(
                        name, 94, locale=context.locale, size=15, minimum=14, max_lines=1
                    )
                    canvas.text(px, yy + 96, caption, size=caption_size)
                yy += 130
            for line in lines:
                canvas.text(x + 24, yy, line, size=24)
                yy += line_height
        yield canvas.finish(page=page + page_offset, pages=total_pages or len(pages) + page_offset)


def render_records(*args: Any, **kwargs: Any) -> list[Image.Image]:
    """Collect pages for callers that explicitly want an in-memory batch."""
    return list(iter_records(*args, **kwargs))


def append_model_text(lines: list[str], value: Any, prefix: str = "") -> None:
    """Retain structured optional source fields without fabricating interpretation."""
    if isinstance(value, dict):
        for key, item in value.items():
            append_model_text(lines, item, f"{prefix}{key}: ")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            append_model_text(lines, item, f"{prefix}{index + 1}. ")
    elif value is not None and value != "":
        lines.append(prefix + str(value))


def medal_lines(medal: Any) -> list[str]:
    if medal is None:
        return ["Medal: Not supplied"]
    return [
        f"Medal: {medal.name or medal.id} · Level {medal.level}" + (" · Plated" if medal.plated else ""),
        f"Obtained: {stamp(medal.obtained_at)}",
    ]


def team_images(run: Any) -> list[tuple[str | None, str]]:
    return [
        (
            image_url(member.images.avatar) or image_url(member.images.portrait),
            member.name or member.character_id,
        )
        for member in run.team
    ]


def run_lines(run: Any) -> list[str]:
    lines = [
        f"Clear: {'Completed' if run.completed else 'Not completed'} · Time {duration(run.duration_seconds)}",
        f"Completed at: {stamp(run.completed_at)}",
    ]
    if run.score is not None:
        lines.append(f"Score: {run.score}" + (" · Best run" if run.is_best else ""))
    if run.waves is not None:
        lines.append(f"Waves: {run.waves}")
    for member in run.team:
        label = f"{member.name or member.character_id}"
        details = []
        for name, value in (
            ("Lv", member.level),
            ("Potential", member.potential),
            ("Evolution", member.evolution),
            ("Rarity", member.rarity),
            ("Position", member.position),
        ):
            if value is not None:
                details.append(f"{name} {value}")
        for semantic in (member.element, member.profession):
            if semantic.name or semantic.key:
                details.append(semantic.name or semantic.key)
        lines.append(label + (" · " + " · ".join(details) if details else ""))
    if not run.team:
        lines.append("Team: Not supplied")
    return lines
