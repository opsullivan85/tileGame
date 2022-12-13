from abc import ABC
from random import randint

from pyglet import image, sprite
import numpy as np
from PIL import Image as PILImage

from game.Constants import TEXTURE_SIZE
from game.drawable import Drawable
from game.gameGrid import GameGrid
from game.gridObject import GridObject

from game.pose import Pose


class GridDrawable(GridObject, Drawable, ABC):
    def __init__(self, pose: Pose = Pose(), img: image.AbstractImage = None, rotation_center: tuple = (0.5, 0.5)):
        super().__init__(pose)
        img.anchor_x = int(img.width * rotation_center[0])
        img.anchor_y = int(img.height * rotation_center[1])
        self._sprite: sprite = sprite.Sprite(img, self.pose.x, self.pose.y)

    @property
    def pose(self) -> Pose:
        return GridObject.pose.fget(self)

    @pose.setter
    def pose(self, other: Pose):
        GridObject.pose.fset(self, other)

    def __update(self):
        if self.pose.w_update:
            self._sprite.scale_x = TEXTURE_SIZE * self.pose.w / self._sprite.image.width
        if self.pose.h_update:
            self._sprite.scale_y = TEXTURE_SIZE * self.pose.h / self._sprite.image.height
        if self.pose.x_update:
            self._sprite.x = TEXTURE_SIZE * self.pose.x + TEXTURE_SIZE / 2
        if self.pose.y_update:
            self._sprite.y = TEXTURE_SIZE * self.pose.y + TEXTURE_SIZE / 2
        if self.pose.theta_update:
            self._sprite.rotation = self.pose.theta

    def draw(self):
        self.__update()
        self._sprite.draw()


def add_from_image(element_class: GridDrawable, image_path: str,
                   grid: GameGrid, random_rotation: bool = False) -> None:
    """ Adds all objects from the given image to the given grid

    :param element_class: element class to add
    :param random_rotation: randomly rotates the objects in 90 degree increments
    :param image_path: Path to image
    :param grid: Grid to add objects to
    :return: None
    """
    bool_array = np.asarray(PILImage.open(image_path)) == 0
    for row_num, row in enumerate(bool_array):
        for col_num, element in enumerate(row):
            if element:
                if random_rotation:
                    grid.add(element_class(Pose(col_num, row_num, 90*randint(0, 3))))
                else:
                    grid.add(element_class(Pose(col_num, row_num)))
