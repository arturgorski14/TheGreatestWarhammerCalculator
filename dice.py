# TODO: refactor: Move dice functions to class

import random
from typing import Iterable, List, Tuple, Union

DiceRolls = Union[int, Iterable[int]]


def roll_n_times(n_attacks: int) -> List[int]:
    dices = []
    for _ in range(n_attacks):
        dice = random.randint(1, 6)
        dices.append(dice)
    return dices


# TODO: refactor: rerolls - code smell
# Consider reroll using strategy pattern for different units
def reroll_all(dice_rolls: DiceRolls) -> List[int]:
    """
    Assuming pre-reroll values are redundant
    """
    if isinstance(dice_rolls, int):
        dice_rolls = [dice_rolls]
    dice_rolls = roll_n_times(len(dice_rolls))
    return dice_rolls


def reroll_equal_and_below_threshold(
    dice_rolls: DiceRolls, threshold: int
) -> List[int]:
    # TODO: better variable names
    if isinstance(dice_rolls, int):
        dice_rolls = [dice_rolls]
    _dice_rolls = [value for value in dice_rolls if value > threshold]
    to_reroll = len(dice_rolls) - len(_dice_rolls)
    return _dice_rolls + roll_n_times(to_reroll)


def hit_roll(hit_dice: int, dice_rolls: DiceRolls) -> Tuple[int, int]:
    if isinstance(dice_rolls, int):
        dice_rolls = [dice_rolls]

    successful_hits = sum(1 for roll in dice_rolls if roll >= hit_dice)
    unsuccessful_hits = len(dice_rolls) - successful_hits

    return successful_hits, unsuccessful_hits


def wound_roll(strength: int, toughness: int, dice_rolls: DiceRolls) -> Tuple[int, int]:
    hit_dice = _determine_hit_dice(strength, toughness)

    return hit_roll(hit_dice, dice_rolls)


def _determine_hit_dice(strength: int, toughness: int) -> int:
    """
    :return: Minimum dice value which is required for successful hit
    :exception: Impossible case with integers
    """
    if strength >= 2 * toughness:
        hit_dice = 2
    elif strength > toughness:
        hit_dice = 3
    elif strength == toughness:
        hit_dice = 4
    elif 2 * strength <= toughness:  # niestety musi być taka kolejność
        hit_dice = 6
    elif strength < toughness:
        hit_dice = 5
    else:
        raise ValueError(f"PLEASE VERIFY INPUT DATA: {strength=}, {toughness=}")

    return hit_dice


def save_roll(save: int, dice_rolls: DiceRolls) -> Tuple[int, int]:
    return hit_roll(save, dice_rolls)
