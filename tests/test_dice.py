from unittest.mock import patch

import pytest

from dice import (hit_roll, reroll_all, reroll_equal_and_below_threshold,
                  roll_n_times, save_roll, wound_roll)
from unit import UnitFactory

dices = list(range(1, 7))
unit_factory = UnitFactory()


def test_roll_n_times():
    minimum = 1
    maximum = 6
    attacker = unit_factory(attacks=25)

    _dices = roll_n_times(attacker.attacks)

    assert len(_dices) == attacker.attacks
    assert min(_dices) == minimum
    assert max(_dices) == maximum


def test_reroll_single_dice():
    _dices = 1
    expected = 4

    with patch("dice.random.randint") as rnd:
        rnd.return_value = expected

        rerolled_dices = reroll_all(_dices)

        assert len(rerolled_dices) == 1
        assert rerolled_dices == [rnd.return_value]
        assert rerolled_dices[0] != _dices


def test_reroll_multiple_dices():
    _dices = [1, 1, 2, 3, 4, 5, 6]
    expected = 3
    threshold = 1
    with patch("dice.random.randint") as rnd:
        rnd.return_value = expected

        dices_with_rerolled = reroll_equal_and_below_threshold(_dices, threshold)

        assert sorted(dices_with_rerolled) == sorted([3, 3, 2, 3, 4, 5, 6])


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
