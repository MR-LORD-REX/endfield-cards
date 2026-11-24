"""Contract showcases preserve source state and stay bounded on one card."""

from datetime import UTC, datetime

import pytest
from PIL import Image
from skport.games.endfield.models import (
    ContractState,
    CrisisContract,
    EnemySummary,
    ImageLinks,
    MedalSummary,
    PlayerCard,
    PlayerIdentity,
    ResourceMeter,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.assets.store import AssetStore
from endfield_cards.errors import DataValidationError, OwnerMismatchError
from endfield_cards.rendering import RenderEngine
from endfield_cards.rendering.templates import contingency_contract as contract
from endfield_cards.rendering.templates.contingency_contract import _shared as parts
from endfield_cards.utils.drawing import PageCanvas


def state():
    player = PlayerIdentity(name="Contract Owner", game_uid="123", skport_id="social")

    def link(name):
        return ImageLinks(skport=f"https://card.example.test/{name}.png")

    current = CrisisContract(
        id="cc",
        name="Contingency Contract: Test Operation",
        poster=link("poster"),
        best_score=17,
        attempts=3,
        stage_id="dungeon",
        stage_name="Encounter",
        medal=MedalSummary(name="Observed Medal", level=2, plated=True, icon=link("medal")),
        ends_at=datetime(2026, 11, 24, 22, tzinfo=UTC),
        ends_at_collection=datetime(2026, 12, 1, 20, tzinfo=UTC),
        missions=[
            ResourceMeter(name="Weekly", current=99, maximum=7),
            ResourceMeter(name="Indicators", current=3, maximum=5),
            ResourceMeter(name="Stages", current=0, maximum=2),
        ],
        enemies=[
            EnemySummary(id=f"enemy-{i}", name=f"Observed Enemy {i}", icon=link(f"enemy-{i}"), level=60)
            for i in range(7)
        ],
    )
    return ContractState(player=player, current=current, contracts=[current])


@pytest.fixture
def drawn(monkeypatch):
    output = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        output.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return output


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_actual_contract_info_art_and_overflow_are_preserved(variant, drawn):
    model = state()
    source = Image.new("RGBA", (98, 88), (53, 112, 190, 211))
    images = {
        model.current.poster.url: source,
        model.current.medal.icon.url: source,
        **{enemy.icon.url: source for enemy in model.current.enemies},
    }
    pixels = source.tobytes()
    before = model.model_dump()
    pages = contract.render(model, context_for(model), variant=variant, assets=images)
    text = "\n".join(value for value, *_ in drawn)
    assert len(pages) == 1 and pages[0].size == (1600, 1000)
    assert all(
        value in text
        for value in ["Test Operation", "17", "3 attempts", "99 / 7", "3 / 5", "0 / 2", "Medal Lv 2 · Plated"]
    )
    assert all(enemy.name in text for enemy in model.current.enemies)
    assert "akef-cards" in text and "endfield-cards" in text and "UID 123" in text
    assert all(0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in drawn)
    assert source.tobytes() == pixels and model.model_dump() == before
    assert model.current.missions[0].current == 99
    pages[0].close()
    source.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_missing_source_score_and_medal_do_not_turn_into_observed_zero(variant, drawn):
    model = state()
    model.current = CrisisContract(id="cc", name="Partial Contract")
    model.contracts = [model.current]
    pages = contract.render(model, context_for(model), variant=variant)
    text = "\n".join(value for value, *_ in drawn)
    assert "—" in text and "Medal unavailable" in text and "Mission progress unavailable" in text
    assert "0 attempts" not in text and "Not earned yet" not in text
    pages[0].close()


def test_selections_reject_missing_or_ambiguous_contract_ids_before_drawing(monkeypatch):
    def unexpected(*args, **kwargs):
        raise AssertionError("Invalid selection must fail before canvas allocation")

    monkeypatch.setattr(PageCanvas, "__init__", unexpected)
    model = state()
    with pytest.raises(DataValidationError) as exc:
        contract.render(model, context_for(model), contract_id="absent")
    assert exc.value.code == "contract_not_found"
    model.contracts.append(model.current.model_copy(deep=True))
    with pytest.raises(DataValidationError) as exc:
        contract.render(model, context_for(model))
    assert exc.value.code == "duplicate_contract"


@pytest.mark.asyncio
async def test_profile_owner_is_validated_before_any_custom_art_io(monkeypatch):
    calls = []

    async def unexpected(self, art):
        calls.append(art)
        raise AssertionError("Mismatched profile must not load artwork")

    monkeypatch.setattr(AssetStore, "load", unexpected)
    model = state()
    wrong = PlayerCard(player=PlayerIdentity(name="Other", game_uid="456", skport_id="other"))
    async with RenderEngine() as cards:
        with pytest.raises(OwnerMismatchError):
            await cards.render_contingency_contract(model, profile=wrong, art=b"invalid")
    assert calls == []


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_future_extra_missions_stay_one_page_with_explicit_overflow(variant, drawn):
    model = state()
    model.current.missions.extend(
        ResourceMeter(name=f"Extra mission {i}", current=i, maximum=10) for i in range(7)
    )
    pages = contract.render(model, context_for(model), variant=variant)
    text = "\n".join(value for value, *_ in drawn)
    assert len(pages) == 1 and "+4 missions" in text
    assert all(0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in drawn)
    pages[0].close()


def test_light_weapon_independent_palette_and_earned_medal_state():
    model = state()
    canvas = parts.new_canvas(context_for(model), dark=False, assets={})
    palette = canvas.fg, canvas.muted, canvas.panel_color, canvas.line
    parts.score(canvas, model.current, (1080, 170, 1560, 440))
    assert palette == (canvas.fg, canvas.muted, canvas.panel_color, canvas.line)
    canvas.image.close()


def test_radial_mission_values_and_labels_are_centered_on_each_circle(monkeypatch):
    model = state()
    rings, values, labels = [], [], []
    draw_ring, draw_text = parts.ring, PageCanvas.text
    wanted = {"99 / 7", "3 / 5", "0 / 2"}

    def capture_ring(canvas, x, y, size, ratio):
        rings.append((x + size / 2, y + size / 2))
        return draw_ring(canvas, x, y, size, ratio)

    def capture_text(canvas, x, y, value, **options):
        if value in wanted or value in {"Weekly", "Indicators", "Stages"}:
            font = canvas.fonts.get(options["size"], weight="semibold", text=value)
            bounds = font.getbbox(value)
            center = (x + (bounds[0] + bounds[2]) / 2, y + (bounds[1] + bounds[3]) / 2)
            (values if value in wanted else labels).append(center)
        return draw_text(canvas, x, y, value, **options)

    monkeypatch.setattr(parts, "ring", capture_ring)
    monkeypatch.setattr(PageCanvas, "text", capture_text)
    pages = contract.render(model, context_for(model), variant="light")
    assert len(rings) == len(values) == len(labels) == 3
    for ring_center, value_center, label_center in zip(rings, values, labels, strict=True):
        assert abs(ring_center[0] - value_center[0]) <= 1
        assert abs(ring_center[1] - value_center[1]) <= 1
        assert abs(ring_center[0] - label_center[0]) <= 1
    pages[0].close()
