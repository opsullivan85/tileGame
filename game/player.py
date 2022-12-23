from typing import List

from pyglet import image

from game.attributes import AttrHealthy
from game.gridObject import GridObject
from game.pose import Pose
from game.resources import get_resource_path


class Player(AttrHealthy):
    _player_texture_path = get_resource_path('textures/pointer.png')

    def __init__(self, pose: Pose = Pose()):
        super().__init__(100, pose=pose, img=image.load(Player._player_texture_path))
        self.tile_size = 2
        self.update_every_frame = True

    def __eq__(self, other):
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
