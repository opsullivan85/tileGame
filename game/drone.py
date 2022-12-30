from collections import deque
from typing import List

from pyglet import image

from game.attributes import AttrPathFollowing
from game.gridDrawable import GridDrawable
from game.pose import Pose
from game.resources import get_resource_path


class Drone(AttrPathFollowing, GridDrawable):
    """ Follows a path on repeat forever
    """
    _drone_texture_path = get_resource_path('textures/pointer.png')

    def __init__(self, pose: Pose, path: deque[Pose] = None):
        img = image.load(Drone._drone_texture_path).get_region(0, 0, 64, 48)
        super().__init__(pose=pose, img=img)
        if path is not None:
            self.is_path_following = True
            self.set_path(path, wrap=True)
        else:
            self.is_path_following = False
        self.update_every_frame = True
        self.tile_size = 1

    def set_path(self, path: deque[Pose], wrap: bool = False):
        super().set_path(path=path, wrap=wrap)
        self.is_path_following = path is not None

    def can_coexist(self, others: List['GridObject']) -> bool:
        return super().can_coexist(others)

    def overlaps(self, others: List['GridObject']) -> None:
        pass

    def collision(self, other: 'GridObject') -> None:
        pass

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.is_path_following:
            self.follow_path()

    def equals(self, other: 'GridObject') -> bool:
        return isinstance(other, Drone) and self.path == other.path
