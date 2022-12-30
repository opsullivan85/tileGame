from abc import ABC, abstractmethod
from random import randint
from typing import List, Type

import numpy as np
from PIL import Image as PILImage

from game.pose import Pose


class GridObject(ABC):
    """ Abstract class for things which can be placed on the game grid
    """
    update_every_frame = False

    def __init__(self, pose: Pose = Pose()):
        super().__init__()
        self.grid: 'GameGrid' = None
        self.pose = pose
        # Size of the object, in terms of space taken up within the grid
        self.tile_size = 5

    def add_to_grid(self, grid: 'GameGrid') -> bool:
        """ Add the object to the given grid

        :param grid: grid to add to
        :return: bool, True if the add was successful, False otherwise
        """
        return grid.add(self)

    def remove_from_grid(self) -> bool:
        """ Remove the object from the grid

        :return: bool, True if the remove was successful, False otherwise
        """
        return self.grid.remove(self)

    def move_to_position(self, pose: Pose) -> bool:
        """ Move the object to the given position on the grid.

        .. note:: Below is an overview of how the method works

            - Bounds check on desired pose, potentially return
            - Perform collisions with other objects at pose. There is a case to be made for having this one step later
              but it is easy to change later.
            - Check to see if object can coexist with other objects at the desired pose, potentially return
            - Move to position

        :param pose: position to move to
        :return: bool, True if the move was successful, False otherwise
        """
        # Check if given position is in bounds
        if pose.x < 0 or pose.x >= self.grid.width or pose.y < 0 or pose.y >= self.grid.height:
            return False

        # Perform collision simulations between this object and all other objects at the given position
        for other in self.grid.get(pose):
            self.collision(other)
            other.collision(self)

        # Check if the object can coexist with other objects at the given position
        if not self.can_coexist(self.grid.get(pose)):
            return False

        # Remove from old position.
        # Try except could be avoided with a check to self.grid.objects,
        # but this is more efficient since it only checks the grid once and will rarely fail
        try:
            self.grid.get(self.pose).remove(self)
        except ValueError:
            ...  # Object was not in the grid, happens on first adding to grid

        # Update pose and add to new position
        self.pose.set_to(pose)
        self.grid.get(self.pose).append(self)
        return True

    @abstractmethod
    def can_coexist(self, others: List['GridObject']) -> bool:
        """ Whether this object can coexist with other objects on the grid at this tile

        :param others: Other grid objects at this tile
        :return: bool, true if this object can coexist with the other object
        """
        total_size = self.tile_size + sum([other.tile_size for other in others])
        return total_size <= 5

    @abstractmethod
    def overlaps(self, others: List['GridObject']) -> None:
        """ Handle overlapping with other objects on the grid every frame

        :param others: Objects this object overlaps with, including self
        :return: None
        """
        ...

    @abstractmethod
    def collision(self, other: 'GridObject') -> None:
        """ Called when this object collides with another object. Called on every pair of objects that collide,
        once for each object. Should not return anything. Typically called before a can_coexist check.

        .. note:: Be careful modifying `other` because both self.collision(other) and other.collision(self) will be called
        and effects should not be applied twice.

        .. see:: can_coexist
        :param other: Other object
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
    def equals(self, other: 'GridObject') -> bool:
        """ Checks equality, does not override the == operator.
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
