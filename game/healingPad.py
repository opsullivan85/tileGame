from typing import List

from pyglet import image

from game.attributes import AttrHealing, AttrHealthy
from game.gridDrawable import GridDrawable
from game.pose import Pose
from game.resources import get_resource_path


class HealingPad(AttrHealing, GridDrawable):
    _healingPad_texture_path = get_resource_path('textures/healingPad.png')

    def __init__(self, healing: float, pose: Pose = Pose()):
        super().__init__(healing=healing, pose=pose, img=image.load(HealingPad._healingPad_texture_path))
        self.tile_size = 0

    def heal(self, other: AttrHealthy) -> None:
        other.health = min(other.max_health, other.health + self.healing)

    def can_coexist(self, others: List['GridObject']) -> bool:
        return True

    def overlaps(self, others: List['GridObject']) -> None:
        for other in others:
            if isinstance(other, AttrHealthy):
                self.heal(other)

    def collision(self, other: 'GridObject') -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def __eq__(self, other: 'GridObject') -> bool:
        return isinstance(other, HealingPad) and self.healing == other.healing
