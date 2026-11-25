"""Exploration-only boards preserving every supplied area and category counter."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from math import ceil
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.errors import DataValidationError
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import composite_fitted

WIDTH = 2000
PAD = 44
GAP = 18
TOP = 192
MAX_HEIGHT = 2400
FOOTER = 88
AREA_HEIGHT = 224
LIGHT_COLUMNS = 4
LEDGER_ROW = 73
CATEGORY_LIMIT = 6
ICONS = {
    "puzzleCount": "player.explore-puzzle",
    "trchestCount": "player.explore-chest",
    "equipTrchestCount": "player.explore-equipment",
    "pieceCount": "player.explore-collectible",
    "blackboxCount": "player.explore-datalogger",
    "trstarCount": "player.explore-aurylene",
}


def text(c: PageCanvas, x: int, y: int, value: object, width: int, **options: Any) -> None:
    """Fit short labels without measuring unbounded source strings."""
    value = str(value)
    value = value[:239] + "…" if len(value) > 240 else value
    c.text(x, y, value, width=width, max_lines=options.pop("max_lines", 1), **options)


def number(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:,.0f}" if float(value).is_integer() else f"{value:g}"


def values(counter: Any) -> tuple[float | None, float | None]:
    fields = counter.model_fields_set
    return (
        counter.current if "current" in fields else None,
        counter.maximum if "maximum" in fields else None,
    )


def counter_text(counter: Any | None) -> str:
    if counter is None:
        return "—"
    current, maximum = values(counter)
    return f"{number(current)} / {number(maximum)}"


@dataclass(frozen=True)
class Summary:
    current: float
    maximum: float
    known: int
    total: int

    @property
    def ratio(self) -> float | None:
        return self.current / self.maximum if self.maximum > 0 and self.known else None

    @property
    def label(self) -> str:
        if not self.known:
            return "—"
        return f"{number(self.current)} / {number(self.maximum)}" + (
            " known" if self.known < self.total else ""
        )


def summary(counters: list[Any]) -> Summary:
    pairs = [values(counter) for counter in counters]
    known = [(current, maximum) for current, maximum in pairs if current is not None and maximum is not None]
    return Summary(sum(pair[0] for pair in known), sum(pair[1] for pair in known), len(known), len(pairs))


def percent(value: Summary) -> str:
    if value.ratio is None:
        return "—"
    return f"{value.ratio:.0%}" + (" known" if value.known < value.total else "")


def counters_for(region: Any) -> list[Any]:
    return [counter for area in region.areas for counter in area.counters]


def regions(model: Any) -> list[Any]:
    entries = list(model.regions)
    identifiers = [entry.id for entry in entries if entry.id]
    if len(set(identifiers)) != len(identifiers):
        raise DataValidationError("Exploration contains duplicate region identities", code="duplicate_region")
    for region in entries:
        identifiers = [area.id for area in region.areas if area.id]
        if len(set(identifiers)) != len(identifiers):
            raise DataValidationError("Exploration contains duplicate area identities", code="duplicate_area")
        for area in region.areas:
            keys = [counter.key for counter in area.counters if counter.key]
            if len(set(keys)) != len(keys):
                raise DataValidationError(
                    "Exploration contains duplicate category identities", code="duplicate_counter"
                )
    return entries


def urls(model: Any) -> set[str]:
    """Exploration uses bundled semantic icons; optional profile art is supplied separately."""
    return set()


def progress(c: PageCanvas, ratio: float | None, box: tuple[int, int, int, int]) -> None:
    x, y, right, bottom = box
    c.draw.rounded_rectangle(box, radius=max(1, (bottom - y) // 2), fill=c.line)
    if ratio is None:
        return
    amount = round((right - x) * min(1.0, max(0.0, ratio)))
    if amount:
        color = c.muted if ratio >= 1 else c.accent
        c.draw.rounded_rectangle((x, y, x + amount, bottom), radius=max(1, (bottom - y) // 2), fill=color)


def draw_header(c: PageCanvas, entries: list[Any], profile: Any) -> None:
    c.icon("player.exploration", PAD, 27, 30, tint=c.accent if c.dark else "#916900")
    text(c, PAD + 43, 27, "ENDFIELD / EXPLORATION", 870, size=23, bold=True)
    source = image_url(profile.avatar) if profile is not None else None
    pixels = c.assets.get(source) if source else None
    c.draw.ellipse((PAD, 76, PAD + 80, 156), fill=c.accent)
    if pixels is not None:
        composite_fitted(c.image, pixels, (PAD + 4, 80, PAD + 76, 152), shape="circle")
    else:
        c.centered_text(
            (PAD + 4, 80, PAD + 76, 152), c.context.owner.name[:1], size=37, bold=True, fill="#171C24"
        )
    text(c, PAD + 104, 75, c.context.owner.name, 850, size=43, bold=True)
    identity = f"UID {c.context.owner.game_uid}"
    if profile is not None:
        if profile.server_name:
            identity += " · " + profile.server_name
        if "authority_level" in profile.model_fields_set:
            identity += f" · Authority {profile.authority_level}"
    text(c, PAD + 106, 130, identity, 860, size=18, fill=c.muted)
    areas = [area for region in entries for area in region.areas]
    total = summary([counter for area in areas for counter in area.counters])
    for index, (label, value) in enumerate(
        (("REGIONS", len(entries)), ("AREAS", len(areas)), ("EXPLORED", percent(total)))
    ):
        x = 1170 + index * 252
        c.draw.line((x - 22, 84, x - 22, 151), fill=c.line)
        text(c, x, 82, label, 240, size=15, bold=True, fill=c.muted)
        text(c, x - 1, 109, value, 240, size=39, bold=True)
    c.draw.line((PAD, 174, WIDTH - PAD, 174), fill=c.line)


@dataclass
class AreaTile:
    area: Any | None
    source_index: int
    counters: list[Any]
    part: int = 1
    parts: int = 1


@dataclass
class LightSection:
    region: Any
    source_index: int
    tiles: list[AreaTile] = field(default_factory=list)
    continued: bool = False

    @property
    def height(self) -> int:
        return 79 + ceil(max(1, len(self.tiles)) / LIGHT_COLUMNS) * (AREA_HEIGHT + GAP) - GAP


def light_pages(entries: list[Any]) -> list[list[LightSection]]:
    """Plan bounded rows without dropping areas or extra source categories."""
    pages: list[list[LightSection]] = [[]]
    used = 0
    room = MAX_HEIGHT - TOP - FOOTER
    for region_index, region in enumerate(entries):
        tiles: list[AreaTile] = []
        for area_index, area in enumerate(region.areas):
            chunks = [
                area.counters[start : start + CATEGORY_LIMIT]
                for start in range(0, len(area.counters), CATEGORY_LIMIT)
            ] or [[]]
            tiles.extend(
                AreaTile(area, area_index, chunk, part + 1, len(chunks)) for part, chunk in enumerate(chunks)
            )
        tiles = tiles or [AreaTile(None, 0, [])]
        current: LightSection | None = None
        for start in range(0, len(tiles), LIGHT_COLUMNS):
            row = tiles[start : start + LIGHT_COLUMNS]
            required = AREA_HEIGHT + (GAP if current is not None else 79)
            if pages[-1] and used + required > room:
                pages.append([])
                used = 0
                current = None
                required = AREA_HEIGHT + 79
            if current is None:
                current = LightSection(region, region_index, continued=start > 0)
                pages[-1].append(current)
            current.tiles.extend(row)
            used += required
        used += 28
    return pages


def draw_region_title(c: PageCanvas, region: Any, index: int, y: int, *, continued: bool = False) -> None:
    c.icon("player.exploration", PAD + 2, y + 3, 27, tint=c.accent if c.dark else "#916900")
    title = f"{index + 1:02d}  {region.name or region.id or 'Unnamed region'}"
    if continued:
        title += " · continued"
    text(c, PAD + 43, y, title, 1150, size=30, bold=True)
    totals = summary(counters_for(region))
    text(c, 1350, y + 4, totals.label, WIDTH - PAD - 1350, size=22, bold=True)
    text(
        c,
        PAD + 45,
        y + 41,
        f"{len(region.areas)} areas · {len(category_keys(region))} categories",
        1250,
        size=15,
        fill=c.muted,
    )


def draw_area_tile(c: PageCanvas, tile: AreaTile, box: tuple[int, int, int, int]) -> None:
    x, y, right, bottom = box
    c.panel(box)
    if tile.area is None:
        c.icon("player.exploration", x + 20, y + 26, 34, tint=c.muted)
        text(c, x + 68, y + 29, "No area data supplied", right - x - 88, size=23, fill=c.muted)
        return
    label = f"{tile.source_index + 1:02d}  {tile.area.name or tile.area.id or 'Unnamed area'}"
    text(c, x + 18, y + 13, label, right - x - 106, size=23, bold=True)
    totals = summary(tile.area.counters)
    badge = (
        f"{tile.part}/{tile.parts}"
        if tile.parts > 1
        else "Partial"
        if totals.known < totals.total
        else percent(totals)
    )
    text(c, right - 81, y + 17, badge, 66, size=17, fill=c.muted)
    c.draw.line((x + 17, y + 50, right - 17, y + 50), fill=c.line)
    if not tile.counters:
        text(c, x + 18, y + 88, "Counters unavailable", right - x - 36, size=22, fill=c.muted)
        return
    cell_width = (right - x - 32) // 3
    for index, counter in enumerate(tile.counters):
        row, column = divmod(index, 3)
        px, py = x + 16 + column * cell_width, y + 63 + row * 78
        c.icon(ICONS.get(counter.key, "player.exploration"), px + 1, py + 5, 26, tint=c.fg)
        text(c, px + 34, py + 7, counter_text(counter), cell_width - 43, size=19, bold=True)
        text(
            c,
            px + 2,
            py + 37,
            counter.name or counter.key or "Counter",
            cell_width - 10,
            size=14,
            fill=c.muted,
        )
        current, maximum = values(counter)
        ratio = current / maximum if current is not None and maximum is not None and maximum > 0 else None
        progress(c, ratio, (px + 2, py + 64, px + cell_width - 12, py + 68))


def light_page(
    sections: list[LightSection],
    entries: list[Any],
    context: Any,
    assets: Any,
    profile: Any,
    page: int,
    pages: int,
) -> Image.Image:
    height = max(730, TOP + sum(section.height + 28 for section in sections) + FOOTER)
    c = PageCanvas("Exploration", context, size=(WIDTH, height), assets=assets, header=False)
    draw_header(c, entries, profile)
    y = TOP
    cell_width = (WIDTH - PAD * 2 - GAP * (LIGHT_COLUMNS - 1)) // LIGHT_COLUMNS
    for section in sections:
        draw_region_title(c, section.region, section.source_index, y, continued=section.continued)
        for index, tile in enumerate(section.tiles):
            row, column = divmod(index, LIGHT_COLUMNS)
            px, py = PAD + column * (cell_width + GAP), y + 79 + row * (AREA_HEIGHT + GAP)
            draw_area_tile(c, tile, (px, py, px + cell_width, py + AREA_HEIGHT))
        y += section.height + 28
    return c.finish(page, pages)


@dataclass
class LedgerSection:
    region: Any
    source_index: int
    categories: list[tuple[str, str]]
    areas: list[tuple[int, Any]]
    category_page: int = 1
    category_pages: int = 1
    continued: bool = False

    @property
    def height(self) -> int:
        return 160 + max(1, len(self.areas)) * LEDGER_ROW


def category_keys(region: Any) -> list[tuple[str, str]]:
    found: dict[str, str] = {}
    for area in region.areas:
        for index, counter in enumerate(area.counters):
            key = counter.key or f"__unnamed_{index}"
            found.setdefault(key, counter.name or counter.key or "Counter")
    return list(found.items())


def ledger_pages(entries: list[Any]) -> list[list[LedgerSection]]:
    pages: list[list[LedgerSection]] = [[]]
    used = 0
    room = MAX_HEIGHT - TOP - FOOTER
    for region_index, region in enumerate(entries):
        keys = category_keys(region)
        chunks = [keys[start : start + CATEGORY_LIMIT] for start in range(0, len(keys), CATEGORY_LIMIT)] or [
            []
        ]
        areas = list(enumerate(region.areas))
        for chunk_index, chunk in enumerate(chunks):
            current: LedgerSection | None = None
            for area_index, area in areas or [(0, None)]:
                required = LEDGER_ROW + (0 if current is not None else 160)
                if pages[-1] and used + required > room:
                    pages.append([])
                    used = 0
                    current = None
                    required = LEDGER_ROW + 160
                if current is None:
                    current = LedgerSection(
                        region, region_index, chunk, [], chunk_index + 1, len(chunks), area_index > 0
                    )
                    pages[-1].append(current)
                current.areas.append((area_index, area))
                used += required
            used += 28
    return pages


def draw_ledger(c: PageCanvas, section: LedgerSection, y: int) -> None:
    draw_region_title(c, section.region, section.source_index, y, continued=section.continued)
    top = y + 78
    left_width = 350
    cell_width = (WIDTH - PAD * 2 - left_width) // max(1, len(section.categories))
    if section.category_pages > 1:
        text(
            c,
            PAD + 4,
            top + 20,
            f"Categories {section.category_page}/{section.category_pages}",
            left_width - 22,
            size=18,
            fill=c.muted,
        )
    else:
        text(c, PAD + 5, top + 20, "AREA / PROGRESS", left_width - 22, size=18, bold=True, fill=c.muted)
    for index, (key, name) in enumerate(section.categories):
        px = PAD + left_width + index * cell_width
        c.icon(ICONS.get(key, "player.exploration"), px + 7, top + 3, 28, tint=c.accent)
        text(c, px + 49, top + 6, name, cell_width - 62, size=18, bold=True)
        total = summary(
            [
                counter
                for area in section.region.areas
                for source_index, counter in enumerate(area.counters)
                if (counter.key or f"__unnamed_{source_index}") == key
            ]
        )
        text(c, px + 49, top + 36, total.label, cell_width - 60, size=15, fill=c.muted)
    row_y = y + 160
    for source_index, area in section.areas:
        c.draw.rounded_rectangle(
            (PAD, row_y, WIDTH - PAD, row_y + LEDGER_ROW - 8), radius=9, fill=c.panel_color
        )
        if area is None:
            text(
                c, PAD + 20, row_y + 16, "No area data supplied", WIDTH - PAD * 2 - 40, size=23, fill=c.muted
            )
            row_y += LEDGER_ROW
            continue
        text(
            c,
            PAD + 18,
            row_y + 10,
            f"{source_index + 1:02d}  {area.name or area.id or 'Unnamed area'}",
            left_width - 40,
            size=20,
            bold=True,
            max_lines=2,
        )
        area_total = summary(area.counters)
        progress(c, area_total.ratio, (PAD + 18, row_y + 54, PAD + left_width - 28, row_y + 58))
        counters = {
            (counter.key or f"__unnamed_{index}"): counter for index, counter in enumerate(area.counters)
        }
        for index, (key, _) in enumerate(section.categories):
            px = PAD + left_width + index * cell_width
            counter = counters.get(key)
            c.centered_text(
                (px + 6, row_y + 5, px + cell_width - 12, row_y + 38),
                counter_text(counter),
                size=22,
                bold=True,
            )
            current, maximum = values(counter) if counter is not None else (None, None)
            ratio = current / maximum if current is not None and maximum is not None and maximum > 0 else None
            progress(c, ratio, (px + 35, row_y + 48, px + cell_width - 42, row_y + 53))
        row_y += LEDGER_ROW


def dark_page(
    sections: list[LedgerSection],
    entries: list[Any],
    context: Any,
    assets: Any,
    profile: Any,
    page: int,
    pages: int,
) -> Image.Image:
    height = max(730, TOP + sum(section.height + 28 for section in sections) + FOOTER)
    c = PageCanvas("Exploration", context, dark=True, size=(WIDTH, height), assets=assets, header=False)
    draw_header(c, entries, profile)
    y = TOP
    for section in sections:
        draw_ledger(c, section, y)
        y += section.height + 28
    return c.finish(page, pages)


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: Any = None,
    profile: Any = None,
    **options: Any,
) -> Iterator[Image.Image]:
    validate_owner(model, context)
    if profile is not None:
        validate_owner(profile, context)
    entries = regions(model)
    if not entries:
        c = PageCanvas(
            "Exploration", context, dark=variant == "dark", size=(WIDTH, 730), assets=assets, header=False
        )
        draw_header(c, entries, profile)
        c.panel((PAD, 212, WIDTH - PAD, 388))
        c.icon("player.exploration", PAD + 28, 260, 50, tint=c.muted)
        text(
            c, PAD + 101, 266, "No exploration regions supplied", WIDTH - PAD * 2 - 135, size=31, fill=c.muted
        )
        yield c.finish()
        return
    if variant == "light":
        plans = light_pages(entries)
        for page, sections in enumerate(plans, 1):
            yield light_page(sections, entries, context, assets, profile, page, len(plans))
    else:
        dark_plans = ledger_pages(entries)
        for page, section_group in enumerate(dark_plans, 1):
            yield dark_page(section_group, entries, context, assets, profile, page, len(dark_plans))


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
