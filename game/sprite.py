from game.drawable import Drawable
from pyglet import image, sprite

from game.pose import Pose


class Sprite(Drawable):
    def __init__(self, image_path: str, pose: Pose):
        self.pose: Pose = pose
        self._sprite: sprite = sprite.Sprite(image.load(image_path), self.pose.x, self.pose.y)

    def update(self):
        self._sprite.scale_x = self.pose.w/self._sprite.image.width
        self._sprite.scale_y = self.pose.h/self._sprite.image.height
        self._sprite.x = self.pose.x
        self._sprite.y = self.pose.y

    def draw(self):
        self.update()
        self._sprite.draw()
