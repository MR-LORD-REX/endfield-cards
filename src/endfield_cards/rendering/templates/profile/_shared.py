"""Profile content and components shared by AKEF's three visual arrangements."""

from datetime import UTC
from typing import Any

from PIL import Image, ImageDraw

from endfield_cards.adapters.skport import image_url
from endfield_cards.models import RenderContext
from endfield_cards.utils.drawing import ELEMENT_COLORS, PageCanvas, element_key
from endfield_cards.utils.images import composite_fitted, fitted, gradient_alpha, masked, shape_mask
from endfield_cards.utils.records import Record, stamp

SIZE_BY_VARIANT = {"overview": (1600, 1400), "operations": (1600, 1400), "identity": (1920, 1200)}
RARITY = {6: "#F18A43", 5: "#E9BC48", 4: "#A17CDF", 3: "#68A4D6"}
BOARD_W, BOARD_H = 11.9, 4.12


def new_canvas(context: RenderContext, variant: str, assets: dict | None = None) -> PageCanvas:
    canvas = PageCanvas(
        "Profile",
        context,
        dark=variant == "operations",
        size=SIZE_BY_VARIANT[variant],
        assets=assets,
        header=False,
    )
    if variant == "operations":
        canvas.background, canvas.panel_color, canvas.line = "#14171D", "#22262E", "#3B424D"
        canvas.image.paste(canvas.background, (0, 0, canvas.width, canvas.height))
    return canvas


def source(canvas: PageCanvas, url: str | None) -> Image.Image | None:
    return canvas.assets.get(url) if url else None


def days_played(model: Any) -> int | None:
    created, observed = model.created_at, model.server_time or model.snapshot_at
    if created is None or observed is None:
        return None
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    if observed.tzinfo is None:
        observed = observed.replace(tzinfo=UTC)
    elapsed = (observed - created).total_seconds()
    return int(elapsed // 86400) if elapsed >= 0 else None


def facts(model: Any) -> list[tuple[str, str]]:
    values = []
    for label, key in (("Authority", "authority_level"), ("World level", "world_level")):
        if key in model.model_fields_set:
            values.append((label, f"{getattr(model, key):,}"))
    age = days_played(model)
    if age is not None:
        values.append(("Days", f"{age:,}"))
    for label, key in (
        ("Operators", "characters"),
        ("Weapons", "weapons"),
        ("Files", "documents"),
        ("Achievements", "achievements"),
    ):
        if key in model.counts.model_fields_set:
            values.append((label, f"{getattr(model.counts, key):,}"))
    values.extend((region.name or region.id, f"{region.level:,}") for region in model.regions)
    return values


def draw_avatar(
    canvas: PageCanvas,
    model: Any,
    box: tuple[int, int, int, int],
    *,
    shape: str = "circle",
    ring: str | None = "yellow",
) -> None:
    x, y, right, bottom = box
    color = canvas.accent if ring == "yellow" else ring or canvas.line
    draw = canvas.draw
    outline = (x - 4, y - 4, right + 4, bottom + 4)
    if shape == "circle":
        draw.ellipse(outline, fill=color)
        draw.ellipse((x - 1, y - 1, right + 1, bottom + 1), fill=canvas.background)
    else:
        draw.rounded_rectangle(outline, radius=19 if shape == "rounded" else 0, fill=color)
    image = source(canvas, image_url(model.avatar))
    if image is not None:
        composite_fitted(canvas.image, image, box, shape=shape, radius=16, focus=(0.5, 0.25))
    else:
        draw.rectangle(box, fill=canvas.panel_color)
        canvas.text(
            x + 24,
            y + 30,
            canvas.context.owner.name[:1],
            size=62,
            bold=True,
            width=right - x - 48,
            max_lines=1,
        )


def paint_banner(
    canvas: PageCanvas,
    model: Any,
    box: tuple[int, int, int, int],
    *,
    dark: bool = False,
    rounded: bool = True,
) -> None:
    x, y, right, bottom = box
    w, h = right - x, bottom - y
    band = Image.new("RGBA", (w, h), "#21252D" if dark else "#FCFBF8")
    art = source(canvas, image_url(model.banner))
    if art is not None:
        band.alpha_composite(fitted(art, (w, h), focus=(0.5, 0.5)))
        veil = Image.new("RGBA", (w, h), "#14171D" if dark else "#F2F1EC")
        veil.putalpha(gradient_alpha((w, h), vertical=False, start=0.15, end=0.83, maximum=235, reverse=True))
        band.alpha_composite(veil)
    else:
        draw = ImageDraw.Draw(band)
        for position in range(int(w * 0.54), w + h, 38):
            draw.line((position - h, h, position, 0), fill="#2B3039" if dark else "#EBE9E1", width=11)
        draw.polygon(
            ((w - 360, 0), (w - 316, 0), (w - 520, h), (w - 564, h)), fill="#5C4D19" if dark else "#F9DA73"
        )
    if rounded:
        band = masked(band, shape_mask((w, h), radius=22))
    canvas.image.alpha_composite(band, (x, y))


def draw_identity(
    canvas: PageCanvas,
    model: Any,
    x: int,
    y: int,
    width: int,
    *,
    name_size: int = 68,
    color: str | None = None,
) -> None:
    canvas.text(
        x, y, canvas.context.owner.name, size=name_size, bold=True, fill=color, width=width, max_lines=1
    )
    meta = f"UID {canvas.context.owner.game_uid}"
    if model.server_name:
        meta += " · " + model.server_name
    canvas.text(x, y + name_size + 10, meta, size=22, fill=color or canvas.muted, width=width, max_lines=1)
    line = model.biography or model.mission
    if line:
        canvas.text(x, y + name_size + 46, line, size=22, fill=color, width=width, max_lines=2)


def medal_url(medal: Any) -> str | None:
    return image_url(medal.icon) or image_url(medal.plated_icon if medal.plated else medal.initial_icon)


def medal_slots(model: Any) -> dict[int, Any]:
    slots = {medal.slot: medal for medal in model.medals if medal.slot is not None and 1 <= medal.slot <= 10}
    for medal in model.medals:
        if medal.slot is None:
            available = next((slot for slot in range(1, 11) if slot not in slots), None)
            if available is not None:
                slots[available] = medal
    return slots


def medal_geometry(x: int, y: int, unit: float) -> dict[int, tuple[int, int, int, int]]:
    w, h, gap = int(unit * 2), int(unit * 2.31), unit * 0.2
    result = {}
    for slot in range(1, 11):
        row, col = (slot - 1) % 2, (slot - 1) // 2
        px = int(x + col * (w + gap) + row * (w + gap) / 2)
        py = int(y + row * (h - unit * 0.5))
        result[slot] = (px, py, px + w, py + h)
    return result


def medal_board(canvas: PageCanvas, model: Any, x: int, y: int, width: int) -> tuple[int, int]:
    unit = width / BOARD_W
    slots = medal_slots(model)
    for slot, box in medal_geometry(x, y, unit).items():
        px, py, right, bottom = box
        size = right - px, bottom - py
        mask = shape_mask(size, shape="hexagon")
        medal = slots.get(slot)
        icon = source(canvas, medal_url(medal)) if medal else None
        if icon is not None:
            plate = fitted(icon, size, focus=(0.5, 0.5))
        else:
            plate = Image.new("RGBA", size, (54, 60, 72, 125) if canvas.dark else (31, 35, 44, 30))
        canvas.image.alpha_composite(masked(plate, mask), (px, py))
    return int(unit * BOARD_W), int(unit * BOARD_H)


def draw_caption(
    canvas: PageCanvas, model: Any, characters: list[Any], page: int, pages: int, x: int, y: int, width: int
) -> None:
    scope = (
        canvas.t("Owned roster") if canvas.context.source_scope == "owner" else canvas.t("Public showcase")
    )
    count = (
        f"{len(model.characters)} supplied"
        if canvas.context.source_scope == "owner"
        else f"{len(model.characters)}/8"
    )
    canvas.text(
        x, y, f"{scope} · {count}", size=23, bold=True, fill=canvas.muted, width=width - 130, max_lines=1
    )
    if pages > 1:
        canvas.text(
            x + width - 112, y, f"{page:02d}/{pages:02d}", size=22, fill=canvas.accent, width=112, max_lines=1
        )


def _stars(canvas: PageCanvas, count: int, x: int, y: int, color: str, size: int = 17) -> None:
    for index in range(count):
        canvas.icon("rarity.star", x + index * (size + 4), y, size, tint=color)


def _badges(canvas: PageCanvas, character: Any, x: int, y: int, *, clipped: bool = False) -> None:
    tint = ELEMENT_COLORS.get(element_key(character), "#86909C")
    if clipped:
        canvas.draw.rectangle((x, y, x + 40, y + 38), fill=tint)
    else:
        canvas.draw.ellipse((x, y, x + 38, y + 38), fill=tint)
    canvas.icon(
        image_url(character.element.icons) or "element." + character.element.key,
        x + 7,
        y + 7,
        24,
        tint="#FFFFFF",
    )
    canvas.draw.rounded_rectangle((x + 46, y, x + 84, y + 38), radius=7 if not clipped else 0, fill="#171C25")
    canvas.icon(
        image_url(character.profession.icons) or "profession." + character.profession.key,
        x + 52,
        y + 6,
        26,
        tint="#F2F1EC",
    )


def draw_tile(canvas: PageCanvas, character: Any, box: tuple[int, int, int, int], *, style: str) -> None:
    x, y, right, bottom = box
    w, h = right - x, bottom - y
    dark = style == "operations"
    clipped = style == "identity"
    art_h = h if dark else h - 96
    tint = ELEMENT_COLORS.get(element_key(character), "#86909C")
    tile = Image.new("RGBA", (w, art_h), tint)
    url = (
        image_url(character.images.portrait)
        or image_url(character.images.half_body)
        or image_url(character.images.avatar)
    )
    portrait = source(canvas, url)
    if portrait is not None:
        tile.alpha_composite(fitted(portrait, (w, art_h), focus=character.images.focal_point or (0.5, 0.20)))
    shade = Image.new("RGBA", tile.size, "#11151C")
    shade.putalpha(
        gradient_alpha(tile.size, start=0.40 if dark else 0.66, end=1.0, maximum=248 if dark else 100)
    )
    tile.alpha_composite(shade)
    tile = masked(
        tile,
        shape_mask(
            tile.size,
            shape="clipped" if clipped else "rounded" if dark else "top-rounded",
            radius=16,
            cut=28 if clipped else 0,
        ),
    )
    canvas.image.alpha_composite(tile, (x, y))
    rare = RARITY.get(character.rarity, canvas.muted)
    _badges(canvas, character, x + 14, y + 14, clipped=clipped)
    if dark:
        for index in range(5):
            px = right - 111 + index * 18
            canvas.draw.rounded_rectangle(
                (px, y + 27, px + 10, y + 38),
                radius=2,
                fill=canvas.accent if index < character.potential else "#555B66",
            )
        _stars(canvas, character.rarity, x + 19, bottom - 156, rare, 14)
        canvas.text(x + 20, bottom - 130, canvas.t("Level"), size=16, fill=canvas.accent)
        canvas.text(x + 18, bottom - 110, character.level, size=49, bold=True)
        canvas.text(x + 93, bottom - 87, f"/{character.max_level}", size=20, fill="#CDD2DA")
        canvas.draw.rounded_rectangle(
            (x + 158, bottom - 83, x + 204, bottom - 53), radius=6, fill=canvas.accent
        )
        canvas.text(x + 169, bottom - 79, f"E{character.evolution}", size=18, bold=True, fill="#15191F")
        canvas.text(x + 20, bottom - 44, character.name, size=27, bold=True, width=w - 40, max_lines=1)
        canvas.draw.rounded_rectangle((x + 17, bottom - 8, right - 17, bottom - 4), radius=2, fill=rare)
        return
    canvas.draw.rounded_rectangle(
        (x, y + art_h, right, bottom), radius=13, fill="#15191F" if clipped else canvas.panel_color
    )
    canvas.draw.rectangle(
        (x, y + art_h, right, y + art_h + 16), fill="#15191F" if clipped else canvas.panel_color
    )
    canvas.draw.rectangle((x, y + art_h, right, y + art_h + 5), fill=rare)
    if not clipped:
        _stars(canvas, character.rarity, x + 17, y + art_h - 27, rare, 16)
    if clipped:
        name_width = w - 38 - character.rarity * 17
        canvas.text(
            x + 14,
            y + art_h + 13,
            character.name,
            size=25,
            bold=True,
            fill="#F4F3EE",
            width=max(80, name_width),
            max_lines=1,
        )
        _stars(canvas, character.rarity, right - 14 - character.rarity * 17, y + art_h + 18, rare, 13)
        canvas.draw.rectangle((x + 14, bottom - 43, x + 127, bottom - 15), fill=canvas.accent)
        canvas.text(
            x + 24,
            bottom - 41,
            f"Lv {character.level}/{character.max_level}",
            size=17,
            bold=True,
            fill="#15191F",
            width=103,
            max_lines=1,
        )
        canvas.text(
            x + 143,
            bottom - 41,
            f"E{character.evolution}  P{character.potential}",
            size=18,
            fill="#D0D4DC",
            width=w - 155,
            max_lines=1,
        )
    else:
        canvas.text(x + 17, y + art_h + 15, character.name, size=26, bold=True, width=w - 34, max_lines=1)
        canvas.text(
            x + 17,
            bottom - 40,
            f"Lv {character.level}/{character.max_level}",
            size=23,
            bold=True,
            width=w - 125,
            max_lines=1,
        )
        canvas.text(
            right - 103,
            bottom - 37,
            f"E{character.evolution}  P{character.potential}",
            size=20,
            fill=canvas.muted,
            width=89,
            max_lines=1,
        )


def draw_empty(canvas: PageCanvas, box: tuple[int, int, int, int]) -> None:
    x, y, right, bottom = box
    canvas.panel(box)
    canvas.text(
        x + 40,
        y + 80,
        canvas.t("No characters supplied"),
        size=34,
        bold=True,
        width=right - x - 80,
        max_lines=2,
    )


def detail_records(model: Any) -> list[Record]:
    records = [
        Record(
            "Profile information",
            [f"{name}: {value}" for name, value in facts(model)]
            + [model.biography, model.mission, f"Created: {stamp(model.created_at)}"],
        )
    ]
    records.extend(
        Record(
            medal.name or medal.id,
            [f"Level {medal.level}", f"Obtained: {stamp(medal.obtained_at)}"],
            images=[(medal_url(medal), medal.name)],
        )
        for medal in model.medals
    )
    for region in model.regions:
        lines = [f"Region level: {region.level}"]
        for area in region.areas:
            lines.append(area.name or area.id)
            lines.extend(
                f"{counter.name or counter.key}: {counter.current:g}/{counter.maximum:g}"
                for counter in area.counters
            )
        records.append(Record(region.name or region.id, lines))
    return records
