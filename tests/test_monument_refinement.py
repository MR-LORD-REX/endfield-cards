"""Monument overview keeps source artwork, stage selectors and observed clears."""

import pytest
from PIL import Image
from skport.games.endfield.models import (
    EventStage,
    ImageLinks,
    MedalSummary,
    MonumentEvent,
    MonumentState,
    PlayerCard,
    PlayerIdentity,
    StageRun,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import DataValidationError, OwnerMismatchError
from endfield_cards.rendering.templates import monument
from endfield_cards.rendering.templates.monument import _shared as parts
from endfield_cards.utils.drawing import PageCanvas


def link(name):
    return ImageLinks(skport=f"https://monument.example.test/{name}.png")


def state(count=8):
    owner = PlayerIdentity(skport_id="social-owner", name="Monument Owner", game_uid="4572346170")
    return MonumentState(
        player=owner,
        events=[
            MonumentEvent(
                id=f"event-{index}",
                name=f"Observed event {index}",
                poster=link(f"poster-{index}"),
                is_active=index == 7,
                medal=MedalSummary(
                    name=f"Observed medal {index}",
                    level=8 if index == 0 else 0,
                    plated=index == 0,
                    icon=link(f"medal-{index}"),
                ),
                stages=[
                    EventStage(
                        id=f"stage-{index}-{stage}",
                        name=f"Observed stage {index}-{stage}",
                        normal_id=f"normal-{index}-{stage}",
                        hard_id=f"hard-{index}-{stage}",
                        normal_cleared=stage % 2 == 0,
                        hard_cleared=stage == 1,
                        normal=StageRun(completed=True, duration_seconds=62.25) if stage == 0 else None,
                        hard=StageRun(completed=True, duration_seconds=70.5) if stage == 1 else None,
                    )
                    for stage in range(6)
                ],
            )
            for index in range(count)
        ],
    )


@pytest.fixture
def drawn(monkeypatch):
    entries = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        entries.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return entries


class Images(dict):
    def __init__(self, model):
        self.requested = []
        self.sources = {url: Image.new("RGBA", (250, 330), (54, 121, 174, 220)) for url in parts.urls(model)}
        super().__init__(self.sources)

    def get(self, key, default=None):
        self.requested.append(key)
        return super().get(key, default)

    def close(self):
        for image in self.sources.values():
            image.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_full_monument_is_one_image_with_all_stage_names_and_source_icons(variant, drawn):
    model = state()
    originals = model.model_dump()
    images = Images(model)
    pixels = {key: image.tobytes() for key, image in images.items()}
    pages = monument.render(model, context_for(model), variant=variant, assets=images)
    assert len(pages) == 1 and pages[0].size == (1600, 1500)
    text = "\n".join(entry[0] for entry in drawn)
    assert all(event.name in text for event in model.events)
    assert all(stage.name in text for event in model.events for stage in event.stages)
    assert "Normal 3/6" in text and "Hard 1/6" in text and "24/48" in text and "8/48" in text
    assert "Fastest clear 01:02.25" in text and "Lv 8 · P" in text and "ACTIVE" in text
    assert "Monument Owner" in text and "UID 4572346170" in text
    assert "akef-cards" in text and "endfield-cards" in text
    assert all(image_url in images.requested for image_url in parts.urls(model))
    assert all(0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in drawn)
    assert model.model_dump() == originals
    assert pixels == {key: image.tobytes() for key, image in images.items()}
    pages[0].close()
    images.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_missing_medal_and_clear_time_remain_unavailable(variant, drawn):
    model = state(1)
    model.events[0].medal = None
    model.events[0].stages = [EventStage(id="unknown", name="Supplied stage", normal_cleared=True)]
    pages = monument.render(model, context_for(model), variant=variant)
    text = "\n".join(entry[0] for entry in drawn)
    assert "Clear time unavailable" in text and "Fastest clear 00:00" not in text
    assert "Normal 1/1" in text and "Hard 0/1" in text and "Lv 0" not in text
    assert parts.totals(model.events)[-1] == ("EARNED MEDALS", "—")
    pages[0].close()


def test_fastest_uses_completed_observed_runs_and_preserves_zero():
    model = state(1)
    event = model.events[0]
    event.stages = [
        EventStage(normal=StageRun(duration_seconds=1), hard=StageRun(duration_seconds=0, completed=True))
    ]
    assert parts.fastest(event) == 0
    event.stages[0].hard = None
    assert parts.fastest(event) is None


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_large_collection_paginates_only_beyond_twelve(variant, drawn):
    model = state(13)
    pages = monument.render(model, context_for(model), variant=variant)
    assert len(pages) == 2
    names = [value for value, *_ in drawn if value.startswith("Observed event ")]
    assert names == [event.name for event in model.events]
    assert all(page.width == 1600 and page.height <= 2110 for page in pages)
    for page in pages:
        page.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_stage_overflow_and_long_names_keep_single_default_card(variant, drawn):
    model = state(1)
    model.events[0].name = "Very long observed event " * 20
    model.events[0].stages.extend(EventStage(name=f"Additional stage {index}") for index in range(20))
    pages = monument.render(model, context_for(model), variant=variant)
    assert len(pages) == 1
    assert "+21 stages" in "\n".join(entry[0] for entry in drawn)
    assert all(0 <= y and y + height <= bottom for _, _, y, height, _, bottom in drawn)
    pages[0].close()


def test_explicit_details_keep_full_selector_ids(drawn):
    model = state(1)
    pages = monument.render(model, context_for(model), details=True)
    text = "\n".join(entry[0] for entry in drawn)
    assert len(pages) > 1 and "normal-0-5" in text and "hard-0-5" in text and "stage-0-5" in text
    for page in pages:
        page.close()


def test_duplicate_event_ids_are_rejected_before_canvas(monkeypatch):
    model = state(2)
    model.events[1].id = model.events[0].id

    def unexpected(*args, **options):
        pytest.fail("Duplicate selector identities must be rejected before rendering")

    monkeypatch.setattr(PageCanvas, "__init__", unexpected)
    with pytest.raises(DataValidationError) as error:
        monument.render(model, context_for(model))
    assert error.value.code == "duplicate_event"


def test_profile_owner_is_validated_before_canvas(monkeypatch):
    model = state(1)
    profile = PlayerCard(player=PlayerIdentity(skport_id="other", name="Other", game_uid="other"))

    def unexpected(*args, **options):
        pytest.fail("Invalid profile owner must be rejected before rendering")

    monkeypatch.setattr(PageCanvas, "__init__", unexpected)
    with pytest.raises(OwnerMismatchError):
        monument.render(model, context_for(model), profile=profile)


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_empty_monument_is_bounded(variant, drawn):
    model = state(0)
    pages = monument.render(model, context_for(model), variant=variant)
    assert len(pages) == 1 and pages[0].size == (1600, 700)
    assert "No monument events supplied" in "\n".join(entry[0] for entry in drawn)
    pages[0].close()
