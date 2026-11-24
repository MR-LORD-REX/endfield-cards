"""Monument event boards keep source statuses and teams concise and bounded."""

from datetime import UTC, datetime

import pytest
from PIL import Image
from skport.games.endfield.models import (
    CharacterImages,
    EnemySummary,
    EventStage,
    ImageLinks,
    MedalSummary,
    MonumentEvent,
    MonumentState,
    PlayerIdentity,
    SemanticLabel,
    StageRun,
    TeamMember,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import DataValidationError
from endfield_cards.rendering.templates import monument_detail
from endfield_cards.rendering.templates.monument_detail import _shared as parts
from endfield_cards.utils.drawing import PageCanvas


def link(name):
    return ImageLinks(skport=f"https://monument-detail.example.test/{name}.png")


def state(count=6):
    player = PlayerIdentity(name="Detail Owner", game_uid="1234567890", skport_id="owner")
    team = [
        TeamMember(
            character_id=f"char-{index}",
            name=f"Operator {index + 1}",
            level=90 - index,
            element=SemanticLabel(key="fire", name="Heat"),
            profession=SemanticLabel(key="caster", name="Caster"),
            potential=index,
            evolution=2,
            images=CharacterImages(portrait=link(f"portrait-{index}")),
        )
        for index in range(4)
    ]
    return MonumentState(
        player=player,
        events=[
            MonumentEvent(
                id="event",
                name="Howlers of the Crag",
                is_active=True,
                poster=link("poster"),
                medal=MedalSummary(level=3, plated=True, icon=link("medal")),
                rules=["Enemies are resistant to stagger.", "Defeat all enemies to clear the stage."],
                stages=[
                    EventStage(
                        id=f"stage-{index}",
                        name=f"Observed stage {index + 1}",
                        recommended_level=80,
                        enemies=[EnemySummary(name="Observed enemy", icon=link("enemy"))],
                        normal_cleared=True,
                        hard_cleared=index == 0,
                        normal=StageRun(completed=True, duration_seconds=62.25, team=team),
                        hard=StageRun(completed=True, duration_seconds=71.5, team=team[:3])
                        if index == 0
                        else None,
                    )
                    for index in range(count)
                ],
            )
        ],
    )


@pytest.fixture
def drawn(monkeypatch):
    results = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        results.append((str(value), x, y, height, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return results


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_six_stage_board_retains_times_names_and_source_art_without_mutation(variant, drawn):
    model = state()
    assets = {url: Image.new("RGBA", (240, 300), (74, 123, 183, 255)) for url in parts.urls(model)}
    original = model.model_dump()
    pixels = {url: image.tobytes() for url, image in assets.items()}
    pages = monument_detail.render(model, context_for(model), variant=variant, assets=assets)
    assert len(pages) == 1 and pages[0].width == 1600 and pages[0].height < 2000
    text = "\n".join(value for value, *_ in drawn)
    assert all(stage.name in text for stage in model.events[0].stages)
    assert all(member.name in text for member in model.events[0].stages[0].normal.team)
    assert "01:02.25" in text and "01:11.50" in text
    assert "Cleared" in text and "Not cleared" in text
    assert "HARD CLEAR TEAM" in text and "NORMAL TEAM" in text
    assert "akef-cards" in text and "endfield-cards" in text and "UID 1234567890" in text
    assert all(0 <= y and y + height <= bottom for _, _, y, height, bottom in drawn)
    assert model.model_dump() == original
    assert pixels == {url: image.tobytes() for url, image in assets.items()}
    pages[0].close()
    for image in assets.values():
        image.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_missing_flags_and_times_never_become_zero_or_false_clears(variant, drawn):
    model = state(1)
    model.events[0].stages = [EventStage(name="Unknown stage")]
    pages = monument_detail.render(model, context_for(model), variant=variant)
    text = "\n".join(value for value, *_ in drawn)
    assert "Unknown" in text and "TEAM NOT SUPPLIED" in text
    assert "Not cleared" not in text and "00:00" not in text and "Lv 0" not in text
    assert parts.cleared(model.events[0].stages[0], "normal") is None
    assert "0/1 · 1 unknown" in text
    pages[0].close()


def test_zero_is_an_observed_duration_and_partial_run_is_not_a_clear(drawn):
    model = state(1)
    model.events[0].stages = [EventStage(name="Attempt", normal=StageRun(duration_seconds=0))]
    pages = monument_detail.render(model, context_for(model))
    text = "\n".join(value for value, *_ in drawn)
    assert "00:00.00" in text and "NORMAL RECORDED TEAM" in text and "Unknown" in text
    assert parts.cleared(model.events[0].stages[0], "normal") is None
    pages[0].close()


def test_difficulty_labels_have_no_leading_icons(monkeypatch, drawn):
    model = state(1)
    c = PageCanvas("Stage", context_for(model), header=False)
    calls = []
    monkeypatch.setattr(c, "icon", lambda *args, **kwargs: calls.append(args))
    parts.draw_record(c, model.events[0].stages[0], "normal", 30, 50, 650)
    parts.draw_record(c, model.events[0].stages[0], "hard", 30, 90, 650)
    assert calls == []
    assert [(value, x) for value, x, *_ in drawn if value in {"NORMAL", "HARD"}] == [
        ("NORMAL", 30),
        ("HARD", 30),
    ]
    c.image.close()


def test_medal_is_centered_without_level_caption_and_source_pixels_are_unchanged(drawn):
    model = state(1)
    event = model.events[0]
    event.medal.plated = False
    source = Image.new("RGBA", (20, 40), "#0000FF")
    original = source.tobytes()
    c = PageCanvas("Medal", context_for(model), assets={event.medal.icon.url: source}, header=False)
    parts.draw_medal(c, event, (200, 100, 300, 202))
    blue = c.image.crop((200, 100, 300, 202)).getchannel("B").point(lambda value: 255 if value > 200 else 0)
    left, top, right, bottom = blue.getbbox()
    assert abs((left + right) / 2 - 50) <= 1 and abs((top + bottom) / 2 - 51) <= 1
    assert not any(value.startswith("Lv ") for value, *_ in drawn)
    assert source.tobytes() == original
    c.image.close()
    source.close()


def test_matching_source_teams_use_clear_dates_instead_of_duplicate_names(drawn):
    model = state(1)
    stage = model.events[0].stages[0]
    stage.hard.team = list(stage.normal.team)
    stage.normal.completed_at = datetime(2026, 10, 26, 6, 1, tzinfo=UTC)
    stage.hard.completed_at = datetime(2026, 11, 1, 8, 17, tzinfo=UTC)
    pages = monument_detail.render(model, context_for(model))
    text = "\n".join(value for value, *_ in drawn)
    assert "Hard 01 Nov 2026 · 08:17 UTC" in text and "Normal 26 Oct 2026 · 06:01 UTC" in text
    assert "NORMAL TEAM  " not in text
    assert all(member.name in text for member in stage.normal.team)
    pages[0].close()


def test_changed_progression_keeps_alternate_team_visible(drawn):
    model = state(1)
    stage = model.events[0].stages[0]
    stage.hard.team = [member.model_copy(deep=True) for member in stage.normal.team]
    stage.hard.team[0].level = 80
    pages = monument_detail.render(model, context_for(model))
    assert "NORMAL TEAM  " in "\n".join(value for value, *_ in drawn)
    pages[0].close()


def test_false_active_flag_uses_observed_hard_clear_badge_without_archival_claim(drawn):
    model = state(1)
    model.events[0].is_active = False
    pages = monument_detail.render(model, context_for(model))
    text = "\n".join(value for value, *_ in drawn)
    assert "HARD 1/1" in text and "ARCHIVED" not in text and "ACTIVE" not in text
    pages[0].close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_only_large_selected_stage_sets_paginate_in_source_order(variant, drawn):
    model = state(7)
    pages = monument_detail.render(model, context_for(model), variant=variant)
    assert len(pages) == 2
    names = [value for value, *_ in drawn if "Observed stage" in value]
    assert names == [f"{index + 1:02d}  Observed stage {index + 1}" for index in range(7)]
    assert "01 / 02" in "\n".join(value for value, *_ in drawn)
    assert "02 / 02" in "\n".join(value for value, *_ in drawn)
    for page in pages:
        page.close()


def test_default_selects_active_event_and_explicit_id_selects_only_that_history(drawn):
    model = state(1)
    model.events.insert(0, MonumentEvent(id="archived", name="Archived event", is_active=False))
    pages = monument_detail.render(model, context_for(model))
    assert len(pages) == 1 and "Archived event" not in "\n".join(value for value, *_ in drawn)
    pages[0].close()
    drawn.clear()
    pages = monument_detail.render(model, context_for(model), event_id="archived")
    text = "\n".join(value for value, *_ in drawn)
    assert "Archived event" in text and "Howlers of the Crag" not in text
    pages[0].close()


def test_default_falls_back_to_latest_source_start_even_if_events_are_unordered(drawn):
    model = state(1)
    model.events[0].is_active = False
    model.events[0].starts_at = datetime(2026, 10, 1, tzinfo=UTC)
    model.events.insert(
        0, MonumentEvent(id="old", name="Older event", starts_at=datetime(2026, 9, 1, tzinfo=UTC))
    )
    model.events.append(
        MonumentEvent(id="latest", name="Latest event", starts_at=datetime(2026, 11, 1, tzinfo=UTC))
    )
    pages = monument_detail.render(model, context_for(model))
    text = "\n".join(value for value, *_ in drawn)
    assert "Latest event" in text and "Older event" not in text and "Howlers of the Crag" not in text
    pages[0].close()


def test_selectors_and_duplicate_stage_ids_fail_before_drawing(monkeypatch):
    model = state(2)

    def unexpected(*args, **kwargs):
        raise AssertionError("Validation must precede drawing")

    monkeypatch.setattr(parts, "render_page", unexpected)
    with pytest.raises(DataValidationError, match="absent"):
        monument_detail.render(model, context_for(model), event_id="missing")
    model.events[0].stages[1].id = model.events[0].stages[0].id
    with pytest.raises(DataValidationError, match="duplicate"):
        monument_detail.render(model, context_for(model))


def test_long_rules_are_bounded_before_font_measurement_and_favor_source_mechanics(drawn):
    rules = ["Flavor paragraph " * 5000, "- Actual first mechanic " * 2000, "- Second mechanic."]
    original = list(rules)
    preview = parts.compact_rules(rules)
    assert len(preview) <= 380 and preview.startswith("Actual first mechanic")
    assert "Second mechanic." in preview and "Flavor paragraph" not in preview and "+1 more" in preview
    assert rules == original
    model = state(1)
    model.events[0].rules = rules
    pages = monument_detail.render(model, context_for(model))
    measured = [value for value, *_ in drawn if value.startswith("Actual first mechanic")]
    assert len(measured) == 1 and len(measured[0]) <= 380
    pages[0].close()


def test_unavailable_portrait_uses_avatar_pixels_and_known_semantic_keys_avoid_remote_icons():
    member = state(1).events[0].stages[0].normal.team[0]
    member.images.avatar = link("available-avatar")
    member.element.icons = link("remote-element")
    member.profession.icons = link("remote-profession")

    class Assets(dict):
        def __init__(self):
            super().__init__({member.images.avatar.url: Image.new("RGBA", (50, 70), "#F04020")})
            self.requested = []

        def get(self, key, default=None):
            self.requested.append(key)
            return super().get(key, default)

    assets = Assets()
    c = PageCanvas("Fixture", context_for(state()), assets=assets)
    parts.draw_member(c, member, (50, 160, 230, 330))
    assert member.images.portrait.url in assets.requested and member.images.avatar.url in assets.requested
    assert (
        member.element.icons.url not in assets.requested
        and member.profession.icons.url not in assets.requested
    )
    assert c.image.getpixel((130, 210))[:3] == (240, 64, 32)
    c.image.close()
    for image in assets.values():
        image.close()


def test_unknown_semantic_key_uses_supplied_icon_fallback():
    member = state(1).events[0].stages[0].normal.team[0]
    member.element = SemanticLabel(key="future-element", icons=link("new-element"))
    assets = {member.element.icons.url: Image.new("RGBA", (20, 20), "#F04020")}
    c = PageCanvas("Fixture", context_for(state()), assets=assets)
    parts.draw_member(c, member, (50, 160, 230, 330))
    assert c.image.getpixel((67, 178))[:3] == (240, 64, 32)
    c.image.close()
    for image in assets.values():
        image.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_long_labels_rules_and_source_date_stay_inside_board(variant, drawn):
    model = state(4)
    event = model.events[0]
    event.name = "極めて長いイベントの名前" * 30
    event.rules = ["Source mechanic " * 150]
    event.ends_at = datetime(2026, 11, 25, 14, tzinfo=UTC)
    for stage in event.stages:
        stage.name = "長いステージの名前" * 30
    pages = monument_detail.render(model, context_for(model, locale="ja"), variant=variant)
    assert len(pages) == 1
    assert all(0 <= y and y + height <= bottom for _, _, y, height, bottom in drawn)
    assert "Ends 25 Nov 2026 · 14:00 UTC" in "\n".join(value for value, *_ in drawn)
    pages[0].close()
