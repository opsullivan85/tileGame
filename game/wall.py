from typing import List

from pyglet import image

from game.gridDrawable import GridDrawable
from game.gridObject import GridObject
from game.pose import Pose
from game.resources import get_resource_path


class Wall(GridDrawable):
    _wall_texture_path = get_resource_path('textures/wall.png')

    def __init__(self, pose: Pose = Pose()):
        super().__init__(pose, image.load(Wall._wall_texture_path))

    def __eq__(self, other):
        return isinstance(other, Wall) and \
            self.pose.coordinates_equal(other.pose) and \
            self.pose.sizes_equal(other.pose)

    def can_coexist(self, others: List['GridObject']) -> bool:
        # Return false if anything in others
        return not others

    def collision(self, other: 'GridObject') -> None:
        ...

    def overlaps(self, others: List['GridObject']) -> None:
        ...

    def update(self, dt: float) -> None:
        ...
