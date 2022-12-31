from abc import ABC
from typing import Union

from pyglet import image, sprite
from pyglet.shapes import ShapeBase
from pyglet.sprite import Sprite

from game.camera import Camera
from game.constants import TEXTURE_SIZE, GRID_WIDTH, GRID_HEIGHT
from game.drawable import Drawable
from game.gridObject import GridObject
from game.pose import Pose


class GridDrawable(GridObject, Drawable, ABC):
    """ Abstract class for drawable grid objects
    """

    def __init__(self, pose: Pose = Pose(), img: image.AbstractImage = None, rotation_center: tuple = (0.5, 0.5),
                 texture_size: int = TEXTURE_SIZE):
        """

        :param pose: Starting pose of the object
        :param img: Pyglet image to use for the sprite texture
        :param rotation_center: Center of rotation for the sprite, must be set before initialization
        :param texture_size: size to display the texture at
        """
        super().__init__(pose)
        self.texture_size = texture_size
        img.anchor_x = int(img.width * rotation_center[0])
        img.anchor_y = int(img.height * rotation_center[1])
        self._sprite: sprite.Sprite = sprite.Sprite(img, self.pose.x, self.pose.y)

    def __update(self, camera: Camera):
        """ Updates the visual properties of this sprite.
        TODO: Check if this is faster than just updating every frame.

        .. note::
            - Dunder naming is used to avoid name conflicts with subclasses.
            - This method is called automatically when the sprite is drawn.
            - I'm not sure if the extra work of checking for pose updates actually makes it faster.
        """
        self._sprite.scale_x = self.texture_size * self.pose.w / self._sprite.image.width
        self._sprite.scale_y = self.texture_size * self.pose.h / self._sprite.image.height
        self._sprite.x = self.texture_size * self.pose.x - (camera.pose.x - GRID_WIDTH / 2) * self.texture_size
        self._sprite.y = self.texture_size * self.pose.y - (camera.pose.y - GRID_HEIGHT / 2) * self.texture_size
        self._sprite.rotation = self.pose.theta

    def get_sprites(self) -> list[Union[Sprite, ShapeBase]]:
        return [self._sprite]

    def draw(self, camera: Camera, dt: float):
        self.__update(camera)
        self._sprite.draw()
