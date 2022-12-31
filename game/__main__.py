import pyglet

from game.constants import WINDOW_PIXEL_WIDTH, WINDOW_PIXEL_HEIGHT



def main():
    window = pyglet.window.Window(width=WINDOW_PIXEL_WIDTH, height=WINDOW_PIXEL_HEIGHT)
    from game.game import Game
    game = Game(window)
    pyglet.app.run()


if __name__ == '__main__':
    main()
