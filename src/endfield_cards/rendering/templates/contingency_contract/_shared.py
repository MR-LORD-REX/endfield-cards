"""A concise contract showcase preserving missions, medal, art and encounter."""

from collections.abc import Iterator
from dataclasses import replace
from importlib import import_module
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url, validate_owner
from endfield_cards.errors import DataValidationError
from endfield_cards.utils.drawing import PageCanvas
from endfield_cards.utils.images import composite_fitted, fitted, gradient_alpha, masked, shape_mask
from endfield_cards.utils.meters import bar, ring
from endfield_cards.utils.records import Record, duration, iter_records, meter_text, record_page_count
from endfield_cards.utils.time import display_time

SIZE = (1600, 1000)
Box = tuple[int, int, int, int]


def contracts(model: Any) -> list[Any]:
    if not hasattr(model, "contracts"):
        return [model]
    source_ids = [item.id for item in model.contracts if item.id]
    if len(set(source_ids)) != len(source_ids):
        raise DataValidationError("Contract contains duplicate identities", code="duplicate_contract")
    entries = [model.current] if model.current is not None else []
    entries.extend(
        item for item in model.contracts if all(item.id != entry.id or not item.id for entry in entries)
    )
    identifiers = [item.id for item in entries if item.id]
    if len(set(identifiers)) != len(identifiers):
        raise DataValidationError("Contract contains duplicate identities", code="duplicate_contract")
    return entries


def selected(model: Any, contract_id: str | None = None) -> Any:
    entries = contracts(model)
    if contract_id is not None:
        entries = [item for item in entries if item.id == str(contract_id)]
        if not entries:
            raise DataValidationError(
                "Selected Contingency Contract is absent from this snapshot", code="contract_not_found"
            )
    return entries[0] if entries else None


def urls(model: Any) -> set[str]:
    links = []
    for item in contracts(model):
        links.append(image_url(item.poster))
        if item.medal is not None:
            links.append(image_url(item.medal.icon))
        links.extend(image_url(enemy.icon) for enemy in item.enemies[:8])
    return {url for url in links if url}


def text(c: PageCanvas, x: int, y: int, value: object, width: int, *, size: int = 20, **options: Any) -> None:
    c.text(x, y, value, width=width, size=size, max_lines=options.pop("max_lines", 1), **options)


def new_canvas(context: Any, *, dark: bool, assets: Any) -> PageCanvas:
    return PageCanvas(
        "Contingency Contract",
        replace(context, display_timezone="UTC"),
        dark=dark,
        size=SIZE,
        assets=assets,
        header=False,
    )


def owner_header(c: PageCanvas, profile: Any = None) -> None:
    url = image_url(profile.avatar) if profile is not None else None
    source = c.assets.get(url) if url else None
    c.draw.ellipse((38, 32, 131, 125), fill=c.accent)
    if source is not None:
        composite_fitted(c.image, source, (43, 37, 126, 120), shape="circle", focus=(0.5, 0.25))
    else:
        c.draw.ellipse((43, 37, 126, 120), fill=c.panel_color)
        text(c, 65, 51, c.context.owner.name[:1], 55, size=41, bold=True)
    text(c, 151, 34, c.context.owner.name, 858, size=44, bold=True)
    identity = f"UID {c.context.owner.game_uid}"
    if profile is not None:
        if profile.server_name:
            identity += " · " + profile.server_name
        if "authority_level" in profile.model_fields_set:
            identity += f" · Authority {profile.authority_level}"
    text(c, 153, 96, identity, 857, size=19, fill=c.muted)
    c.icon("player.contingency-contract", 1045, 54, 31, tint=c.accent if c.dark else "#916900")
    text(c, 1088, 58, "CONTINGENCY CONTRACT", 470, size=23, bold=True)


def hero(c: PageCanvas, item: Any, box: Box, *, full: bool = False) -> None:
    x, y, right, bottom = box
    size = right - x, bottom - y
    url = image_url(item.poster)
    source = c.assets.get(url) if url else None
    tile = (
        fitted(source, size, focus=(0.55, 0.4)) if source is not None else Image.new("RGBA", size, "#24303A")
    )
    shade = Image.new("RGBA", size, "#101822")
    shade.putalpha(gradient_alpha(size, start=0.0, end=0.93, maximum=235, vertical=False, reverse=True))
    tile.alpha_composite(shade)
    if full:
        floor = Image.new("RGBA", size, "#181B20")
        floor.putalpha(gradient_alpha(size, start=0.38, end=1, maximum=255))
        tile.alpha_composite(floor)
    c.image.alpha_composite(
        masked(tile, shape_mask(size, shape="rectangle" if full else "rounded", radius=16)), (x, y)
    )


def title(c: PageCanvas, item: Any, box: Box) -> None:
    x, y, right, bottom = box
    text(c, x, y, "OPERATION", right - x, size=17, bold=True, fill=c.accent)
    name = item.name.removeprefix("Contingency Contract:").strip() or item.id or "Unavailable"
    text(c, x - 1, y + 34, name, right - x, size=43, bold=True, fill="#F4F5F7", max_lines=2)
    stage = getattr(item, "stage_name", "")
    if stage and stage != "Contingency Contract":
        text(c, x, bottom - 33, stage, right - x, size=18, fill="#BBC5CF")


def medal(c: PageCanvas, item: Any, box: Box) -> None:
    x, y, right, bottom = box
    value = item.medal
    if value is None:
        text(c, x, y + 18, "Medal unavailable", right - x, size=16, fill=c.muted)
        return
    url = image_url(value.icon)
    source = c.assets.get(url) if url else None
    size = min(right - x, bottom - y - 30)
    if source is not None:
        glyph = fitted(source, (size, size), contain=True)
        if value.level == 0:
            glyph.putalpha(glyph.getchannel("A").point(lambda alpha: alpha // 2))
        c.image.alpha_composite(glyph, (x + (right - x - size) // 2, y))
    status = (
        f"Medal Lv {value.level}" + (" · Plated" if value.plated else "")
        if value.level > 0
        else "Not earned yet"
    )
    text(c, x, bottom - 26, status, right - x, size=15, fill=c.muted, max_lines=1)


def score(c: PageCanvas, item: Any, box: Box) -> None:
    x, y, right, bottom = box
    c.panel(box)
    text(c, x + 23, y + 21, "BEST SCORE", right - x - 46, size=16, bold=True, fill=c.muted)
    value = str(item.best_score) if "best_score" in item.model_fields_set else "—"
    text(c, x + 20, y + 55, value, 252, size=110, bold=True, fill=c.accent if c.dark else c.fg)
    attempts = str(item.attempts) if "attempts" in item.model_fields_set else "—"
    text(c, x + 24, bottom - 53, f"{attempts} attempts", right - x - 48, size=20, fill=c.muted)
    medal(c, item, (right - 164, y + 24, right - 16, y + 207))


def missions(c: PageCanvas, item: Any, box: Box, *, radial: bool) -> None:
    x, y, right, bottom = box
    c.panel(box)
    values = item.missions[:6]
    if not values:
        text(c, x + 22, y + 26, "Mission progress unavailable", right - x - 44, size=24, fill=c.muted)
        return
    if radial:
        columns = min(3, len(values))
        rows = (len(values) + columns - 1) // columns
        cell_w, cell_h = (right - x - 30) // columns, (bottom - y - 22) // rows
        for index, meter in enumerate(values):
            row, column = divmod(index, columns)
            px, py = x + 15 + column * cell_w, y + 11 + row * cell_h
            size = min(114, cell_h - 34)
            gx, gy = px + (cell_w - size) // 2, py + max(0, (cell_h - size - 31) // 2)
            ring(c, gx, gy, size, meter.ratio)
            inset = max(11, min(18, size // 7))
            c.centered_text(
                (gx + inset, gy + inset, gx + size - inset, gy + size - inset),
                meter_text(meter),
                size=29 if size >= 100 else 17,
                bold=True,
            )
            c.centered_text(
                (px + 7, gy + size + 9, px + cell_w - 7, gy + size + 31),
                meter.name or meter.key,
                size=17 if size >= 100 else 14,
                bold=True,
            )
        if len(item.missions) > len(values):
            text(
                c,
                x + 22,
                bottom - 22,
                f"+{len(item.missions) - len(values)} missions",
                right - x - 44,
                size=12,
                fill=c.muted,
            )
        return
    step = min(100, (bottom - y - 22) // len(values))
    for index, meter in enumerate(values):
        py = y + 13 + index * step
        text(
            c,
            x + 22,
            py + 1,
            meter.name or meter.key,
            (right - x) * 2 // 3,
            size=min(21, step - 27),
            bold=True,
        )
        text(c, right - 191, py + 1, meter_text(meter), 169, size=min(31, step - 20), bold=True)
        bar(c, (x + 22, py + step - 13, right - 22, py + step - 6), meter.ratio)
    if len(item.missions) > len(values):
        text(
            c,
            x + 22,
            bottom - 18,
            f"+{len(item.missions) - len(values)} missions",
            right - x - 44,
            size=12,
            fill=c.muted,
        )


def encounter(c: PageCanvas, item: Any, box: Box) -> None:
    x, y, right, bottom = box
    c.panel(box)
    text(c, x + 20, y + 13, "ENCOUNTER", right - x - 40, size=17, bold=True)
    enemy_count = str(len(item.enemies)) if len(item.enemies) <= 8 else f"8 / {len(item.enemies)}"
    text(
        c,
        right - 260,
        y + 15,
        f"{enemy_count} enemies · {len(item.modifiers)} indicators",
        239,
        size=13,
        fill=c.muted,
    )
    values = item.enemies[:8]
    if not values:
        text(c, x + 22, y + 77, "Enemy data unavailable", right - x - 44, size=21, fill=c.muted)
        return
    step = (right - x - 34) // len(values)
    for index, enemy in enumerate(values):
        px, py = x + 17 + index * step, y + 48
        url = image_url(enemy.icon)
        source = c.assets.get(url) if url else None
        size = min(76, step - 10)
        if source is not None:
            composite_fitted(
                c.image,
                source,
                (px + (step - size) // 2, py, px + (step + size) // 2, py + size),
                radius=9,
                contain=True,
            )
        text(c, px + 3, py + size + 5, enemy.name or enemy.id, step - 7, size=14, bold=True, max_lines=2)
        if enemy.level is not None:
            text(c, px + 3, bottom - 26, f"Lv {enemy.level}", step - 7, size=12, fill=c.muted)


def schedule(c: PageCanvas, model: Any, item: Any, box: Box) -> None:
    x, y, right, bottom = box
    c.panel(box)
    text(c, x + 21, y + 15, "SCHEDULE / UTC", right - x - 42, size=17, bold=True)
    for index, (label, value) in enumerate(
        (("Gameplay ends", item.ends_at), ("Collection ends", item.ends_at_collection))
    ):
        py = y + 54 + index * 60
        text(c, x + 21, py, label, right - x - 42, size=13, fill=c.muted)
        text(c, x + 21, py + 22, display_time(value, c.context), right - x - 42, size=18, bold=True)
    unlocked = sum(modifier.is_unlocked for modifier in item.modifiers)
    text(
        c,
        x + 21,
        bottom - 30,
        f"Indicators unlocked {unlocked}/{len(item.modifiers)}",
        right - x - 42,
        size=14,
        fill=c.muted,
    )


def history(c: PageCanvas, model: Any, item: Any, box: Box) -> None:
    other = [entry for entry in contracts(model) if entry is not item and entry.id != item.id]
    if other:
        names = " · ".join(
            f"{entry.name.removeprefix('Contingency Contract:').strip()} ({entry.best_score})"
            for entry in other[:3]
        )
        if len(other) > 3:
            names += f" · +{len(other) - 3} contracts"
        text(c, box[0], box[1], "Other contracts: " + names, box[2] - box[0], size=13, fill="#C0C8D2")


def iter_render(
    model: Any,
    context: Any,
    *,
    variant: str = "light",
    assets: dict | None = None,
    profile: Any = None,
    contract_id: str | None = None,
    details: bool = False,
    **options: Any,
) -> Iterator[Image.Image]:
    item = selected(model, contract_id)
    if profile is not None:
        validate_owner(profile, context)
    module = import_module(f"endfield_cards.rendering.templates.contingency_contract.{variant}")
    c = module.draw(model, context, item=item, profile=profile, assets=assets)
    records = []
    if details and item is not None:
        records = [Record(item.name or item.id, [item.rules, f"Contract ID: {item.id}"])]
        records.extend(
            Record(meter.name or meter.key, [meter_text(meter), meter.note]) for meter in item.missions
        )
        records.extend(
            Record(modifier.name or modifier.id, [modifier.description, f"Score {modifier.score}"])
            for modifier in item.modifiers
        )
        records.extend(
            Record(enemy.name or enemy.id, [enemy.description, enemy.ability or ""]) for enemy in item.enemies
        )
        records.extend(Record(run.id or "Run", [duration(run.duration_seconds)]) for run in item.runs)
    total = 1 + (record_page_count(context, records) if records else 0)
    yield c.finish(1, total)
    if records:
        yield from iter_records(
            "Contingency Contract details",
            context,
            records,
            variant=variant,
            assets=assets,
            page_offset=1,
            total_pages=total,
        )


def render(model: Any, context: Any, **options: Any) -> list[Image.Image]:
    return list(iter_render(model, context, **options))
