from pyglet import image, sprite

from game.drawable import Drawable
from game.pose import Pose


class Sprite(Drawable):
    def __init__(self, image_path: str, pose: Pose, rotation_center: tuple = (0.5, 0.5)):
        self._pose: Pose = pose
        self._needs_update: bool = True

        texture = image.load(image_path)
        texture.anchor_x = int(texture.width * rotation_center[0])
        texture.anchor_y = int(texture.height * rotation_center[1])
        self._sprite: sprite = sprite.Sprite(texture, self.pose.x, self.pose.y)

    @property
    def pose(self):
        self._needs_update = True
        return self._pose

    def update(self):
        if self._needs_update:
            self._sprite.scale_x = self.pose.w / self._sprite.image.width
            self._sprite.scale_y = self.pose.h / self._sprite.image.height
            self._sprite.x = self.pose.x
            self._sprite.y = self.pose.y
            self._sprite.rotation = self.pose.theta
            self._needs_update = False

    def draw(self):
        self.update()
        self._sprite.draw()
