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
        return self.x == other.x and \
            self.y == other.y and \
            self.theta == other.theta and \
            self.w == other.w and \
            self.h == other.h

    def __str__(self):
        return f'(x={"*" * self.x_updated}{self.x}, ' \
               f'y={"*" * self.y_updated}{self.y}, ' \
               f'theta={"*" * self.theta_updated}{self.theta}, ' \
               f'w={"*" * self.w_updated}{self.w}, ' \
               f'h={"*" * self.h_updated}{self.h})'

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

    def __add__(self, other):
        """ Add two poses together like vectors, **ignoring width and height**.
        """
        return Pose(self.x + other.x, self.y + other.y, self.theta + other.theta, self.w, self.h)

    def __sub__(self, other):
        """ Subtract two poses like vectors, **ignoring width and height**.
        """
        return Pose(self.x - other.x, self.y - other.y, self.theta - other.theta, self.w, self.h)

    def __mul__(self, other):
        """ Multiply two poses like vectors, **including width and height**.
        """
        return Pose(self.x * other.x, self.y * other.y, self.theta * other.theta, self.w * other.w, self.h * other.h)

    def __truediv__(self, other):
        """ Divide two poses like vectors, **including width and height**.

        warnings:: This is not a floor division. GameGrids do not like working with floats.
        """
        return Pose(self.x / other.x, self.y / other.y, self.theta / other.theta, self.w / other.w, self.h / other.h)

    def __floordiv__(self, other):
        """ Divide two poses like vectors, flooring, **including width and height**.
        """
        return Pose(self.x // other.x, self.y // other.y, self.theta // other.theta, self.w // other.w,
                    self.h // other.h)

    def set_to(self, other: 'Pose'):
        """ Set the pose to the values of another pose.
        Respects update variables.

        :param other: The other pose to copy
        """
        if other.x != self.x:
            self.x = other.x
        if other.y != self.y:
            self.y = other.y
        if other.theta != self.theta:
            self.theta = other.theta
        if other.w != self.w:
            self.w = other.w
        if other.h != self.h:
            self.h = other.h

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
