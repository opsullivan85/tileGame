from typing import List

from game.drawable import Drawable
from abc import ABC, abstractmethod

from game.pose import Pose


class GridObject(ABC):
    """ Interface for things which can be placed on the game grid
    """

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

        :param others: Objects this object overlaps with
        :return: None
        """
        ...
