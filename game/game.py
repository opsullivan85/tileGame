from collections import deque
from math import floor
from time import time

from pyglet import window, clock
from pyglet.window import key

from game.callbackHandler import CallbackHandler
from game.camera import Camera
from game.constants import WINDOW_PIXEL_WIDTH, WINDOW_PIXEL_HEIGHT, GRID_HEIGHT, GRID_WIDTH
from game.drone import Drone
from game.gameGrid import GameGrid
from game.gridObject import add_from_image
from game.healingPad import HealingPad
from game.player import Player
from game.pose import Pose
from game.resources import get_resource_path
from game.spike import Spike
from game.wall import Wall


class Game(window.Window):
    """ Main game class.
    """

    def __init__(self):
        super().__init__(width=WINDOW_PIXEL_WIDTH, height=WINDOW_PIXEL_HEIGHT)
        self.grid = GameGrid(GRID_HEIGHT, GRID_WIDTH)

        self.init_walls()

        self.grid.add(Spike(damage=10, pose=Pose(3, 3)))
        self.grid.add(HealingPad(healing=10, pose=Pose(3, 7)))

        self.player = Player(Pose(1, 1))
        self.grid.add(self.player)
        self.grid.add(Player(Pose(2, 2)))
        self.grid.add(Player(Pose(1, 5, 0)))
        self.grid.add(Player(Pose(1, 5, 45)))

        path = deque([
            Pose(1, 7),
            Pose(2, 7),
            Pose(3, 7),
            Pose(2, 7),
        ])
        self.grid.add(Player(Pose(1, 7, 45)))
        self.grid.add(Drone(Pose(1, 7), path=path))

        self.player_camera = Camera(self.player.pose)
        self.player_camera.set_tracking(self.player.pose)

        self.prev_frame_time = time()
        self.prev_update_time = time()
        self.fps = 0

        self.callbackHandler = CallbackHandler()
        self.callbackHandler.add_callback(self.player.is_dead, self.on_player_death, one_time=True)

        self.clock = clock.get_default()

        self.set_update_interval()

    def init_walls(self):
        add_from_image(self.grid, Wall, get_resource_path('map.png'), random_rotation=True)

    def draw(self, camera: Camera, dt: float):
        self.grid.draw(camera, dt)

    # @override_dt_kwarg
    def on_draw(self, dt: float = None):
        if dt is None:
            dt = time() - self.prev_frame_time

        # try:
        #     print(1 / dt)
        # except ZeroDivisionError:
        #     ...
        self.prev_frame_time = time()
        self.clear()
        self.player_camera.update(dt)
        self.draw(self.player_camera, dt)

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
        elif symbol == key.SPACE:
            [print() for _ in range(5)]
            print(self.grid)
        elif symbol == key.ESCAPE:
            self.close()
        self.set_update_interval()

    def on_player_death(self):
        self.close()

    def set_update_interval(self, interval: float = 0.5):
        """ Sets the update interval. Updates immediately on call.

        :param interval: time between updates in seconds
        """
        self.clock.unschedule(self.update)
        # self.update needs to be called here so the game updates on player movement
        self.update()  # figure out how to pass in a sensible interval
        self.clock.schedule_interval_soft(self.update, interval)

    def update(self, dt: float = None):
        """ Update the game state.

        :param dt: time since last update, not currently used
        """
        if dt is None:
            dt = time() - self.prev_update_time
        self.prev_update_time = time()
        # run game updates
        self.grid.update(dt)
        # check callbacks
        self.callbackHandler.check_callbacks()
        # draw everything
        self.on_draw()
        # reset pose update information
        for element in self.grid.elements:
            element.pose.reset_updates()
