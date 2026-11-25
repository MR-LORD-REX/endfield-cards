"""Both comparison variants retain the shared character weapon level markers."""

import pytest
from skport.games.endfield.models import (
    CharacterBuild,
    CharacterIdentity,
    Gem,
    GemTerm,
    PlayerIdentity,
    Skill,
    Weapon,
)

from endfield_cards.adapters.skport import context_for
from endfield_cards.rendering.templates.character import components as parts
from endfield_cards.rendering.templates.comparison._shared import draw_loadout
from endfield_cards.utils.drawing import PageCanvas


@pytest.mark.parametrize("dark", [False, True])
def test_comparison_weapon_uses_confirmed_base_bonus_and_essence_capsules(dark, monkeypatch):
    source = CharacterBuild(
        identity=CharacterIdentity(skport_id="operator"),
        owner=PlayerIdentity(skport_id="owner", name="Owner", game_uid="game"),
        weapon=Weapon(
            name="Weapon",
            skills=[Skill(name="Will", level=9, base_level=3, bonus_level=6)],
            gem=Gem(name="Essence", terms=[GemTerm(name="Will", points=6)]),
        ),
    )
    before = source.model_dump()
    c = PageCanvas("Comparison", context_for(source), header=False, dark=dark, size=(2160, 1400))
    calls = []
    original = parts._level_capsules

    def capture(canvas, x, y, base, bonus, width):
        calls.append((base, bonus, x, y))
        return original(canvas, x, y, base, bonus, width)

    monkeypatch.setattr(parts, "_level_capsules", capture)
    draw_loadout(c, source, 0, dark=dark)
    assert [(base, bonus) for base, bonus, *_ in calls] == [(3, 6), (0, 6)]
    assert all(40 <= x < 720 and 426 <= y and y + 13 <= 769 for _, _, x, y in calls)
    assert source.model_dump() == before
    c.image.close()
