from abc import ABC, abstractmethod
from random import randint
from typing import List, Type

import numpy as np
from PIL import Image as PILImage

from game.pose import Pose


class GridObject(ABC):
    """ Interface for things which can be placed on the game grid
    """
    update_every_frame = False

    @abstractmethod
    def __init__(self, pose: Pose = Pose()):
        self.grid: 'GameGrid' = None
        self._pose = pose

    @property
    def pose(self) -> Pose:
        return self._pose

    @pose.setter
    def pose(self, other: Pose):
        self._pose = other

    def add_to_grid(self, grid: 'GameGrid') -> bool:
        """ Add the object to the given grid

        :param grid: grid to add to
        :return: bool, True if the add was successful, False otherwise
        """
        return grid.add(self)

    def move_to_position(self, pose: Pose) -> bool:
        """ Move the object to the given position on the grid

        :param pose: position to move to
        :return: bool, True if the move was successful, False otherwise
        """
        for element in self.grid.get(pose):
            if not self.can_coexist(element):
                return False
        try:
            self.grid.get(self.pose).remove(self)
        except ValueError:
            ...  # Object was not in the grid, happens on first adding to grid
        self.pose = pose
        self.grid.get(self.pose).append(self)
        return True

    @abstractmethod
    def can_coexist(self, other: 'GridObject') -> bool:
        """ Whether or not this object can coexist with another object on the grid

        :param other: Other grid object
        :return: bool, true if this object can coexist with the other object
        """
        ...

    @abstractmethod
    def overlaps(self, others: List['GridObject']) -> None:
        """ Handle overlapping with other objects on the grid every frame

        :param others: Objects this object overlaps with, including self
        :return: None
        """
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        """ Handle updates, called every frame if class variable update_every_frame is True

        :param dt: Time since last update
        :return: None
        """
        ...

    @abstractmethod
    def __eq__(self, other: 'GridObject') -> bool:
        """ Checks equality, overrides the == operator.
        Important for testing.

        :param other: Other object to compare to
        :return: if the objects are equal
        """
        ...


def add_from_image(grid: 'GameGrid', element_class: Type[GridObject],
                   image_path: str, random_rotation: bool = False) -> None:
    """ Adds all objects from the given image to the given grid

    :param element_class: element class to add
    :param random_rotation: randomly rotates the objects in 90 degree increments
    :param image_path: Path to image
    :param grid: Grid to add objects to
    :return: None
    """
    bool_array = np.asarray(PILImage.open(image_path)) == 0
    for row_num, row in enumerate(reversed(bool_array)):
        for col_num, element in enumerate(row):
            if element:
                grid.add(element_class(
                    Pose(col_num, row_num, 90 * randint(0, 3) * random_rotation)
                ))
