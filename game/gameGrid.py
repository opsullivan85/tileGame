from typing import List

from game.drawable import Drawable
from game.gridObject import GridObject
from game.pose import Pose


# TODO: handle edge cases (literally).
#  Elements at the top and right of the grid throw exceptions if they try to escape
#  Elements at the bottom and left of the grid can effect the other side of the grid without being visible
class GameGrid(Drawable):
    """ Class manages the grid of the game.
    """

    def __init__(self, height, width):
        """

        :param height: Height of the grid
        :param width: Width of the grid
        """
        self.height = height
        self.width = width
        self.grid = [[[] for _ in range(height)] for _ in range(width)]
        self.elements: List[GridObject] = []
        self.drawables: List[Drawable] = []
        self.always_update_list: List[GridObject] = []
        self.update_list: List[GridObject] = []

    def add(self, element: GridObject) -> bool:
        """ Tries to add an object to the grid

        :param element: The object to add
        :return: if the object was successfully added
        """
        element.grid = self
        # Add to list of elements if element was successfully added to grid
        if return_val := element.move_to_position(element.pose):
            self.elements.append(element)
            if issubclass(type(element), Drawable):
                self.drawables.append(element)
            if element.update_every_frame:
                self.always_update_list.append(element)
        return return_val

    def remove(self, element: GridObject) -> bool:
        """ Tries to remove an object from the grid

        :param element: The object to remove
        :return: if the object was successfully removed
        """
        if element in self.elements:
            self.elements.remove(element)
            self.grid[element.pose.x][element.pose.y].remove(element)
            try:
                self.drawables.remove(element)
            except ValueError:
                ...
            try:
                self.always_update_list.remove(element)
            except ValueError:
                ...
            return True
        return False

    def get(self, pose: Pose) -> List[GridObject]:
        """ Gets the objects at the given position

        :param pose: Position to get objects at
        :return: List of objects at the given position
        """
        return self.grid[pose.x][pose.y]

    def __eq__(self, other: 'GameGrid') -> bool:
        """ Compares two game grids.
        Two game grids are equal if they have elements in the same places that agree on their equality.
        Layer order is enforced.

        :param other: The other object to compare to
        """
        return self.grid == other.grid

    def draw(self):
        for element in self.drawables:
            element.draw()

    def update(self, dt: float = 1):
        for element in self.always_update_list + self.update_list:
            element.update(dt)
        self.update_list = []
