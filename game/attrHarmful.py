from abc import ABC

from game.attrHealthy import AttrHealthy
from game.gridObject import GridObject


class AttrHarmful(GridObject, ABC):
    def __init__(self, damage: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage

    def attack(self, other: AttrHealthy) -> None:
        other.health -= self.damage


