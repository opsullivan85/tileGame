from typing import List

from game.Constants import *
from game.drawable import Drawable
from game.gridObject import GridObject
from game.pose import Pose


class GameGrid(Drawable):
    def __init__(self):
        self.grid = [[[] for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.elements: List[GridObject] = []
        self.drawables: List[Drawable] = []

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
        return return_val

    def remove(self, element: GridObject) -> bool:
        """ Tries to remove an object from the grid

        :param element: The object to remove
        :return: if the object was successfully removed
        """
        if element in self.elements:
            self.elements.remove(element)
            try:
                self.drawables.remove(element)
            except ValueError:
                ...
            return True
        return False

    def remove(self, element: GridObject) -> bool:
        """ Tries to remove an object from the grid

        :param element: The object to remove
        :return: if the object was successfully removed
        """
        if element in self.elements:
            self.elements.remove(element)
            try:
                self.drawables.remove(element)
            except ValueError:
                ...
            return True
        return False

    def get(self, pose: Pose) -> List[GridObject]:
        """ Gets the objects at the given position

        :param position: Position to get objects at
        :return: List of objects at the given position
        """
        print(pose.x, pose.y)
        return self.grid[pose.x][pose.y]

    def draw(self):
        for element in self.drawables:
            element.draw()
