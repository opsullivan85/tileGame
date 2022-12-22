from pyglet import window
from pyglet.window import key

from game.constants import WINDOW_PIXEL_WIDTH, WINDOW_PIXEL_HEIGHT, GRID_HEIGHT, GRID_WIDTH
from game.gameGrid import GameGrid
from game.gridObject import add_from_image
from game.player import Player
from game.pose import Pose
from game.resources import get_resource_path
from game.wall import Wall

from time import time

class Game(window.Window):
    """ Main game class.
    """

    def __init__(self):
        super().__init__(width=WINDOW_PIXEL_WIDTH, height=WINDOW_PIXEL_HEIGHT)
        self.grid = GameGrid(GRID_HEIGHT, GRID_WIDTH)
        self.init_walls()

        self.player = Player(Pose(1, 1))
        self.grid.add(self.player)
        self.grid.add(Player(Pose(2, 2)))
        self.grid.add(Player(Pose(3, 3)))
        self.grid.add(Player(Pose(3, 3, 90)))
        self.prev_time = time()

    def init_walls(self):
        add_from_image(self.grid, Wall, get_resource_path('map.png'))

    def draw(self):
        print(time() - self.prev_time)
        self.prev_time = time()
        for obj in self.grid.elements:
            obj.pose.theta += 1
        self.grid.draw()

    def on_draw(self):
        self.grid.update()
        self.clear()
        self.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            self.player.move_to_position(self.player.pose + Pose(0, 1))
            self.player.pose.theta = 0
        elif symbol == key.A:
            self.player.move_to_position(self.player.pose - Pose(1, 0))
            self.player.pose.theta = -90
        elif symbol == key.S:
            self.player.move_to_position(self.player.pose - Pose(0, 1))
            self.player.pose.theta = 180
        elif symbol == key.D:
            self.player.move_to_position(self.player.pose + Pose(1, 0))
            self.player.pose.theta = 90
        elif symbol == key.UP:
            self.player.pose.h += 0.5
        elif symbol == key.DOWN:
            self.player.pose.h -= 0.5
        elif symbol == key.LEFT:
            self.player.pose.w -= 0.5
        elif symbol == key.RIGHT:
            self.player.pose.w += 0.5
        elif symbol == key.BRACKETLEFT:
            self.player.health -= 5
        elif symbol == key.BRACKETRIGHT:
            self.player.health += 5
        # print(self.player.pose)
