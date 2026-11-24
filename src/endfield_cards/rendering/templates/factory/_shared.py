"""Regional, settlement, exploration and cabin records with bounded continuation."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from PIL import Image

from endfield_cards.adapters.skport import image_url
from endfield_cards.utils.records import Record, append_model_text, iter_records, meter_text, stamp


def urls(model: Any) -> set[str]:
    links = [
        image_url(item.officer.icon)
        for region in model.regions
        for item in region.settlements
        if item.officer is not None
    ]
    links.extend(image_url(member.icon) for cabin in model.cabins for member in cabin.crew)
    return {link for link in links if link}


def iter_render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> Iterator[Image.Image]:
    records = []
    for region in model.regions:
        lines = [f"Region level: {region.level}", f"Funds: {meter_text(region.funds)}"]
        if region.funds.recovery_at:
            lines.append("Funds recover: " + stamp(region.funds.recovery_at))
        if region.factory:
            append_model_text(lines, region.factory)
        records.append(Record(region.name or region.id, lines, "player.factory"))
        for settlement in region.settlements:
            lines = [
                f"Region: {region.name or region.id}",
                f"Level: {settlement.level}" + (" · Maximum level" if settlement.maximum_level else ""),
                f"Experience: {meter_text(settlement.experience)}",
                f"Stock: {meter_text(settlement.stock)}",
            ]
            images = []
            if settlement.officer is not None:
                lines.append(f"Officer: {settlement.officer.name or settlement.officer.id}")
                images.append(
                    (image_url(settlement.officer.icon), settlement.officer.name or settlement.officer.id)
                )
                if settlement.officer.description:
                    lines.append(settlement.officer.description)
            if settlement.last_tick_at:
                lines.append("Last update: " + stamp(settlement.last_tick_at))
            for meter in (settlement.experience, settlement.stock):
                if meter.note:
                    lines.append(meter.note)
                if meter.recovery_at:
                    lines.append("Recovery: " + stamp(meter.recovery_at))
            records.append(Record(settlement.name or settlement.id, lines, "player.development", images))
        for area in region.areas:
            lines = [f"Region: {region.name or region.id}"]
            for counter in area.counters:
                lines.append(f"{counter.name or counter.key}: {meter_text(counter)}")
                if counter.note:
                    lines.append(counter.note)
            records.append(Record(area.name or area.id, lines, "player.exploration"))
    for cabin in model.cabins:
        lines = [f"Cabin level: {cabin.level}"]
        images = []
        for member in cabin.crew:
            detail = [member.name or member.id]
            if member.physical_strength is not None:
                detail.append(f"Stamina {member.physical_strength:g}")
            if member.favorability is not None:
                detail.append(f"Favorability {member.favorability:g}")
            lines.append(" · ".join(detail))
            if member.description:
                lines.append(member.description)
            images.append((image_url(member.icon), member.name or member.id))
        if not cabin.crew:
            lines.append("No assigned crew supplied")
        append_model_text(lines, cabin.reports)
        records.append(Record(cabin.name or cabin.id, lines, "player.factory", images))
    yield from iter_records("FACTORY", context, records, variant=variant, assets=assets)


def render(
    model: Any, context: Any, *, variant: str = "light", assets: dict | None = None, **options: Any
) -> list[Image.Image]:
    """Collect the explicitly requested render batch."""
    return list(iter_render(model, context, variant=variant, assets=assets, **options))
