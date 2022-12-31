from typing import List

from pyglet import image, sprite

from game.attributes import AttrHealthy
from game.camera import Camera
from game.gridDrawable import GridDrawable
from game.gridObject import GridObject
from game.pose import Pose
from game.resources import get_resource_path

_player_texture_path = get_resource_path('textures/pointer.png')
_player_image = image.load(_player_texture_path).get_region(0, 0, 64, 48)
_player_sprite = sprite.Sprite(_player_image)


class Player(GridDrawable):

    def __init__(self, pose: Pose = Pose()):
        # super().__init__(100, pose=pose)
        super().__init__(pose=pose)
        self.tile_size = 2
        self.update_every_frame = True

    def __str__(self):
        return f'Player(pose={self.pose}, health={self.health})'

    def equals(self, other):
        return isinstance(other, Player) and self.health == other.health

    def can_coexist(self, others: List['GridObject']) -> bool:
        return super().can_coexist(others)

    def collision(self, other: 'GridObject') -> None:
        # if isinstance(other, Wall):
        #     other.remove_from_grid()
        ...

    def overlaps(self, others: List['GridObject']) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def draw(self, camera: Camera, dt: float):
        super().draw(camera, self.pose, _player_sprite, dt)
