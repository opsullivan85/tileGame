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


def add_from_image(image_path: str, grid: GameGrid) -> None:
    """ Adds all objects from the given image to the given grid

    :param image_path: Path to image
    :param grid: Grid to add objects to
    :return: None
    """
    bool_array = np.asarray(PILImage.open(image_path)) == 0
    print(np.asarray(PILImage.open(image_path)))
    for row_num, row in enumerate(bool_array):
        for col_num, element in enumerate(row):
            if element:
                grid.add(Wall(Pose(row_num, col_num, 90*randint(0, 3))))
