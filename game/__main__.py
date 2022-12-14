import pyglet
from pyglet.window import mouse
from pyglet.window import key

from game.Constants import *
from game.game import Game
from game.gameGrid import GameGrid
from game.pose import Pose
from game.wall import Wall

# window = pyglet.window.Window(width=WINDOW_PIXEL_WIDTH, height=WINDOW_PIXEL_HEIGHT)

game = Game()

# @window.event
# def on_draw():
#     window.clear()
#     game.draw()


# @window.event
# def on_key_press(symbol, modifiers):
#     if symbol == key.W:
#         s.pose.y += 10
#     elif symbol == key.A:
#         s.pose.x -= 10
#     elif symbol == key.S:
#         s.pose.y -= 10
#     elif symbol == key.D:
#         s.pose.x += 10


# @window.event
# def on_mouse_motion(x, y, dx, dy):
#     s.pose.w += ((dx > 0) * 2 - 1) * (abs(dx) > 1)
#     s.pose.h += ((dy > 0) * 2 - 1) * (abs(dy) > 1)


# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == mouse.LEFT:
#         grid.elements[0].move_to_position(Pose(grid.elements[0].pose.x + 1, grid.elements[0].pose.y+1))
#     else:
#         grid.elements[1].pose.theta += 5
#         print(grid.elements[1].pose.theta)


event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)


if __name__ == '__main__':
    pyglet.app.run()
