from typing import Iterable, Union

import pytest

from dice import hit_roll, wound_roll
from unit import UnitFactory

DiceRolls = Union[int, Iterable[int]]


@pytest.mark.parametrize(
    "weapon_skill", [2, 3, 4, 5, 6]
)  # weapon_skill 1 doesn't exists in warhammer40k
def test_weapon_skill_attack(weapon_skill):
    dices = list(range(1, 7))
    unsuccessful_hits = weapon_skill - 1
    successful_hits = len(dices) - unsuccessful_hits
    unit_factory = UnitFactory()
    attacker = unit_factory(weapon_skill=weapon_skill)

    success, failure = hit_roll(attacker.weapon_skill, dices)

    assert success == successful_hits
    assert failure == unsuccessful_hits


def test_attacker_hits_defender():
    unit_factory = UnitFactory()
    attacker = unit_factory(strength=4)
    defender = unit_factory(toughness=4)
    dice_rolls = [2, 5]

    successful_hits, unsuccessful_hits = wound_roll(
        attacker.strength, defender.toughness, dice_rolls
    )

    assert successful_hits == 1
    assert unsuccessful_hits == 1
