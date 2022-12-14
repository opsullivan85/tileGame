

class Pose:
    def __init__(self, x: float = 0, y: float = 0, theta: float = 0, w: float = 1, h: float = 1):
        self._x = x
        self.x_update = True
        self._y = y
        self.y_update = True
        self._theta = theta
        self.theta_update = True
        self._w = w
        self.w_update = True
        self._h = h
        self.h_update = True

    def __add__(self, other):
        return Pose(self.x + other.x, self.y + other.y, self.theta + other.theta, self.w + other.w, self.h + other.h)

    def __sub__(self, other):
        return Pose(self.x - other.x, self.y - other.y, self.theta - other.theta, self.w - other.w, self.h - other.h)

    def __mul__(self, other):
        return Pose(self.x * other.x, self.y * other.y, self.theta * other.theta, self.w * other.w, self.h * other.h)

    def __truediv__(self, other):
        return Pose(self.x / other.x, self.y / other.y, self.theta / other.theta, self.w / other.w, self.h / other.h)

    def reset_updates(self):
        self.x_update = False
        self.y_update = False
        self.theta_update = False
        self.w_update = False
        self.h_update = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.x_update = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.y_update = True

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        self._theta = value
        self.theta_update = True

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self.w_update = True

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value
        self.h_update = True
