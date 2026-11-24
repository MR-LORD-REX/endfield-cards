"""AKEF-inspired profile variants with explicit public/owned collection scope."""

from typing import Any

from PIL import Image, ImageDraw

from endfield_cards.adapters.skport import image_url
from endfield_cards.rendering.components import PageCanvas
from endfield_cards.rendering.templates._records import Record, photo, render_records, stamp


def urls(model: Any) -> set[str]:
    links = [image_url(model.avatar)]
    links.extend(image_url(c.images.portrait) or image_url(c.images.avatar) for c in model.characters)
    links.extend(image_url(m.icon) for m in model.medals)
    return {link for link in links if link}


def render(
    model: Any,
    context: Any,
    *,
    variant: str = "overview",
    assets: dict | None = None,
    details: bool = False,
    **options: Any,
) -> list[Image.Image]:
    groups = [model.characters[i : i + 8] for i in range(0, len(model.characters), 8)] or [[]]
    pages: list[Image.Image] = []
    canvases: list[PageCanvas] = []
    for group in groups:
        c = PageCanvas("Profile", context, dark=variant == "operations", assets=assets)
        if variant == "identity":
            c.draw.rectangle((24, 135, 378, 923), fill=c.accent)
            photo(c, image_url(model.avatar), (56, 167, 346, 457), assets)
            c.text(56, 490, context.owner.name, size=48, fill="#22252B", bold=True, width=280)
            c.text(56, 615, f"UID {context.owner.game_uid}", size=26, fill="#22252B", width=280)
            c.text(
                56, 668, c.t("Authority") + f"  {model.authority_level}", size=26, fill="#22252B", width=280
            )
            tile_x, tile_y, tile_w, tile_h, step = 406, 290, 268, 290, 282
        else:
            c.panel((42, 144, 1558, 300))
            photo(c, image_url(model.avatar), (60, 159, 186, 285), assets)
            c.text(209, 161, context.owner.name, size=43, bold=True, width=510)
            c.text(209, 221, f"UID {context.owner.game_uid}", size=24, fill=c.muted)
            c.text(801, 171, c.t("Authority"), size=22, fill=c.muted)
            c.text(801, 206, model.authority_level, size=44, bold=True)
            c.text(1090, 171, c.t("World level"), size=22, fill=c.muted)
            c.text(1090, 206, model.world_level, size=44, bold=True)
            tile_x, tile_y, tile_w, tile_h, step = 42, 400, 362, 240, 384
        scope = c.t("Owned roster") if context.source_scope == "owner" else c.t("Public showcase")
        count = (
            f"{len(model.characters)} supplied"
            if context.source_scope == "owner"
            else f"{len(model.characters)}/8"
        )
        c.text(tile_x, tile_y - 72, f"{scope}  ·  {count}", size=27, bold=True)
        for col, key in enumerate(("characters", "weapons", "documents", "achievements")):
            if key not in model.counts.model_fields_set:
                continue
            if variant == "identity":
                c.text(56, 730 + col * 39, key.title(), size=17, fill="#22252B", width=208, max_lines=1)
                c.text(
                    278,
                    730 + col * 39,
                    getattr(model.counts, key),
                    size=19,
                    bold=True,
                    fill="#22252B",
                    width=66,
                    max_lines=1,
                )
            else:
                px = 786 + col * 194
                c.text(px, 328, key.title(), size=17, fill=c.muted, width=180, max_lines=1)
                c.text(px, 354, getattr(model.counts, key), size=27, bold=True, width=180, max_lines=1)
        if not group:
            c.panel((tile_x, tile_y, 1558, 879))
            c.text(tile_x + 30, tile_y + 90, c.t("No characters supplied"), size=36, width=900)
        for j, character in enumerate(group):
            row, col = divmod(j, 4)
            x, y = tile_x + col * step, tile_y + row * (tile_h + 24)
            c.panel((x, y, x + tile_w, y + tile_h))
            portrait_h = tile_h - 76
            photo(
                c,
                image_url(character.images.portrait) or image_url(character.images.avatar),
                (x + 1, y + 1, x + tile_w - 1, y + portrait_h),
                assets,
            )
            c.draw.rectangle((x + 1, y + portrait_h, x + tile_w - 1, y + tile_h - 1), fill=c.panel_color)
            c.draw.rectangle((x + 1, y + tile_h - 5, x + tile_w - 1, y + tile_h), fill=c.accent)
            c.text(
                x + 12, y + portrait_h + 5, character.name, size=23, bold=True, width=tile_w - 24, max_lines=1
            )
            c.text(
                x + 12,
                y + portrait_h + 39,
                f"Lv {character.level}/{character.max_level}   P{character.potential}",
                size=19,
            )
            c.icon("profession." + character.profession.key, x + tile_w - 72, y + portrait_h + 39, 23)
            c.icon("element." + character.element.key, x + tile_w - 38, y + portrait_h + 39, 23)
        for index, medal in enumerate(model.medals[:8]):
            c.icon(image_url(medal.icon) or "", 48 + index * 36, 899, 25)
        if model.regions:
            text = " · ".join(f"{region.name} Lv {region.level}" for region in model.regions)
            c.text(600, 900, text, size=16, fill=c.muted, width=940, max_lines=1)
        canvases.append(c)
    pages = [canvas.finish(index + 1, len(canvases)) for index, canvas in enumerate(canvases)]
    if not details:
        return pages
    records: list[Record] = []
    profile_lines = [
        f"{name.title()}: {getattr(model.counts, name) if name in model.counts.model_fields_set else 'Unavailable'}"
        for name in ("characters", "weapons", "documents", "achievements")
    ]
    for label, value in (
        ("Biography", model.biography),
        ("Mission", model.mission),
        ("Server", model.server_name),
        ("Experience", model.experience),
        ("Created", stamp(model.created_at)),
        ("Last login", stamp(model.last_login_at)),
    ):
        if value is not None and value != "":
            profile_lines.append(f"{label}: {value}")
    records.append(Record("Profile information", profile_lines))
    for character in model.characters:
        records.append(
            Record(
                character.name or character.identity.skport_id,
                [
                    f"Level {character.level}/{character.max_level} · Evolution {character.evolution} · Potential {character.potential}",
                    character.profession.name,
                    character.element.name,
                ],
            )
        )
    for medal in model.medals:
        records.append(
            Record(
                medal.name or medal.id,
                [
                    f"Level {medal.level} · {'Plated' if medal.plated else 'Standard'}",
                    f"Obtained: {stamp(medal.obtained_at)}",
                ],
                "player.medals",
                [(image_url(medal.icon), medal.name)],
            )
        )
    for region in model.regions:
        lines = [f"Level {region.level} · Funds {region.funds.current:g}/{region.funds.maximum:g}"]
        for area in region.areas:
            lines.append(area.name or area.id)
            for counter in area.counters:
                lines.append(f"{counter.name or counter.key}: {counter.current:g}/{counter.maximum:g}")
                if counter.note:
                    lines.append(counter.note)
        records.append(Record(region.name or region.id, lines, "player.exploration"))
    pages.extend(
        render_records(
            "Profile information",
            context,
            records,
            variant="dark" if variant == "operations" else "light",
            assets=assets,
            size=(1600, 1000),
            page_offset=len(pages),
        )
    )
    total = len(pages)
    for index, image in enumerate(pages):
        footer = PageCanvas("Profile", context, dark=variant == "operations", size=image.size)
        footer.image = image
        footer.draw = ImageDraw.Draw(image)
        footer.finish(index + 1, total)
    return pages
