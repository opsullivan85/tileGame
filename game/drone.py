from collections import deque
from typing import List

from pyglet import image, sprite

from game.attributes import AttrPathFinding, AttrHarmful
from game.camera import Camera
from game.gridDrawable import GridDrawable
from game.pose import Pose
from game.resources import get_resource_path

_drone_texture_path = get_resource_path('textures/pointer.png')
_drone_image = image.load(_drone_texture_path).get_region(0, 0, 64, 48)
_drone_sprite = sprite.Sprite(_drone_image)

class Drone(AttrPathFinding, AttrHarmful, GridDrawable):
    """ Follows a path on repeat forever
    """

    def __init__(self, pose: Pose, path: deque[Pose] = None, wrap: bool = False):
        super().__init__(pose=pose, damage=5)
        self.set_path(path, wrap=wrap)
        self.update_every_frame = True
        self.tile_size = 1

    def set_path(self, path: deque[Pose], wrap: bool = False):
        super().set_path(path=path, wrap=wrap)
        self.is_path_following = path is not None and len(path) > 0

    def can_coexist(self, others: List['GridObject']) -> bool:
        return super().can_coexist(others)

    def overlaps(self, others: List['GridObject']) -> None:
        super().overlaps(others)

    def collision(self, other: 'GridObject') -> None:
        pass

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.is_path_following:
            self.follow_path()

    def equals(self, other: 'GridObject') -> bool:
        return isinstance(other, Drone) and self.path == other.path

    def draw(self, camera: Camera, dt: float):
        super().draw(camera, self.pose, _drone_sprite, dt)
