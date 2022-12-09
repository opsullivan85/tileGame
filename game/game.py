from typing import List

from game.drawable import Drawable
from game.walls import Walls


class Game(Drawable):
    def __init__(self):
        self.drawables: Drawable = []
        self.walls: Walls = None

    def set_walls(self, walls: Walls):
        self.walls = walls

    def draw(self):
        for drawable in self.drawables:
            drawable.draw()
        self.walls.draw()
