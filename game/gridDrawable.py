from abc import ABC

from pyglet import image, sprite

from game.constants import TEXTURE_SIZE
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
        self._sprite: sprite = sprite.Sprite(img, self.pose.x, self.pose.y)

    def __update(self):
        """ Updates the visual properties of this sprite.

        Notes:
            - Dunder naming is used to avoid name conflicts with subclasses.
            - This method is called automatically when the sprite is drawn.
            - I'm not sure if the extra work of checking for pose updates actually makes it faster.
                TODO: Check if this is faster than just updating every frame.

        """
        if self.pose.w_updated:
            self._sprite.scale_x = self.texture_size * self.pose.w / self._sprite.image.width
        if self.pose.h_updated:
            self._sprite.scale_y = self.texture_size * self.pose.h / self._sprite.image.height
        if self.pose.x_updated:
            self._sprite.x = self.texture_size * self.pose.x + self.texture_size / 2
        if self.pose.y_updated:
            self._sprite.y = self.texture_size * self.pose.y + self.texture_size / 2
        if self.pose.theta_updated:
            self._sprite.rotation = self.pose.theta
        self.pose.reset_updates()

    def draw(self):
        self.__update()
        self._sprite.draw()
