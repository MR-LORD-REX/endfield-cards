"""Detailed contracts compose bounded battle and indicator boards from source records."""

from dataclasses import replace
from datetime import UTC, datetime

import pytest
from PIL import Image
from skport.games.endfield.models import (
    CharacterImages,
    ContractModifier,
    ContractState,
    CrisisContract,
    EnemySummary,
    ImageLinks,
    MedalSummary,
    PlayerCard,
    PlayerIdentity,
    ResourceMeter,
    SemanticLabel,
    StageRun,
    TeamMember,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.errors import DataValidationError, OwnerMismatchError
from endfield_cards.rendering.templates import contingency_contract_detail as detail
from endfield_cards.rendering.templates.contingency_contract_detail import _shared as parts
from endfield_cards.utils.drawing import PageCanvas


def state(*, runs=4, modifiers=8):
    def link(name):
        return ImageLinks(skport=f"https://detail.example.test/{name}.png")

    item = CrisisContract(
        id="current",
        name="Contingency Contract: Indigo Experimental Operation",
        best_score=17,
        attempts=8,
        stage_name="Experimental Command Center",
        stage_recommended_level=70,
        ends_at=datetime(2026, 11, 25, 20, tzinfo=UTC),
        ends_at_collection=datetime(2026, 12, 2, 20, tzinfo=UTC),
        poster=link("poster"),
        medal=MedalSummary(level=2, plated=True, icon=link("medal")),
        missions=[ResourceMeter(name="Weekly", current=9, maximum=7)],
        runs=[
            StageRun(
                id=f"run-{i}",
                score=17 - i,
                duration_seconds=255 + i,
                completed=i != 3,
                waves=3,
                completed_at=datetime(2026, 11, 25, 12, tzinfo=UTC),
                team=[
                    TeamMember(
                        character_id=f"char-{j}",
                        name=f"Operator {j}",
                        level=80 + j,
                        rarity=6,
                        potential=2,
                        evolution=3,
                        element=SemanticLabel(key="char_property_pulse"),
                        profession=SemanticLabel(key="profession_guard"),
                        images=CharacterImages(half_body=link(f"char-{j}")),
                    )
                    for j in range(4)
                ],
            )
            for i in range(runs)
        ],
        modifiers=[
            ContractModifier(
                id=f"modifier-{i}",
                name=f"Observed Indicator {i}",
                score=i,
                is_unlocked=i % 2 == 0,
                icon=link(f"modifier-{i}"),
            )
            for i in range(modifiers)
        ],
        enemies=[
            EnemySummary(id=f"enemy-{i}", name=f"Observed Enemy {i}", level=60, icon=link(f"enemy-{i}"))
            for i in range(7)
        ],
    )
    owner = PlayerIdentity(name="Contract Owner", game_uid="123", skport_id="social")
    return ContractState(player=owner, current=item, contracts=[item])


@pytest.fixture
def drawn(monkeypatch):
    output = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        h = original(self, x, y, value, **options)
        output.append((str(value), x, y, h, self.width, self.height))
        return h

    monkeypatch.setattr(PageCanvas, "text", capture)
    return output


def assets(model):
    source = Image.new("RGBA", (140, 180), (31, 102, 151, 220))
    return {url: source for url in parts.urls(model)}, source


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_detail_shows_score_ranked_teams_indicators_and_enemies_without_mutations(variant, drawn):
    model = state()
    model.current.runs.reverse()
    before = model.model_dump()
    images, source = assets(model)
    pixels = source.tobytes()
    pages = detail.render(model, context_for(model), variant=variant, assets=images)
    text = "\n".join(value for value, *_ in drawn)
    assert len(pages) == 1 and pages[0].width == 2000 and pages[0].height < 1700
    for value in (
        "Indigo Experimental Operation",
        "17",
        "8",
        "9 / 7",
        "04:15",
        "Wave 3",
        "Operator 3",
        "Lv 83",
        "E3",
        "INDICATORS",
        "ENCOUNTER",
        "Medal Lv 2 · Plated",
    ):
        assert value in text
    assert all(value.name in text for value in model.current.enemies)
    assert "akef-cards" in text and "endfield-cards" in text and "UID 123" in text
    assert [run.id for run in parts.ordered_runs(model.current)] == ["run-0", "run-1", "run-2", "run-3"]
    assert all(0 <= x < w and 0 <= y and y + h <= bottom for _, x, y, h, w, bottom in drawn)
    assert source.tobytes() == pixels and model.model_dump() == before
    pages[0].close()
    source.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_no_battles_adapts_into_indicator_board_with_all_39_compact_entries(variant, drawn):
    model = state(runs=0, modifiers=39)
    pages = detail.render(model, context_for(model), variant=variant)
    text = "\n".join(value for value, *_ in drawn)
    assert len(pages) == 1 and pages[0].height < 1500
    assert "No recorded battles" in text and "39 supplied" in text
    assert all(value.name in text for value in model.current.modifiers)
    assert "Team unavailable" not in text
    assert all(0 <= x < w and 0 <= y and y + h <= bottom for _, x, y, h, w, bottom in drawn)
    pages[0].close()


def test_default_shows_top_four_with_explicit_source_count_and_all_runs_is_bounded(drawn):
    model = state(runs=9)
    pages = detail.render(model, context_for(model))
    assert len(pages) == 1 and any("Best 4 of 9" in value for value, *_ in drawn)
    pages[0].close()
    drawn.clear()
    pages = detail.render(model, context_for(model), all_runs=True)
    assert len(pages) == 3 and all(page.width == 2000 for page in pages)
    assert any("Records 9–9 of 9" in value for value, *_ in drawn)
    assert all(0 <= x < w and 0 <= y and y + h <= bottom for _, x, y, h, w, bottom in drawn)
    for page in pages:
        page.close()


def test_missing_source_score_is_not_zero_and_unknown_battle_state_is_not_failed(drawn):
    model = state()
    model.current = CrisisContract(id="current", name="Partial operation", runs=[StageRun(id="unknown")])
    model.contracts = [model.current]
    pages = detail.render(model, context_for(model))
    text = "\n".join(value for value, *_ in drawn)
    assert "—" in text and "Result unavailable" in text and "Team unavailable" in text
    assert "Failed" not in text and "Cleared" not in text
    assert "0 attempts" not in text
    pages[0].close()


def test_only_current_contract_is_shown_by_default_and_explicit_history_can_be_selected(drawn):
    model = state()
    model.contracts.append(CrisisContract(id="historical", name="Old contract"))
    pages = detail.render(model, context_for(model))
    assert len(pages) == 1 and not any(value == "Old contract" for value, *_ in drawn)
    pages[0].close()
    drawn.clear()
    pages = detail.render(model, context_for(model), contract_id="historical")
    assert len(pages) == 1 and any(value == "Old contract" for value, *_ in drawn)
    pages[0].close()


def test_invalid_selector_and_owner_are_rejected_before_allocating_canvas(monkeypatch):
    def unexpected(*args, **kwargs):
        raise AssertionError("Must reject before drawing")

    monkeypatch.setattr(PageCanvas, "__init__", unexpected)
    model = state()
    with pytest.raises(DataValidationError) as caught:
        detail.render(model, context_for(model), contract_id="absent")
    assert caught.value.code == "contract_not_found"
    wrong = PlayerCard(player=PlayerIdentity(name="Other", game_uid="456", skport_id="other"))
    with pytest.raises(OwnerMismatchError):
        detail.render(model, context_for(model), profile=wrong)


def test_extreme_indicator_counts_are_bounded_with_overflow_note(drawn):
    model = state(runs=0, modifiers=100)
    pages = detail.render(model, context_for(model))
    assert len(pages) == 1 and pages[0].height < 1600
    assert any("+58 indicators in source data" in value for value, *_ in drawn)
    assert len(model.current.modifiers) == 100
    pages[0].close()


def test_unknown_scores_sort_after_observed_zero_and_duration_ties_are_stable():
    item = CrisisContract(
        runs=[
            StageRun(id="unknown"),
            StageRun(id="zero", score=0, duration_seconds=0),
            StageRun(id="fast", score=5, duration_seconds=10),
            StageRun(id="slow", score=5, duration_seconds=20),
        ]
    )
    assert [run.id for run in parts.ordered_runs(item)] == ["fast", "slow", "zero", "unknown"]


def test_supplied_avatar_is_used_when_preferred_portrait_pixels_are_unavailable():
    model = state(runs=1)
    member = model.current.runs[0].team[0]
    member.images.avatar = ImageLinks(skport="https://detail.example.test/avatar.png")
    source = Image.new("RGBA", (100, 100), "#17C74B")
    images = {member.images.avatar.url: source}
    c = PageCanvas("Team", context_for(model), assets=images, size=(2000, 800), header=False)
    pixels = source.tobytes()
    parts._member(c, member, (100, 100, 350, 430))
    assert c.image.getpixel((220, 175))[:3] == (23, 199, 75)
    assert source.tobytes() == pixels
    assert member.images.avatar.url in parts.urls(model)
    c.image.close()
    source.close()


def test_contract_deadlines_and_battle_times_respect_caller_timezone(drawn):
    model = state(runs=1)
    context = replace(context_for(model), display_timezone="Asia/Calcutta")
    pages = detail.render(model, context)
    values = "\n".join(value for value, *_ in drawn)
    assert "26 Nov 2026 · 01:30 IST" in values
    assert "25 Nov 2026 · 17:30 IST" in values
    pages[0].close()


def test_rule_preview_is_bounded_before_text_measurement_and_source_is_unchanged(drawn):
    model = state(runs=0)
    model.current.rules = "Source mechanic " * 1000
    original = model.current.rules
    pages = detail.render(model, context_for(model))
    previews = [value for value, *_ in drawn if value.startswith("Source mechanic")]
    assert len(previews) == 1 and len(previews[0]) <= 241 and previews[0].endswith("…")
    assert model.current.rules == original
    pages[0].close()
