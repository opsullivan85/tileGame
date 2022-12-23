from math import floor

from pyglet import window, clock
from pyglet.window import key

from game.callbackHandler import CallbackHandler
from game.constants import WINDOW_PIXEL_WIDTH, WINDOW_PIXEL_HEIGHT, GRID_HEIGHT, GRID_WIDTH
from game.gameGrid import GameGrid
from game.gridObject import add_from_image
from game.player import Player
from game.pose import Pose
from game.resources import get_resource_path
from game.spike import Spike
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
        self.prev_frame_time = floor(time())
        self.fps = 0

        self.grid.add(Spike(pose=Pose(3, 3), damage=10))

        self.callbackHandler = CallbackHandler()
        self.callbackHandler.add_callback(self.player.is_dead, self.on_player_death, one_time=True)

        self.set_update_interval()

    def init_walls(self):
        add_from_image(self.grid, Wall, get_resource_path('map.png'))

    def print_fps(self):
        if floor(time()) - self.prev_frame_time:  # if a second has passed
            self.prev_frame_time = floor(time())
            print(self.fps)
            self.fps = 0
        else:
            self.fps += 1

    def draw(self):
        self.print_fps()
        self.grid.draw()

    def on_draw(self):
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
        self.set_update_interval()

    def on_player_death(self):
        self.close()
        print('Player died')

    def set_update_interval(self, interval: float = 0.5):
        """ Sets the update interval. Updates immediately on call.

        :param interval: time between updates in seconds
        """
        clock.unschedule(self.update)
        # self.update needs to be called here so the game updates on player movement
        self.update(1)  # figure out how to pass in a sensible interval
        clock.schedule_interval_soft(self.update, interval)

    def update(self, dt: float):
        """ Update the game state.

        :param dt: time since last update, not currently used
        """
        print(dt)
        # for obj in self.grid.elements:
        #     obj.pose.theta += 10
        self.grid.update()
        self.callbackHandler.check_callbacks()
