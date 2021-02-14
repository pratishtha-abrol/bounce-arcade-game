import colorama

from game import Game

if __name__ == "__main__":
    colorama.init()

    game = Game()
    game.start()