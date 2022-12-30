from abc import ABC
from typing import Optional, Union

from pyglet import shapes
from pyglet.shapes import ShapeBase
from pyglet.sprite import Sprite

from game.camera import Camera
from game.constants import GRID_WIDTH, GRID_HEIGHT
from game.gridDrawable import GridDrawable
from game.gridObject import GridObject


class AttrHealthy(GridDrawable, ABC):
    def __init__(self, health: int, max_health: Optional[int] = None, draw_health_bar: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._health = health
        self.health_updated = False
        if max_health is None:
            self.max_health = health
        else:
            self.max_health = max_health
        self.health_bar = shapes.Line(0, 0, 0, 0, width=5, color=(255, 0, 0))
        self.health_bar.opacity = 150
        self._draw_health_bar = draw_health_bar
        self.draw_health_bar = draw_health_bar

        self.health_bar.x = self.texture_size * self.pose.x
        self.health_bar.x2 = (self.texture_size * self.pose.x + self.texture_size) * (self.health / self.max_health)
        self.health_bar.y = self.texture_size * self.pose.y + self.health_bar._width / 2
        self.health_bar.y2 = self.health_bar.y

    def is_alive(self):
        return self.health > 0

    def is_dead(self):
        return self.health <= 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: float):
        if value != self._health:
            self._health = value
            self.health_updated = True

    @property
    def draw_health_bar(self):
        return self._draw_health_bar

    @draw_health_bar.setter
    def draw_health_bar(self, value: bool):
        self._draw_health_bar = value
        self.health_bar.visible = value

    def __update(self, camera: Camera):
        """ Updates the visual properties of this sprite.
        TODO: Check if this is faster than just updating every frame.

        .. note::
            - Dunder naming is used to avoid name conflicts with subclasses.
            - This method is called automatically when the sprite is drawn.
        """
        if self.health <= self.max_health:
            self.health_bar.x = self.texture_size * (self.pose.x - 0.5) \
                                - (camera.pose.x - GRID_WIDTH / 2) * self.texture_size
            self.health_bar.x2 = self.texture_size * (self.pose.x - 0.5) \
                                 + (self.texture_size * (self.health / self.max_health)) \
                                 - (camera.pose.x - GRID_WIDTH / 2) * self.texture_size
        else:  # Centered here looks better
            shift = self.texture_size * (self.health / self.max_health - 1) / 2
            self.health_bar.x = self.texture_size * (self.pose.x - 0.5) - shift \
                                - (camera.pose.x - GRID_WIDTH / 2) * self.texture_size
            self.health_bar.x2 = self.texture_size * (self.pose.x - 0.5) + self.texture_size + shift \
                                 - (camera.pose.x - GRID_WIDTH / 2) * self.texture_size
        self.health_bar.y = self.texture_size * (self.pose.y - 0.5) + self.health_bar._width / 2 \
                            - (camera.pose.y - GRID_HEIGHT / 2) * self.texture_size
        self.health_bar.y2 = self.health_bar.y

    def get_sprites(self) -> list[Union[Sprite, ShapeBase]]:
        return super().get_sprites() + [self.health_bar]

    def draw(self, camera: Camera, dt: float):
        if self.draw_health_bar:
            self.__update(camera)
        super().draw(camera, dt)
        # Draw health bar under sprite
        self.health_bar.draw()


class AttrHarmful(GridObject, ABC):
    def __init__(self, damage: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage

    def attack(self, other: AttrHealthy) -> None:
        other.health -= self.damage


class AttrHealing(GridObject, ABC):
    def __init__(self, healing: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.healing = healing

    def heal(self, other: AttrHealthy) -> None:
        other.health += self.healing
