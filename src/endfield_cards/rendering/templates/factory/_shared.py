"""Regional industry and Dijiang dashboards, kept separate from exploration."""

from __future__ import annotations

from collections.abc import Iterator
from math import ceil
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.errors import DataValidationError
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import composite_fitted
from endfield_cards.utils.meters import bar
from endfield_cards.utils.records import number

WIDTH = 1600
PAD = 40
GAP = 24
REGIONS_PER_PAGE = 2
POSTS_PER_PANEL = 4
CABINS_PER_PAGE = 6
CREW_PER_PANEL = 3
Box = tuple[int, int, int, int]
CABINS = {
    0: ("Control Nexus", "player.room-control"),
    1: ("Manufacturing Cabin", "player.room-manufacturing"),
    2: ("Growth Chamber", "player.room-growth"),
    5: ("Reception Room", "player.room-reception"),
}
PRODUCTION_NAMES = {
    "power": "Power",
    "electricity": "Electricity",
    "output": "Output",
    "productionRate": "Production rate",
    "throughput": "Throughput",
    "manufacturing": "Manufacturing",
}
REPORT_NAMES = {
    "credit": "Credits",
    "credits": "Credits",
    "clues": "Clues",
    "output": "Output",
    "production": "Production",
}


def text(c: PageCanvas, x: int, y: int, value: Any, width: int, **options: Any) -> None:
    preview = str(value)
    if len(preview) > 180:
        preview = preview[:180] + "…"
    c.text(x, y, preview, width=max(1, width), max_lines=options.pop("max_lines", 1), **options)


def signal(c: PageCanvas) -> str:
    return c.accent if c.dark else "#916900"


def observed(model: Any, field: str) -> Any:
    return getattr(model, field) if field in getattr(model, "model_fields_set", ()) else None


def status_number(value: float | None) -> str:
    return "—" if value is None else f"{value:,.0f}"


def identity_names(profile: Any) -> dict[str, str]:
    """A matching profile may supply display names for the same operator identities."""
    names = {}
    for operator in getattr(profile, "characters", ()):
        if operator.name:
            for key in (operator.identity.skport_id, operator.identity.str_id):
                if key:
                    names[str(key)] = operator.name
    return names


def meter_values(meter: Any) -> tuple[float | None, float | None]:
    return observed(meter, "current"), observed(meter, "maximum")


def meter_text(meter: Any) -> str:
    current, maximum = meter_values(meter)
    return f"{number(current)} / {number(maximum)}"


def meter_ratio(meter: Any) -> float:
    current, maximum = meter_values(meter)
    return current / maximum if current is not None and maximum is not None and maximum > 0 else 0


def meter_full(meter: Any) -> bool:
    current, maximum = meter_values(meter)
    return current is not None and maximum is not None and maximum > 0 and current >= maximum


def scalar_rows(data: Any, names: dict[str, str], limit: int = 3) -> list[tuple[str, str]]:
    """Only recognized scalar production/report values belong on the concise board."""
    if not isinstance(data, dict):
        return []
    rows = []
    for key, label in names.items():
        value = data.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            rows.append((label, number(value)))
        elif isinstance(value, dict):
            current = value.get("current", value.get("count"))
            maximum = value.get("maximum", value.get("total"))
            if isinstance(current, (int, float)) and not isinstance(current, bool):
                rows.append(
                    (
                        label,
                        f"{number(current)} / {number(maximum)}" if maximum is not None else number(current),
                    )
                )
        if len(rows) == limit:
            break
    return rows


def urls(model: Any) -> set[str]:
    links = [
        image_url(post.officer.icon)
        for region in model.regions
        for post in region.settlements
        if post.officer is not None
    ]
    links.extend(image_url(member.icon) for cabin in model.cabins for member in cabin.crew)
    return {url for url in links if url}


def validate(model: Any, context: Any, profile: Any) -> None:
    validate_owner(model, context)
    if profile is not None:
        validate_owner(profile, context)
    for entries, name in ((model.regions, "region"),):
        ids = [entry.id for entry in entries if entry.id]
        if len(set(ids)) != len(ids):
            raise DataValidationError(
                f"Factory contains duplicate {name} identities", code=f"duplicate_{name}"
            )
    for region in model.regions:
        ids = [entry.id for entry in region.settlements if entry.id]
        if len(set(ids)) != len(ids):
            raise DataValidationError(
                "Factory contains duplicate settlement identities", code="duplicate_settlement"
            )


def header(c: PageCanvas, model: Any, profile: Any) -> None:
    c.draw.line((PAD, 15, PAD + 128, 15), fill=c.accent, width=4)
    avatar = image_url(profile.avatar) if profile is not None else None
    source = c.assets.get(avatar) if avatar else None
    c.draw.ellipse((PAD, 35, PAD + 92, 127), fill=c.accent)
    if source is not None:
        composite_fitted(c.image, source, (PAD + 5, 40, PAD + 87, 122), shape="circle")
    else:
        c.centered_text(
            (PAD + 6, 42, PAD + 86, 121), c.context.owner.name[:1], size=39, bold=True, fill="#171C24"
        )
    text(c, PAD + 114, 38, c.context.owner.name, 850, size=45, bold=True)
    identity = f"UID {c.context.owner.game_uid}"
    if profile is not None and profile.server_name:
        identity += " · " + profile.server_name
    if profile is not None and "authority_level" in profile.model_fields_set:
        identity += f" · Authority {profile.authority_level}"
    text(c, PAD + 116, 98, identity, 905, size=18, fill=c.muted)
    c.icon("player.factory", 1199, 35, 33, tint=signal(c))
    text(c, 1244, 39, "FACTORY / DIJIANG", 316, size=23, bold=True, fill=signal(c))
    posts = [post for region in model.regions for post in region.settlements]
    known = [post for post in posts if "maximum_level" in post.model_fields_set]
    maximum = sum(post.maximum_level for post in known)
    value = f"{maximum}/{len(posts)} settlements maxed" if known else "Settlement levels unavailable"
    if known and len(known) < len(posts):
        value += f" · {len(posts) - len(known)} unknown"
    text(c, 1042, 83, value, 518, size=20, bold=True)
    text(
        c,
        1060,
        118,
        f"{len(model.regions)} regions · {len(model.cabins)} Dijiang cabins",
        500,
        size=16,
        fill=c.muted,
    )
    c.draw.line((PAD, 157, WIDTH - PAD, 157), fill=c.line)


def portrait(c: PageCanvas, person: Any, box: Box, *, circle: bool = False, placeholder: str = "—") -> None:
    x, y, right, bottom = box
    if circle:
        c.draw.ellipse(box, fill=c.background, outline=c.line)
    else:
        c.draw.rounded_rectangle(box, radius=9, fill=c.background, outline=c.line)
    source = image_url(person.icon) if person is not None else None
    pixels = c.assets.get(source) if source else None
    if pixels is not None:
        composite_fitted(
            c.image, pixels, box, shape="circle" if circle else "rounded", radius=9, focus=(0.5, 0.15)
        )
    else:
        name = person.name if person is not None and person.name else placeholder
        c.centered_text((x + 3, y + 3, right - 3, bottom - 3), name[:1], size=23, fill=c.muted, bold=True)


def region_height(region: Any, posts: list[Any], *, dark: bool) -> int:
    production = scalar_rows(region.factory, PRODUCTION_NAMES)
    return 172 + len(posts) * (123 if dark else 137) + (30 + 27 * len(production) if production else 0)


def region_panel(
    c: PageCanvas, region: Any, posts: list[Any], offset: int, box: Box, names: dict[str, str]
) -> None:
    x, y, right, _ = box
    width = right - x
    c.panel((x, y, right, y + 152))
    c.icon("player.development", x + 20, y + 23, 27, tint=signal(c))
    text(c, x + 61, y + 18, region.name or "Unnamed region", width - 184, size=31, bold=True)
    level = observed(region, "level")
    c.draw.rounded_rectangle(
        (right - 113, y + 24, right - 20, y + 54), radius=10, fill=c.accent if c.dark else "#222832"
    )
    c.centered_text(
        (right - 111, y + 24, right - 22, y + 54),
        f"Lv {number(level)}",
        size=16,
        bold=True,
        fill="#171C24" if c.dark else "#FFC800",
    )
    text(c, x + 23, y + 68, "REGIONAL FUNDS", width - 46, size=15, bold=True, fill=c.muted)
    text(c, x + 23, y + 94, meter_text(region.funds), width - 46, size=26, bold=True)
    bar(c, (x + 23, y + 130, right - 23, y + 140), meter_ratio(region.funds))
    sy = y + 170
    for index, post in enumerate(posts):
        post_height = 112 if c.dark else 126
        settlement(c, post, (x, sy, right, sy + post_height), offset + index, names)
        sy += 123 if c.dark else 137
    production = scalar_rows(region.factory, PRODUCTION_NAMES)
    if production:
        text(c, x + 5, sy + 3, "PRODUCTION", width - 10, size=15, bold=True, fill=c.muted)
        sy += 29
        for label, value in production:
            text(c, x + 8, sy, label, width // 2 - 16, size=17, fill=c.muted)
            text(c, x + width // 2, sy, value, width // 2 - 8, size=18, bold=True)
            sy += 27
    if offset:
        text(
            c,
            x + 64,
            y + 49,
            f"Settlements {offset + 1}–{offset + len(posts)} of {len(region.settlements)}",
            width - 170,
            size=13,
            fill=c.muted,
        )


def settlement(c: PageCanvas, post: Any, box: Box, index: int, names: dict[str, str]) -> None:
    x, y, right, bottom = box
    width = right - x
    c.panel(box)
    portrait(c, post.officer, (x + 13, y + 15, x + 86, y + 88))
    name = (
        post.officer.name or names.get(post.officer.id, "Officer")
        if post.officer is not None
        else "Unassigned"
        if "officer" in post.model_fields_set
        else "Officer —"
    )
    text(c, x + 14, y + 93, name, 74, size=11, fill=c.muted)
    tx = x + 103
    maximum = observed(post, "maximum_level")
    level = observed(post, "level")
    tag = "MAX" if maximum is True else f"Lv {number(level)}"
    c.draw.rounded_rectangle(
        (right - 91, y + 14, right - 14, y + 42), radius=8, fill=c.accent if maximum else c.line
    )
    c.centered_text(
        (right - 90, y + 14, right - 15, y + 42), tag, size=14, bold=True, fill="#171C24" if maximum else c.fg
    )
    text(c, tx, y + 12, post.name or f"Settlement {index + 1}", width - 209, size=23, bold=True)
    full = meter_full(post.stock)
    text(
        c,
        tx,
        y + 48,
        "STOCK" + (" · FULL" if full else ""),
        155,
        size=13,
        bold=True,
        fill=signal(c) if full else c.muted,
    )
    text(c, tx + 156, y + 46, meter_text(post.stock), right - tx - 171, size=18, bold=True)
    bar(c, (tx, y + 77, right - 15, y + 87), meter_ratio(post.stock))
    if maximum is True:
        text(c, tx, bottom - 25, "Maximum settlement level", right - tx - 15, size=13, fill=c.muted)
    else:
        text(c, tx, bottom - 27, "EXP " + meter_text(post.experience), right - tx - 15, size=14, fill=c.muted)
        if not c.dark:
            bar(c, (x + 15, bottom - 10, right - 15, bottom - 6), meter_ratio(post.experience))


def cabin_name(cabin: Any) -> str:
    return cabin.name or CABINS.get(cabin.kind, ("Cabin", "player.factory"))[0]


def cabin_height(cards: list[tuple[Any, list[Any], int]], *, dark: bool) -> int:
    if not cards:
        return 125
    reports = max(len(scalar_rows(cabin.reports, REPORT_NAMES, 2)) for cabin, _, _ in cards)
    return (260 if dark else 256) + (24 * reports)


def cabin(c: PageCanvas, source: Any, crew: list[Any], offset: int, box: Box, names: dict[str, str]) -> None:
    x, y, right, bottom = box
    width = right - x
    c.panel(box)
    icon = CABINS.get(source.kind, ("Cabin", "player.factory"))[1]
    c.draw.rounded_rectangle((x + 14, y + 13, x + 45, y + 44), radius=6, fill="#252C35")
    c.icon(icon, x + 17, y + 16, 26, preserve_color=True)
    text(c, x + 53, y + 17, cabin_name(source), width - 67, size=20, bold=True)
    level = number(observed(source, "level"))
    text(c, x + 20, y + 49, f"Lv {level}", width - 40, size=16, bold=True, fill=signal(c))
    if offset:
        text(c, x + 81, y + 51, f"Crew {offset + 1}–{offset + len(crew)}", width - 102, size=13, fill=c.muted)
    if not crew:
        label = "No assigned crew" if "crew" in source.model_fields_set else "Crew unavailable"
        text(c, x + 23, y + 121, label, width - 46, size=21, fill=c.muted)
    elif c.dark:
        for index, member in enumerate(crew):
            py = y + 86 + index * 49
            portrait(c, member, (x + 20, py, x + 59, py + 39), circle=True)
            label = member.name or names.get(member.id, f"Operator {offset + index + 1}")
            text(c, x + 73, py - 1, label, width - 91, size=17, bold=True)
            values = []
            if member.physical_strength is not None:
                values.append("Stamina " + status_number(member.physical_strength))
            if member.favorability is not None:
                values.append("Favor " + status_number(member.favorability))
            text(
                c,
                x + 75,
                py + 23,
                " · ".join(values) or "Status unavailable",
                width - 93,
                size=13,
                fill=c.muted,
            )
    else:
        cw = (width - 32) // CREW_PER_PANEL
        for index, member in enumerate(crew):
            px = x + 16 + index * cw
            size = min(57, cw - 5)
            portrait(
                c, member, (px + (cw - size) // 2, y + 83, px + (cw + size) // 2, y + 83 + size), circle=True
            )
            text(
                c,
                px + 1,
                y + 146,
                member.name or names.get(member.id, f"Operator {offset + index + 1}"),
                cw - 2,
                size=13,
                bold=True,
                max_lines=2,
            )
            text(c, px + 1, y + 186, "STAMINA", cw - 2, size=10, fill=c.muted)
            text(c, px + 1, y + 202, status_number(member.physical_strength), cw - 2, size=14, bold=True)
            text(
                c, px + 1, y + 224, "Fav " + status_number(member.favorability), cw - 2, size=12, fill=c.muted
            )
    for index, (label, value) in enumerate(scalar_rows(source.reports, REPORT_NAMES, 2)):
        py = bottom - 21 - (len(scalar_rows(source.reports, REPORT_NAMES, 2)) - index - 1) * 24
        text(c, x + 18, py, label, width // 2 - 20, size=13, fill=c.muted)
        text(c, x + width // 2, py, value, width // 2 - 16, size=14, bold=True)


def plans(model: Any) -> list[tuple[list[tuple[Any, list[Any], int]], list[tuple[Any, list[Any], int]]]]:
    regions = [
        (region, region.settlements[offset : offset + POSTS_PER_PANEL], offset)
        for region in model.regions
        for offset in range(0, max(1, len(region.settlements)), POSTS_PER_PANEL)
    ]
    cabins = [
        (room, room.crew[offset : offset + CREW_PER_PANEL], offset)
        for room in model.cabins
        for offset in range(0, max(1, len(room.crew)), CREW_PER_PANEL)
    ]
    count = max(1, ceil(len(regions) / REGIONS_PER_PAGE), ceil(len(cabins) / CABINS_PER_PAGE))
    return [
        (
            regions[index * REGIONS_PER_PAGE : (index + 1) * REGIONS_PER_PAGE],
            cabins[index * CABINS_PER_PAGE : (index + 1) * CABINS_PER_PAGE],
        )
        for index in range(count)
    ]


def draw(
    model: Any,
    context: Any,
    regions: list[Any],
    rooms: list[Any],
    *,
    dark: bool,
    assets: Any,
    profile: Any,
    page: int,
    pages: int,
) -> Image.Image:
    top = 185
    region_h = max((region_height(region, posts, dark=dark) for region, posts, _ in regions), default=146)
    ship_top = top + region_h + 29
    columns = min(3 if dark else 6, max(1, len(rooms)))
    room_h = cabin_height(rooms, dark=dark)
    rows = max(1, ceil(len(rooms) / columns))
    height = ship_top + 47 + rows * room_h + (rows - 1) * 20 + 100
    c = PageCanvas(
        "Factory and Dijiang", context, dark=dark, size=(WIDTH, max(790, height)), assets=assets, header=False
    )
    header(c, model, profile)
    names = identity_names(profile)
    if regions:
        width = (WIDTH - PAD * 2 - GAP * (len(regions) - 1)) // len(regions)
        for index, (region, posts, offset) in enumerate(regions):
            x = PAD + index * (width + GAP)
            region_panel(c, region, posts, offset, (x, top, x + width, top + region_h), names)
    else:
        c.panel((PAD, top, WIDTH - PAD, top + 135))
        text(
            c,
            PAD + 24,
            top + 49,
            "No regional factory data supplied",
            WIDTH - PAD * 2 - 48,
            size=26,
            fill=c.muted,
        )
    c.icon("player.factory", PAD, ship_top + 2, 27, tint=signal(c))
    text(c, PAD + 41, ship_top + 2, "DIJIANG CABINS", 900, size=24, bold=True)
    if rooms:
        width = (WIDTH - PAD * 2 - 20 * (columns - 1)) // columns
        for index, (room, crew, offset) in enumerate(rooms):
            row, col = divmod(index, columns)
            x, y = PAD + col * (width + 20), ship_top + 47 + row * (room_h + 20)
            cabin(c, room, crew, offset, (x, y, x + width, y + room_h), names)
    else:
        c.panel((PAD, ship_top + 47, WIDTH - PAD, ship_top + 47 + room_h))
        text(
            c, PAD + 24, ship_top + 85, "No cabin data supplied", WIDTH - PAD * 2 - 48, size=25, fill=c.muted
        )
    return c.finish(page=page, pages=pages)


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: Any = None,
    profile: Any = None,
    **options: Any,
) -> Iterator[Image.Image]:
    """Draw bounded factory/Dijiang pages, never consulting exploration areas."""
    validate(model, context, profile)
    pages = plans(model)
    for page, (regions, cabins) in enumerate(pages, 1):
        yield draw(
            model,
            context,
            regions,
            cabins,
            dark=variant == "dark",
            assets=assets,
            profile=profile,
            page=page,
            pages=len(pages),
        )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
