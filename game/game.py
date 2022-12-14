from typing import List

from game.Constants import WINDOW_PIXEL_WIDTH, WINDOW_PIXEL_HEIGHT
from game.drawable import Drawable
from game.gameGrid import GameGrid
from game.gridObject import add_from_image
from game.pose import Pose
from game.wall import Wall
from pyglet import window
from pyglet.window import key


class Game(window.Window):
    def __init__(self):
        super().__init__(width=WINDOW_PIXEL_WIDTH, height=WINDOW_PIXEL_HEIGHT)
        self.grid = GameGrid()
        self.init_walls()

    def init_walls(self):
        add_from_image(self.grid, Wall, '../DrinkTheBeer/resources/map.png')

    def draw(self):
        self.grid.draw()

    def on_draw(self):
        self.grid.update()
        self.clear()
        self.draw()

    def on_key_press(self, symbol, modifiers):
        print(symbol, modifiers)
        if symbol == key.W:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose + Pose(0, 1))
        elif symbol == key.A:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose - Pose(1, 0))
        elif symbol == key.S:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose - Pose(0, 1))
        elif symbol == key.D:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose + Pose(1, 0))
