from random import randint
from typing import List

import numpy as np
from PIL import Image as PILImage
from pyglet import image

from game.gameGrid import GameGrid
from game.gridDrawable import GridDrawable
from game.gridObject import GridObject
from game.pose import Pose


class Wall(GridDrawable):
    _wall_texture_path = '../DrinkTheBeer/resources/images/wall.png'

    def __init__(self, pose: Pose = Pose()):
        super().__init__(pose, image.load(Wall._wall_texture_path))

    def can_coexist(self, other: 'GridObject') -> bool:
        return False

    def overlaps(self, others: List['GridObject']) -> None:
        # `others` will always be empty
        pass

    def update(self, dt: float) -> None:
        ...
