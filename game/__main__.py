import pyglet
from pyglet.window import mouse
from pyglet.window import key
# from importlib import
import time

from game.pose import Pose
from game.sprite import Sprite

window = pyglet.window.Window()

s = Sprite('../DrinkTheBeer/resources/images/testsprite.png', Pose(10, 10, 0, 10, 10))

@window.event
def on_draw():
    window.clear()
    s.draw()
    # label.draw()



@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        s.pose.y += 1
    elif symbol == key.A:
        s.pose.x -= 1
    elif symbol == key.S:
        s.pose.y -= 1
    elif symbol == key.D:
        s.pose.x += 1
#
#
@window.event
def on_mouse_motion(x, y, dx, dy):
    s.pose.w += ((dx > 0) * 2 - 1)*(abs(dx) > 1)
    s.pose.h += ((dy > 0) * 2 - 1)*(abs(dy) > 1)


event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

pyglet.app.run()

if __name__ == '__main__':
    ...
