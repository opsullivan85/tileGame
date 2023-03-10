from abc import ABC
from collections import deque
from typing import Optional, Union, List

from pyglet import shapes
from pyglet.shapes import ShapeBase
from pyglet.sprite import Sprite

from game.camera import Camera
from game.constants import GRID_WIDTH, GRID_HEIGHT
from game.gridDrawable import GridDrawable
from game.gridObject import GridObject
from game.math import a_star, PathFindingError
from game.pose import Pose


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

    def overlaps(self, others: List['GridObject']) -> None:
        for other in others:
            if isinstance(other, AttrHealthy):
                self.attack(other)


class AttrHealing(GridObject, ABC):
    def __init__(self, healing: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.healing = healing
        self.is_path_following = False

    def heal(self, other: AttrHealthy) -> None:
        other.health += self.healing


class AttrPathFinding(GridObject, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__path: deque[Pose] = deque()
        self.__wrap = False
        self.is_path_following = False
        self.actively_path_finding = False
        self.active_path_finding_target = None

    def set_path(self, path: deque[Pose], wrap: bool = False):
        """ Sets the path to follow.

        :param path: Path to follow.
        :param wrap: If True, the path will be repeated, otherwise it will be followed once.
        """
        self.__path = path
        self.__wrap = wrap
        if not self.__wrap and self.__path is not None:
            self.__path.popleft()  # Remove current position

    def follow_path(self) -> bool:
        """ Follows the path set by set_path().

        .. Note:: If the path is blocked, the next position will not be consumed
        in effect it will sit there until the path is clear.

        :return: False if path is finished, True otherwise
        """
        if self.__wrap:
            if len(self.__path) == 1:
                next_pose = self.__path[0]
            else:
                next_pose = self.__path[1]
        else:
            next_pose = self.__path[0]

        success = self.move_to_position(next_pose)
        if success and not self.__wrap:
            self.__path.popleft()
        elif success:
            self.__path.rotate(-1)

        done = len(self.__path) == 0
        if done:
            self.is_path_following = False
        return not done

    def path_find(self, target: Pose) -> bool:
        """ Finds a path to the target and sets it.

        :param target: Target to find a path to.
        :return: True if a path was found, False otherwise.
        """
        try:
            path = a_star(self.pose.as_discrete_point(),
                          target.as_discrete_point(),
                          self.grid.get_collision_matrix(self))
        except PathFindingError:
            return False
        path = deque([Pose.from_discrete_point(p) for p in path])
        self.set_path(path)
        return True

    def actively_path_find(self, target: GridObject) -> bool:
        """ Finds a path to the target and sets it.
        Keeps updating pathfinding forever.

        :param target: Target to find a path to.
        :return: True if a path was found, False otherwise.
        """
        try:
            path = a_star(self.pose.as_discrete_point(),
                          target.pose.as_discrete_point(),
                          self.grid.get_collision_matrix(self))
        except PathFindingError:
            return False
        self.actively_path_finding = True
        self.active_path_finding_target = target
        path = deque([Pose.from_discrete_point(p) for p in path])
        self.set_path(path)
        return True

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.actively_path_finding:
            self.actively_path_find(self.active_path_finding_target)
