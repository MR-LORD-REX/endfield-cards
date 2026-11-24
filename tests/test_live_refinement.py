"""Live cards retain observed state, clocks, ownership and one concise image."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from PIL import Image, ImageDraw
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    LiveStatus,
    PlayerCard,
    PlayerIdentity,
    ResourceMeter,
)
from skport.games.endfield.models.base import ModelIssue

from endfield_cards.adapters.skport import context_for
from endfield_cards.assets.fonts import FontManager
from endfield_cards.assets.manifest import resource_path
from endfield_cards.assets.store import AssetStore
from endfield_cards.client import Cards
from endfield_cards.errors import OwnerMismatchError
from endfield_cards.models import OwnerIdentity, RenderIssue
from endfield_cards.rendering.templates import activity
from endfield_cards.utils.drawing import PageCanvas

NOW = datetime(2026, 11, 24, 12, 0, tzinfo=UTC)


def owner(index: int = 1) -> PlayerIdentity:
    return PlayerIdentity(skport_id=f"owner-{index}", game_uid=f"game-{index}", name=f"Live Owner {index}")


def live() -> LiveStatus:
    return LiveStatus(
        player=owner(),
        server_time=NOW,
        sanity=ResourceMeter(name="Sanity", current=1000, maximum=360),
        daily=ResourceMeter(name="Daily activity", current=23, maximum=100),
        weekly=ResourceMeter(name="Weekly routine", current=3, maximum=10),
        battle_pass=ResourceMeter(name="Battle pass", current=17, maximum=60),
        credits=ResourceMeter(name="Credits", current=200, maximum=300, refresh_at=NOW + timedelta(hours=3)),
    )


def profile(player: PlayerIdentity | None = None) -> PlayerCard:
    return PlayerCard(player=player or owner(), authority_level=60, server_name="Asia", server_time=NOW)


@pytest.fixture
def text_log(monkeypatch):
    entries = []
    original = PageCanvas.text

    def capture(self, x, y, value, **options):
        height = original(self, x, y, value, **options)
        entries.append((str(value), x, y, height, self.width, self.height))
        return height

    monkeypatch.setattr(PageCanvas, "text", capture)
    return entries


@pytest.fixture
def icons(monkeypatch):
    requested = []
    original = PageCanvas.icon

    def capture(self, key, x, y, size=32, **options):
        requested.append(key)
        return original(self, key, x, y, size, **options)

    monkeypatch.setattr(PageCanvas, "icon", capture)
    return requested


def text(entries) -> str:
    return "\n".join(entry[0] for entry in entries)


def normalized(entries) -> str:
    return text(entries).replace(",", "").replace(" ", "").casefold()


def close(pages) -> None:
    for page in pages:
        page.close()


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_live_is_one_card_with_all_observed_meters_icons_and_owner(variant, text_log, icons):
    model, player_card = live(), profile()
    before = model.model_dump(), player_card.model_dump()
    context = replace(context_for(model), display_timezone="Asia/Kolkata")
    pages = activity.render(model, context, variant=variant, profile=player_card)
    assert len(pages) == 1 and pages[0].size == (1600, 1000)
    drawn = normalized(text_log)
    assert all(
        label in drawn for label in ("sanity", "dailyactivity", "weeklyroutine", "battlepass", "credits")
    )
    assert all(str(value) in drawn for value in (1000, 360, 23, 100, 3, 10, 17, 60, 200, 300))
    assert "Live Owner 1" in text(text_log) and "UID game-1" in text(text_log)
    assert "akef-cards" in drawn and "endfield-cards" in drawn
    assert "player.sanity" in icons and "player.daily" in icons
    assert all(
        0 <= x < width and 0 <= y and y + height <= bottom for _, x, y, height, width, bottom in text_log
    )
    assert before == (model.model_dump(), player_card.model_dump())
    close(pages)


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_missing_live_meters_are_unavailable_without_invented_zero(variant, text_log):
    model = LiveStatus(player=owner(), server_time=NOW)
    pages = activity.render(model, context_for(model), variant=variant)
    drawn = text(text_log)
    assert len(pages) == 1 and "Unavailable" in drawn
    assert not any(entry[0].strip() in {"0", "0/0", "0 / 0", "0 / 100", "0 / 360"} for entry in text_log)
    close(pages)


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_additional_supplied_activity_meters_keep_values_and_explicit_overflow_on_one_card(variant, text_log):
    model = live()
    model.activities = [
        ResourceMeter(name=f"Observed activity {index}", current=12 + index, maximum=30 + index)
        for index in range(7)
    ]
    before = model.model_dump()
    pages = activity.render(model, context_for(model), variant=variant)
    drawn = normalized(text_log)
    assert len(pages) == 1
    for index in range(4):
        assert f"observedactivity{index}" in drawn and f"{12 + index}/{30 + index}" in drawn
    assert "observedactivity4" not in drawn and "+3activities" in drawn
    strips = [entry for entry in text_log if "Observed activity" in entry[0]]
    assert strips and all(y >= 154 and y + height <= 184 for _, _, y, height, _, _ in strips)
    assert before == model.model_dump()
    close(pages)


def test_sanity_overflow_is_preserved_but_ring_stays_bounded(monkeypatch, text_log):
    arcs = []
    original = ImageDraw.ImageDraw.arc

    def capture(self, box, start, end, **options):
        arcs.append((start, end))
        return original(self, box, start, end, **options)

    monkeypatch.setattr(ImageDraw.ImageDraw, "arc", capture)
    model = live()
    pages = activity.render(model, context_for(model))
    drawn = normalized(text_log)
    assert "1000" in drawn and "360" in drawn
    assert model.sanity.current == 1000 and model.sanity.ratio > 1
    assert arcs and all(0 <= end - start <= 360 for start, end in arcs)
    close(pages)


def test_countdowns_use_only_supplied_source_time_and_report_missing_deadlines():
    from endfield_cards.utils.time import remaining, source_datetime

    assert source_datetime(NOW.replace(tzinfo=None)) == NOW
    assert source_datetime(str(int(NOW.timestamp()))) == NOW
    assert source_datetime("unavailable") is None
    assert remaining(NOW + timedelta(hours=1, minutes=30), NOW) == "1h 30m"
    assert remaining(NOW + timedelta(hours=3, minutes=1, seconds=1), NOW) == "3h 01m"
    assert remaining(NOW - timedelta(seconds=1), NOW) == "Due"
    assert remaining(None, NOW) == "Unavailable"
    assert remaining(NOW, None) == "Unavailable"


@pytest.mark.parametrize("label,glyph", [("Cycle of Fervor Ⅲ", "Ⅲ"), ("A → B", "→")])
def test_live_number_forms_and_arrows_render_actual_glyphs_instead_of_missing_boxes(label, glyph):
    font = FontManager().get(33, text=label)
    rendered = font.getmask(glyph)
    missing = font.getmask("\u0378")
    assert rendered.getbbox() is not None
    assert (rendered.size, bytes(rendered)) != (missing.size, bytes(missing))


def test_colored_reception_badge_retains_its_palette_when_explicitly_preserved():
    key = "player.room-reception"
    with Image.open(resource_path(key)) as original:
        source = original.convert("RGBA")
    before = source.tobytes()
    opaque_points = [
        (x, y) for y in range(source.height) for x in range(source.width) if source.getpixel((x, y))[3] == 255
    ]
    palette = {source.getpixel(point)[:3] for point in opaque_points}
    assert len(palette) > 1
    canvas = PageCanvas(
        "Live status", context_for(owner()), header=False, size=(120, 70), assets={key: source}
    )
    assert canvas.icon(key, 5, 10, source.width, tint="#FFC800", preserve_color=True)
    assert canvas.icon(key, 65, 10, source.width, tint="#FFC800")
    preserved = {canvas.image.getpixel((x + 5, y + 10))[:3] for x, y in opaque_points}
    flattened = {canvas.image.getpixel((x + 65, y + 10))[:3] for x, y in opaque_points}
    assert preserved == palette and flattened == {(255, 200, 0)}
    assert source.tobytes() == before
    canvas.image.close()
    source.close()


@pytest.mark.parametrize("timezone,clock", [("Asia/Kolkata", "17:30 IST"), ("America/New_York", "07:00 EST")])
def test_live_source_stamp_uses_utc_while_shared_formatter_supports_context_timezone(
    timezone, clock, text_log
):
    from endfield_cards.utils.time import display_time

    model = live()
    model.sanity = ResourceMeter(
        name="Sanity", current=100, maximum=360, recovery_at=NOW + timedelta(hours=1, minutes=30)
    )
    model.credits.refresh_at = NOW + timedelta(hours=3, minutes=1, seconds=1)
    # A different footer snapshot must not replace the LiveStatus source clock.
    context = replace(context_for(model), snapshot_at=NOW + timedelta(days=5), display_timezone=timezone)
    assert display_time(NOW, context) == f"24 Nov 2026 · {clock}"
    pages = activity.render(model, context)
    body = "\n".join(value for value, _, y, _, _, height in text_log if y < height - 66)
    assert "24 Nov 2026 · 12:00 UTC" in body
    assert "IST" not in body and "EST" not in body
    assert "1h 30m" in body and "3h 01m" in body
    assert "29 Nov 2026" not in body
    close(pages)


def event_source() -> dict[str, Any]:
    return {
        "war_echoes": {
            "seasons": [
                {
                    "name": "Season of Test",
                    "startTs": str(int((NOW - timedelta(days=1)).timestamp())),
                    "endTs": str(int((NOW + timedelta(days=2)).timestamp())),
                    "stars": 7,
                    "allPlusTasks": False,
                    "weeks": [{"name": "Cycle of Test III", "stars": 2, "allPlusTasks": False}],
                }
            ]
        },
        "crisis_contract": [
            {
                "name": "Contingency Contract: Observed Test",
                "highest": 24,
                "challengeCount": 3,
                "weeklyMission": {"count": 4, "total": 7},
                "indicatorMission": {"count": 2, "total": 5},
                "stageMission": {"count": 1, "total": 2},
                "gameplayEndAtTs": str(int((NOW + timedelta(days=1)).timestamp())),
                "endAtTs": str(int((NOW + timedelta(days=3)).timestamp())),
                "achieve": {"level": 2, "isPlated": False, "achievementData": {"name": "Observed medal"}},
            }
        ],
    }


def test_event_summaries_distinguish_missing_numbers_from_observed_zero():
    from endfield_cards.utils.activity import event_summaries

    current = event_source()
    week = current["war_echoes"]["seasons"][0]["weeks"][0]
    week["stars"] = None
    week["dungeonGroups"] = [
        {"name": "Unavailable stage", "plusTask": None},
        {"name": "Observed zero stage", "star": 0, "plusTask": False},
    ]
    contract_source = current["crisis_contract"][0]
    contract_source["highest"] = None
    contract_source["challengeCount"] = False
    contract_source["weeklyMission"] = {"total": 7}
    contract_source["stageMission"] = {"count": 0, "total": 2}
    model = live().model_copy(update={"current_event": current}, deep=True)
    echo, contract = event_summaries(model)
    assert echo is not None and echo.stars is None
    assert echo.stages == (
        ("Unavailable stage", None, None),
        ("Observed zero stage", 0, False),
    )
    assert contract is not None and contract.score is None and contract.attempts is None
    assert ("Weekly", None, 7) in contract.missions and ("Stages", 0, 2) in contract.missions
    model.current_event = {"war_echoes": [], "crisis_contract": {}}
    assert event_summaries(model) == (None, None)


def test_live_event_play_and_cycle_deadlines_precede_later_claim_and_season_dates():
    from endfield_cards.utils.activity import event_status, event_summaries

    current = event_source()
    week = current["war_echoes"]["seasons"][0]["weeks"][0]
    week["endTs"] = str(int((NOW - timedelta(hours=1)).timestamp()))
    current["crisis_contract"][0]["gameplayEndAtTs"] = str(int((NOW - timedelta(hours=1)).timestamp()))
    model = live().model_copy(update={"current_event": current}, deep=True)
    echo, contract = event_summaries(model)
    assert echo is not None and contract is not None
    assert echo.ends_at == contract.ends_at == NOW - timedelta(hours=1)
    assert event_status(echo.starts_at, echo.ends_at, NOW) == "Ended"
    assert event_status(contract.starts_at, contract.ends_at, NOW) == "Ended"
    assert event_status(NOW + timedelta(hours=1), NOW + timedelta(days=1), NOW) == "Starts in 1h 00m"
    assert event_status(None, None, NOW) == "End time unavailable"
    assert event_status(None, NOW + timedelta(hours=1), None) == "Time unavailable"


@pytest.mark.parametrize("variant", ["light", "dark"])
def test_live_summarizes_both_current_event_source_shapes_without_raw_json(variant, text_log, icons):
    model = live().model_copy(update={"current_event": event_source()}, deep=True)
    before = model.model_dump()
    pages = activity.render(model, context_for(model), variant=variant)
    drawn = text(text_log)
    compact = normalized(text_log)
    assert len(pages) == 1
    assert "Season of Test" in drawn and "Cycle of Test III" in drawn
    assert "Observed Test" in drawn
    assert "24" in drawn and all(value in compact for value in ("4/7", "2/5", "1/2"))
    assert "player.war-echoes" in icons and "player.contingency-contract" in icons
    assert "war_echoes" not in drawn and "crisis_contract" not in drawn and "gameplayEndAtTs" not in drawn
    assert before == model.model_dump()
    close(pages)


@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [False, True])
async def test_live_profile_owner_mismatch_precedes_even_custom_art_loading(monkeypatch, stream):
    calls = []

    async def unexpected_load(self, source):
        calls.append(source)
        raise AssertionError("Owner mismatch must be rejected before artwork loading")

    monkeypatch.setattr(AssetStore, "load", unexpected_load)
    async with Cards() as cards:
        options = {"profile": profile(owner(2)), "art": b"invalid-art"}
        with pytest.raises(OwnerMismatchError):
            if stream:
                iterator = cards.iter_pages("activity", live(), **options)
                try:
                    await anext(iterator)
                finally:
                    await iterator.aclose()
            else:
                await cards.render_live(live(), **options)
    assert calls == []


@pytest.mark.asyncio
async def test_live_alias_returns_one_encoded_result_and_keeps_profile_source_issues(monkeypatch):
    requests = []
    card = profile()
    card.issues = [ModelIssue(code="profile-source", message="Observed profile issue")]

    async def unexpected_fetch(self, url, **options):
        requests.append(url)
        raise AssertionError("A profile without remote images must not require HTTP")

    monkeypatch.setattr(AssetStore, "get", unexpected_fetch)
    async with Cards() as cards:
        pages = await cards.render_live(live(), profile=card)
    assert len(pages) == 1 and pages[0].family == "activity" and pages[0].pages == 1
    assert RenderIssue("profile-source", "Observed profile issue") in pages[0].issues
    assert requests == []


@pytest.mark.asyncio
async def test_roster_result_keeps_nested_character_sdk_issues_without_http(monkeypatch):
    requests = []
    card = profile()
    card.source_scope = "owner"
    card.roster_complete = True
    card.issues = [ModelIssue(code="profile-source", message="Observed profile issue")]
    card.characters = [
        CharacterBuild(
            identity=CharacterIdentity(skport_id="char-1", str_id="canonical-1"),
            owner=card.player,
            name="Observed operator",
            issues=[ModelIssue(code="character-source", message="Observed character issue")],
        )
    ]
    before = card.model_dump()

    async def unexpected_fetch(self, url, **options):
        requests.append(url)
        raise AssertionError("Nested issue propagation must not require HTTP")

    monkeypatch.setattr(AssetStore, "get", unexpected_fetch)
    async with Cards() as cards:
        pages = await cards.render_roster(card)
    assert len(pages) == 1
    assert pages[0].issues == (
        RenderIssue("profile-source", "Observed profile issue"),
        RenderIssue("character-source", "Observed character issue"),
    )
    assert requests == [] and before == card.model_dump()


def test_live_footer_can_preserve_both_explicit_context_owners(text_log):
    model = live()
    context = replace(context_for(model), comparison_owner=OwnerIdentity("Second context owner", "game-2"))
    pages = activity.render(model, context)
    drawn = text(text_log)
    assert "Live Owner 1" in drawn and "UID game-1" in drawn
    assert "Second context owner" in drawn and "UID game-2" in drawn
    close(pages)
