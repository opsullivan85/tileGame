from typing import List

from pyglet import image, sprite
from pyglet.sprite import Sprite

from game.camera import Camera
from game.gridDrawable import GridDrawable
from game.gridObject import GridObject
from game.pose import Pose
from game.resources import get_resource_path

_wall_texture_path = get_resource_path('textures/wall.png')
_wall_image = image.load(_wall_texture_path).get_region(0, 0, 64, 48)
_wall_sprite = sprite.Sprite(_wall_image)


class Wall(GridDrawable):

    def __init__(self, pose: Pose = Pose()):
        super().__init__(pose)

    def equals(self, other):
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

    def draw(self, camera: Camera, dt: float):
        super().draw(camera, self.pose, _wall_sprite, dt)
