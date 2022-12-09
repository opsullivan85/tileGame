from typing import List

from game.drawable import Drawable


class Walls(Drawable):
    def __init__(self, layout: List[List[bool]]):
        self.layout = layout

    def draw(self):
        ...