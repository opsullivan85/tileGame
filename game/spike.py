from typing import List

from pyglet import image, sprite

from game.attributes import AttrHarmful
from game.camera import Camera
from game.gridDrawable import GridDrawable
from game.pose import Pose
from game.resources import get_resource_path

_spike_texture_path = get_resource_path('textures/pointer.png')
_spike_image = image.load(_spike_texture_path).get_region(0, 0, 64, 48)
_spike_sprite = sprite.Sprite(_spike_image)

class Spike(AttrHarmful, GridDrawable):
    def __init__(self, damage: float, pose: Pose):
        pose.h = 0.35
        pose.w = 0.75
        super().__init__(damage=damage, pose=pose)
        self.tile_size = 0

    def can_coexist(self, others: List['GridObject']) -> bool:
        return True

    def overlaps(self, others: List['GridObject']) -> None:
        super().overlaps(others)

    def collision(self, other: 'GridObject') -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def equals(self, other: 'GridObject') -> bool:
        return isinstance(other, Spike) and self.damage == other.damage

    def draw(self, camera: Camera, dt: float):
        super().draw(camera, self.pose, _spike_sprite, dt)
