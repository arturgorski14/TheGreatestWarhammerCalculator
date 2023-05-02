from typing import Iterable, Tuple, Union

DiceRolls = Union[int, Iterable[int]]


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


def save_roll(save: int, dice_rolls: DiceRolls):
    return hit_roll(save, dice_rolls)
