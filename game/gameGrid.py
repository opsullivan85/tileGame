from typing import List

from multipledispatch import dispatch
from multiprocessing import Process
from threading import Thread

from game.camera import Camera
from game.gridDrawable import GridDrawable
from game.gridObject import GridObject
from game.math import timeit
from game.pose import Pose


class GameGrid():
    """ Class manages the grid of the game.
    """

    def __init__(self, height, width):
        """

        :param height: Height of the grid
        :param width: Width of the grid
        """
        super().__init__()
        self.height = height
        self.width = width
        self.grid: List[List[List[GridObject]]] = [[[] for _ in range(height)] for _ in range(width)]
        self.elements: List[GridObject] = []
        self.drawables: List[Drawable] = []
        self.always_update_list: List[GridObject] = []
        self.update_list: List[GridObject] = []

    def add(self, element: GridObject):
        """ Tries to add an object to the grid

        :param element: The object to add
        :return: if the object was successfully added
        """
        element.grid = self
        if not element.move_to_position(element.pose):
            raise CouldNotAddToGridException(element, element.pose)
        self.elements.append(element)
        if issubclass(type(element), GridDrawable):
            # inspector doesn't realize that element is guaranteed to be a Drawable here
            # noinspection PyTypeChecker
            self.drawables.append(element)
        if element.update_every_frame:
            self.always_update_list.append(element)

    def remove(self, element: GridObject) -> bool:
        """ Tries to remove an object from the grid

        :param element: The object to remove
        :return: if the object was successfully removed
        """
        if element in self.elements:
            self.elements.remove(element)
            self.grid[element.pose.x][element.pose.y].remove(element)
            if issubclass(type(element), Drawable):
                # inspector doesn't realize that element is guaranteed to be a Drawable here
                # noinspection PyTypeChecker
                self.drawables.remove(element)
            try:
                # element.update_every_frame could have changed since the element was added
                self.always_update_list.remove(element)
            except ValueError:
                ...
            return True
        return False

    def get_collision_matrix(self, element: GridObject) -> List[List[bool]]:
        """ Returns a 2D array of booleans indicating if a position can be occupied for the element or not.

        :param element: The element to check for
        :return: A 2D array of booleans
        """
        return [[element.can_coexist(self.get(x, y)) for y in range(self.height)] for x in range(self.width)]

    @dispatch(Pose)
    def get(self, pose: Pose) -> List[GridObject]:
        """ Gets the objects at the given position

        :param pose: Position to get objects at
        :return: List of objects at the given position
        """
        return self.grid[pose.x][pose.y]

    @dispatch(int, int)
    def get(self, x: int, y: int) -> List[GridObject]:
        """ Gets the objects at the given position

        :param x: X position to get objects at
        :param y: Y position to get objects at
        :return: List of objects at the given position
        """
        return self.grid[x][y]

    def equals(self, other: 'GameGrid') -> bool:
        """ Compares two game grids.
        Two game grids are equal if they have elements in the same places that agree on their equality.
        Layer order is enforced.

        :param other: The other object to compare to
        """
        return self.grid == other.grid

    def draw(self, camera: Camera, dt: float):
        for element in self.drawables:
            element.draw(camera, dt)

    def update(self, dt: float = 1):
        for element in self.always_update_list + self.update_list:
            element.update(dt)
        self.update_list = []
        for element in self.elements:
            element.overlaps(self.get(element.pose))

        # # This is not the correct way to do this, also the pyglet objects cannot be pickled
        # # Would be nice to get working in the future
        # procs = []
        # for element in self.always_update_list + self.update_list:
        #     proc = Thread(target=element.update, args=(dt,))
        #     procs.append(proc)
        #     proc.start()
        # self.update_list = []
        # for proc in procs:
        #     proc.join()
        #
        # procs = []
        # for element in self.elements:
        #     proc = Thread(target=element.overlaps, args=(self.get(element.pose),))
        #     procs.append(proc)
        #     proc.start()
        # for proc in procs:
        #     proc.join()

    def __str__(self):
        s = ''
        for y in reversed(range(self.height)):
            for x in range(self.width):
                s += f'{len(self.grid[x][y]) if self.grid[x][y] else "."}'
            s += '\n'
        return s


class CouldNotAddToGridException(Exception):
    """ Exception raised when an object could not be added to the grid"""

    def __init__(self, element: GridObject, pose: Pose):
        """

        :param element: Element that could not be added
        :param pose: Pose that the element could not be added to
        """
        self.element = element
        self.pose = pose
        super().__init__(f'Could not add {element} to grid at {pose}')
