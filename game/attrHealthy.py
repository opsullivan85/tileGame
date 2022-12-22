from abc import ABC
from typing import Optional

from game.gridDrawable import GridDrawable
from pyglet import shapes


class AttrHealthy(GridDrawable, ABC):
    def __init__(self, health: int, max_health: Optional[int] = None, draw_health_bar: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._health = health
        self.health_updated = False
        if max_health is None:
            self.max_health = health
        else:
            self.max_health = max_health
        self.draw_health_bar = draw_health_bar
        self.health_bar = shapes.Line(0, 0, 0, 0, width=5, color=(255, 0, 0))
        self.health_bar.opacity = 150

        self.health_bar.x = self.texture_size * self.pose.x
        self.health_bar.x2 = (self.texture_size * self.pose.x + self.texture_size) * (self.health / self.max_health)
        self.health_bar.y = self.texture_size * self.pose.y + self.health_bar._width / 2
        self.health_bar.y2 = self.health_bar.y

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: float):
        if value != self._health:
            self._health = value
            self.health_updated = True

    def __update(self):
        """ Updates the visual properties of this sprite.
        TODO: Check if this is faster than just updating every frame.

        .. note::
            - Dunder naming is used to avoid name conflicts with subclasses.
            - This method is called automatically when the sprite is drawn.
        """
        if self.pose.x_updated or self.health_updated:
            if self.health <= self.max_health:
                self.health_bar.x = self.texture_size * self.pose.x
                self.health_bar.x2 = self.texture_size * self.pose.x \
                                     + (self.texture_size * (self.health / self.max_health))
            else:  # Centered here looks better
                shift = self.texture_size * (self.health / self.max_health - 1) / 2
                self.health_bar.x = self.texture_size * self.pose.x - shift
                self.health_bar.x2 = self.texture_size * self.pose.x + self.texture_size + shift
            self.health_updated = False
        if self.pose.y_updated:
            self.health_bar.y = self.texture_size * self.pose.y + self.health_bar._width / 2
            self.health_bar.y2 = self.health_bar.y

    def draw(self):
        if self.draw_health_bar:
            self.__update()
        super().draw()
        # Draw health bar under sprite
        self.health_bar.draw()