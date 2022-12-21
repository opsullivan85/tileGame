from pyglet import window
from pyglet.window import key

from game.constants import WINDOW_PIXEL_WIDTH, WINDOW_PIXEL_HEIGHT, GRID_HEIGHT, GRID_WIDTH
from game.gameGrid import GameGrid
from game.gridObject import add_from_image
from game.pose import Pose
from game.resources import get_resource_path
from game.wall import Wall


class Game(window.Window):
    """ Main game class.
    """
    def __init__(self):
        super().__init__(width=WINDOW_PIXEL_WIDTH, height=WINDOW_PIXEL_HEIGHT)
        self.grid = GameGrid(GRID_HEIGHT, GRID_WIDTH)
        self.init_walls()

    def init_walls(self):
        add_from_image(self.grid, Wall, get_resource_path('map.png'))

    def draw(self):
        self.grid.draw()

    def on_draw(self):
        self.grid.update()
        self.clear()
        self.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose + Pose(0, 1))
        elif symbol == key.A:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose - Pose(1, 0))
        elif symbol == key.S:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose - Pose(0, 1))
        elif symbol == key.D:
            self.grid.elements[1].move_to_position(self.grid.elements[1].pose + Pose(1, 0))
        print(self.grid.elements[1].pose)
