import bisect
from collections import deque
from functools import wraps
from time import time, perf_counter
from typing import Callable, List


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def get_smooth_step_func(start: float, stop: float, time_constant: float) -> Callable[[float], float]:
    """ Get a function that returns a smooth step between start and stop

    :param start: position to start smoothing at
    :param stop: position to stop smoothing at
    :param time_constant: time constant for smoothing
    :return: A function that returns a smooth step between start and stop
    """

    def smooth_step(t: float) -> float:
        """ Smooth step function

        TODO: Some of this math is implemented wrong. When using Poses the width and height act funny

        :param t: Smooth step parameter. 0 <= t <= time_constant for smoothed values, outside that range either start
            or stop is returned
        :return: Smoothed value
        """
        if t <= 0:
            return start
        elif t >= time_constant:
            return stop
        else:
            m = t / time_constant
            return (stop - start) * (m * m * 3 - m * m * m * 2) + start

    return smooth_step


def smooth_step(start: float, stop: float, time_constant: float, t: float) -> float:
    """ Smooth step function
    TODO: Some of this math is implemented wrong. When using Poses the width and height act funny
    :param start: position to start smoothing at
    :param stop: position to stop smoothing at
    :param time_constant: time constant for smoothing
    :param t: Smooth step parameter. 0 <= t <= time_constant for smoothed values, outside that range either start
        or stop is returned
    :return: Smoothed value
    """
    if t <= 0:
        return start
    elif t >= time_constant:
        return stop
    else:
        m = t / time_constant
        return (stop - start) * (m * m * 3 - m * m * m * 2) + start


def override_dt_kwarg(func):
    """ Tracks dt and fills in for function calls that don't have it.
    dt is reset every time the function is called, regardless of if dt is included or not.
    Function calls including dt must be kwargs and not args.

    :param func: Function to wrap
    """
    prev_time = time()

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'dt' in kwargs:
            # dt = kwargs['dt']
            del kwargs['dt']
        # else:
        nonlocal prev_time
        dt = time() - prev_time
        prev_time = time()
        return func(*args, dt=dt, **kwargs)

    return wrapper


def bool_matrix_to_string(matrix: List[List[bool]]) -> str:
    """ Converts a 2D array of booleans to a string.

    :param matrix: The matrix to convert
    :return: The string representation of the matrix. 'X' for False, ',' for True, for visibility reasons.
    """
    s = ''

    for y in reversed(range(len(matrix[0]))):
        for x in range(len(matrix)):
            s += ',' if matrix[x][y] else 'x'
        s += '\n'
    return s


class DiscretePoint:
    """ Represents a discrete point in 2D space, with integer coordinates.
    """

    def __init__(self, x: int, y: int):
        """

        :param x: X coordinate
        :param y: Y coordinate
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other: 'DiscretePoint') -> bool:
        if not isinstance(other, DiscretePoint):
            return False
        return self.x == other.x and self.y == other.y

    def left(self) -> 'DiscretePoint':
        """
        :return: The point to the left of this point
        """
        return DiscretePoint(self.x - 1, self.y)

    def right(self) -> 'DiscretePoint':
        """
        :return: The point to the right of this point
        """
        return DiscretePoint(self.x + 1, self.y)

    def up(self) -> 'DiscretePoint':
        """
        :return: The point to the top of this point
        """
        return DiscretePoint(self.x, self.y + 1)

    def down(self) -> 'DiscretePoint':
        """
        :return: The point to the bottom of this point
        """
        return DiscretePoint(self.x, self.y - 1)

    def get_data_at_pt(self, matrix: List[List[any]]) -> any:
        """ Gets the data at this point in the matrix

        :param matrix: Matrix to query
        :return: Value at this point in the matrix
        """
        return matrix[self.x][self.y]

    def __call__(self, matrix: List[List[any]]) -> any:
        return self.get_data_at_pt(matrix)


def manhattan_dst(start: DiscretePoint, target: DiscretePoint) -> float:
    """ Manhattan distance between two points.

    :param start: Starting point.
    :param target: Target point.
    :return:
    """
    return abs(start.x - target.x) + abs(start.y - target.y)


def euclidian_dst(start: DiscretePoint, target: DiscretePoint) -> float:
    """ Euclidian distance between two points.

    :param start: Starting point.
    :param target: Target point.
    :return:
    """
    return ((start.x - target.x) ** 2 + (start.y - target.y) ** 2) ** 0.5


class PathFindingError(Exception):
    """ Raised when pathfinding fails.
    """

    def __init__(self, start: DiscretePoint, target: DiscretePoint, map: List[List[bool]]):
        super().__init__(f'No path found from {start} to {target} on map:\n{bool_matrix_to_string(map)}')


class _PathFindingPoint(DiscretePoint):
    """ Helper class for pathfinding over discrete grids
    """

    def __init__(self, x: int, y: int, target: DiscretePoint, parent: DiscretePoint = None):
        """

        :param x: X coordinate
        :param y: Y coordinate
        :param dst: Distance from target
        :param parent: Parent point in graph
        """
        super().__init__(x, y)
        self.target = target
        self.dst = 0.9*manhattan_dst(self, self.target) + 0.1*euclidian_dst(self, self.target)
        self.parent = parent

    def __str__(self) -> str:
        return f'_PathFindingPoint({self.x}, {self.y})'

    def __eq__(self, other: '_PathFindingPoint') -> bool:
        return self.x == other.x and self.y == other.y and self.dst == other.dst

    def __ne__(self, other: '_PathFindingPoint') -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: '_PathFindingPoint') -> bool:
        return self.dst < other.dst

    def __le__(self, other: '_PathFindingPoint') -> bool:
        return self.dst <= other.dst

    def __gt__(self, other: '_PathFindingPoint') -> bool:
        return self.dst > other.dst

    def __ge__(self, other: '_PathFindingPoint') -> bool:
        return self.dst >= other.dst

    def left(self) -> '_PathFindingPoint':
        """
        :return: The point to the left of this point
        """
        return _PathFindingPoint(self.x - 1, self.y, self.target, self)

    def right(self) -> '_PathFindingPoint':
        """
        :return: The point to the right of this point
        """
        return _PathFindingPoint(self.x + 1, self.y, self.target, self)

    def up(self) -> '_PathFindingPoint':
        """
        :return: The point to the top of this point
        """
        return _PathFindingPoint(self.x, self.y + 1, self.target, self)

    def down(self) -> '_PathFindingPoint':
        """
        :return: The point to the bottom of this point
        """
        return _PathFindingPoint(self.x, self.y - 1, self.target, self)

    def get_path(self) -> deque[DiscretePoint]:
        path = deque([self])
        while path[-1].parent is not None:
            path.append(path[-1].parent)
        for point in path:
            point = DiscretePoint(point.x, point.y)
        return deque(reversed(path))


class OrderedList(List):
    """ An ordered list implementation.
    Only append and pop are implemented.
    __contains__ uses binary search.

    # I'm sure there is a builtin for this, but I couldn't find it.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort()

    def append(self, item: any):
        bisect.insort(self, item)

    def add(self, item: any):
        self.append(item)

    def __str__(self):
        return f'OrderedList[{", ".join(str(i) for i in self)}]'


def a_star(start: DiscretePoint, target: DiscretePoint, grid: List[List[bool]]) -> deque[DiscretePoint]:
    """ A* pathfinding algorithm.

    :param start: Position to start from.
    :param target: Position to reach.
    :param grid: Map to search on. Truthy values are valid paths.
    :return: List of coordinates to follow.
    """
    start = _PathFindingPoint(start.x, start.y, target)
    target = _PathFindingPoint(target.x, target.y, target)
    if not target(grid):
        raise PathFindingError(start, target, grid)
    if start == target:
        return deque([start])

    unexplored: OrderedList[_PathFindingPoint] = OrderedList([start])
    explored: OrderedList[_PathFindingPoint] = OrderedList()

    while unexplored:
        current = unexplored.pop(0)
        if not current(grid):  # Obstacle
            continue
        elif current in explored:  # Already explored
            continue
        elif current == target:
            return current.get_path()
        explored.add(current)
        unexplored.add(current.left())
        unexplored.add(current.right())
        unexplored.add(current.up())
        unexplored.add(current.down())

    raise PathFindingError(start, target, grid)


def timeit(func):
    """ Decorator to time a function. Prints out time

    :param func: Function to time.
    """
    # https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
