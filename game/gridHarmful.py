from abc import ABC

from game.gridHealthy import GridHealthy
from game.gridObject import GridObject


class GridHarmful(GridObject, ABC):
    def __init__(self, damage: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage

    def attack(self, other: GridHealthy) -> None:
        other.health -= self.damage


