from typing import Iterable, Union

import pytest

from dice import hit_roll, save_roll, wound_roll
from unit import UnitFactory

DiceRolls = Union[int, Iterable[int]]
dices = list(range(1, 7))
unit_factory = UnitFactory()


@pytest.mark.parametrize(
    "weapon_skill", [2, 3, 4, 5, 6]
)  # weapon_skill 1 doesn't exists in warhammer40k
def test_weapon_skill_attack(weapon_skill):
    expected_misses = weapon_skill - 1
    expected_hits = len(dices) - expected_misses
    attacker = unit_factory(weapon_skill=weapon_skill)

    success, failure = hit_roll(attacker.weapon_skill, dices)

    assert success == expected_hits
    assert failure == expected_misses


@pytest.mark.parametrize(
    "strength, toughness, expected_hits, expected_misses",
    [
        (20, 1, 5, 1),
        (16, 8, 5, 1),
        (15, 8, 4, 2),
        (5, 4, 4, 2),
        (4, 4, 3, 3),
        (4, 5, 2, 4),
        (4, 7, 2, 4),
        (4, 8, 1, 5),
        (1, 20, 1, 5),
    ],
)
def test_attacker_hits_defender(strength, toughness, expected_hits, expected_misses):
    attacker = unit_factory(strength=strength)
    defender = unit_factory(toughness=toughness)

    successful_hits, unsuccessful_hits = wound_roll(
        attacker.strength, defender.toughness, dices
    )

    assert successful_hits == expected_hits
    assert unsuccessful_hits == expected_misses


@pytest.mark.parametrize(
    "save", [2, 3, 4, 5, 6]
)  # save 1 doesn't exists in warhammer40k
def test_save_roll(save):
    expected_misses = save - 1
    expected_hits = len(dices) - expected_misses
    defender = unit_factory(save=save)

    success, failure = save_roll(defender.save, dices)

    assert success == expected_hits
    assert failure == expected_misses
