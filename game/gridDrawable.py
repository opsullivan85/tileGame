from abc import ABC, abstractmethod
from pyglet.sprite import Sprite

from game.camera import Camera
from game.gridObject import GridObject
from game.pose import Pose


class GridDrawable(GridObject, ABC):
    """ Abstract class for drawable grid objects
    """

    def __init__(self, pose: Pose = Pose()):
        """

        :param pose: Starting pose of the object
        :param img: Pyglet image to use for the sprite texture
        :param rotation_center: Center of rotation for the sprite, must be set before initialization
        :param texture_size: size to display the texture at
        """
        super().__init__(pose)

    @abstractmethod
    def draw(self, camera: Camera, pose: Pose, sprite: Sprite, dt: float):
        camera.draw(pose, sprite)
