from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Unit:
    movement: int
    weapon_skill: int
    balistic_skill: Optional[int]
    strength: int
    toughness: int
    wounds: int
    initiative: int
    attacks: int
    leadership: int
    save: int


class UnitFactory:
    def __call__(self, *args, **kwargs):
        # TODO: sanitize input - schema
        default_unit = dict(
            movement=1,
            weapon_skill=2,
            balistic_skill=None,
            strength=1,
            toughness=1,
            wounds=1,
            initiative=1,
            attacks=1,
            leadership=1,
            save=2,
        )

        default_unit.update(args)
        default_unit.update(kwargs)

        return Unit(**default_unit)
