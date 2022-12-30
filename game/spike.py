from typing import List

from pyglet import image

from game.attributes import AttrHealthy, AttrHarmful
from game.gridDrawable import GridDrawable
from game.pose import Pose
from game.resources import get_resource_path


class Spike(AttrHarmful, GridDrawable):
    _spike_texture_path = get_resource_path('textures/pointer.png')

    def __init__(self, damage: float, pose: Pose = Pose()):
        pose.h = 0.35
        pose.w = 0.75
        super().__init__(damage=damage, pose=pose, img=image.load(Spike._spike_texture_path))
        self.tile_size = 0

    def can_coexist(self, others: List['GridObject']) -> bool:
        return True

    def overlaps(self, others: List['GridObject']) -> None:
        for other in others:
            if isinstance(other, AttrHealthy):
                self.attack(other)

    def collision(self, other: 'GridObject') -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def equals(self, other: 'GridObject') -> bool:
        return isinstance(other, Spike) and self.damage == other.damage
