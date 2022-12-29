from typing import Union
from math import isclose


class Pose:
    """ Class for storing and manipulating poses.
    """

    def __init__(self, x: float = 0, y: float = 0, theta: float = 0, w: float = 1, h: float = 1):
        self._x = x
        self.x_updated = True
        self._y = y
        self.y_updated = True
        self._theta = theta
        self.theta_updated = True
        self._w = w
        self.w_updated = True
        self._h = h
        self.h_updated = True

    def __eq__(self, other):
        return isclose(self.x, other.x) \
            and isclose(self.y, other.y) \
            and isclose(self.theta, other.theta) \
            and isclose(self.w, other.w) \
            and isclose(self.h, other.h)

    def __str__(self):
        return f'(x={"*" * self.x_updated}{self.x:.3f}, ' \
               f'y={"*" * self.y_updated}{self.y:.3f}, ' \
               f'theta={"*" * self.theta_updated}{self.theta:.3f}, ' \
               f'w={"*" * self.w_updated}{self.w:.3f}, ' \
               f'h={"*" * self.h_updated}{self.h:.3f})'

    def any_updated(self) -> bool:
        """ Check if any of the pose attributes have been updated.
        Resets after every game engine update.
        """
        return self.x_updated or self.y_updated or self.theta_updated or self.w_updated or self.h_updated

    def coordinates_equal(self, other: 'Pose') -> bool:
        """ Check if the coordinates of two poses are equal

        :param other: The other object to compare to
        :return: True if the coordinates of the two poses are equal
        """
        return self.x == other.x and self.y == other.y

    def get_coordinates_as_pose(self) -> 'Pose':
        """ Get a new pose with the same coordinates as this pose.
        Without rotation or size.
        """
        return Pose(self.x, self.y)

    def sizes_equal(self, other: 'Pose') -> bool:
        """ Check if the sizes of two poses are equal

        :param other: The other object to compare to
        :return: True if the sizes of the two poses are equal
        """
        return self.w == other.w and self.h == other.h

    def get_size_as_pose(self) -> 'Pose':
        """ Get a new pose with the same size as this pose.
        Without rotation or coordinates.
        """
        return Pose(0, 0, w=self.w, h=self.h)

    def rotation_equal(self, other: 'Pose') -> bool:
        """ Check if the rotations of two poses are equal

        :param other: The other object to compare to
        :return: True if the rotations of the two poses are equal
        """
        return self.theta == other.theta

    def get_rotation_as_pose(self) -> 'Pose':
        """ Get a new pose with the same rotation as this pose.
        Without coordinates or size.
        """
        return Pose(0, 0, theta=self.theta)

    def __add__(self, other: 'Pose'):
        """ Add two poses together like vectors, **ignoring width and height**.
        """
        return Pose(self.x + other.x, self.y + other.y, self.theta + other.theta, self.w, self.h)

    def __sub__(self, other: 'Pose'):
        """ Subtract two poses like vectors, **ignoring width and height**.
        """
        return Pose(self.x - other.x, self.y - other.y, self.theta - other.theta, self.w, self.h)

    def __mul__(self, other: Union['Pose', float]):
        """ Multiply two poses like vectors, **including width and height**.
        Or multiply a pose and a scalar, **including width and height**.
        """
        if isinstance(other, Pose):
            return Pose(self.x * other.x,
                        self.y * other.y,
                        self.theta * other.theta,
                        self.w * other.w,
                        self.h * other.h)
        else:
            return Pose(self.x * other,
                        self.y * other,
                        self.theta * other,
                        self.w * other,
                        self.h * other)

    def __truediv__(self, other: Union['Pose', float]):
        """ Divide two poses like vectors, **including width and height**.
        Or divide a pose and a scalar, **including width and height**.

        warnings:: This is not a floor division. GameGrids do not like working with floats.
        """
        if isinstance(other, Pose):
            return Pose(self.x / other.x,
                        self.y / other.y,
                        self.theta / other.theta,
                        self.w / other.w,
                        self.h / other.h)
        else:
            return Pose(self.x / other,
                        self.y / other,
                        self.theta / other,
                        self.w / other,
                        self.h / other)

    def __floordiv__(self, other: Union['Pose', float]):
        """ Divide two poses like vectors, flooring, **including width and height**.
        Or divide a pose and a scalar, flooring, **including width and height**.
        """
        if isinstance(other, Pose):
            return Pose(self.x // other.x,
                        self.y // other.y,
                        self.theta // other.theta,
                        self.w // other.w,
                        self.h // other.h)
        else:
            return Pose(self.x // other,
                        self.y // other,
                        self.theta // other,
                        self.w // other,
                        self.h // other)

    def set_to(self, other: 'Pose') -> 'Pose':
        """ Set the pose to the values of another pose.
        Respects update variables.

        :param other: The other pose to copy
        :return: The pose itself
        """
        self.x = other.x
        self.y = other.y
        self.theta = other.theta
        self.w = other.w
        self.h = other.h
        return self

    def reset_updates(self):
        """ Reset the update flags for all pose attributes
        """
        self.x_updated = False
        self.y_updated = False
        self.theta_updated = False
        self.w_updated = False
        self.h_updated = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value != self._x:
            self._x = value
            self.x_updated = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value != self._y:
            self._y = value
            self.y_updated = True

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        if value != self._theta:
            self._theta = value
            self.theta_updated = True

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        if value != self._w:
            self._w = value
            self.w_updated = True

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        if value != self._h:
            self._h = value
            self.h_updated = True
