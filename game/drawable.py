from abc import ABC, abstractmethod


class Drawable(ABC):
    """ Interface for things which can be drawn to the screen.
    """

    @abstractmethod
    def draw(self, camera: 'Camera', dt: float):
        ...
