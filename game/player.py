from typing import List

from pyglet import image

from game.gridDrawable import GridDrawable
from game.gridObject import GridObject
from game.pose import Pose
from game.resources import get_resource_path
from game.wall import Wall


class Player(GridDrawable):
    _player_texture_path = get_resource_path('textures/pointer.png')

    def __init__(self, pose: Pose = Pose()):
        super().__init__(pose, image.load(Player._player_texture_path))
        self.tile_size = 2

    def __eq__(self, other):
        return isinstance(other, Player) and self.pose == other.pose

    def can_coexist(self, others: List['GridObject']) -> bool:
        for other in others:
            if isinstance(other, Wall):
                other.remove_from_grid()
        return super().can_coexist(others)

    def overlaps(self, others: List['GridObject']) -> None:
        # `others` will always be empty
        pass

    def update(self, dt: float) -> None:
        ...
