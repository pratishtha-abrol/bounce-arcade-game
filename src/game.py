"""
code to run the game
"""

import time
import colorama
import numpy as np
import random
import config
import util

from screen import Screen
from objects import Paddle, Ball

class Game:
    
    def __init__(self):
        print("\033[?25l\033[2J", end='')
        self.screen = Screen()
        self.paddle = Paddle()
        self.ball = Ball()

        self.__objects = {
            "ball": [self.ball],
            "paddle": [self.paddle],
            "bricks": []
        }

    def clear(self):
        self.screen.clear()
        # sp.call("clear", shell=True)
        print("\033[0;0H")

    def start(self):
        kb = util.KBHit()

        while True:
            time.sleep(config.DELAY)
            self.clear()

            if kb.kbhit():
                if self.manage_keys(kb.getch()):
                    print(colorama.Fore.RED + "YOU QUIT || SCORE: ", config.SCORE)
                    break
            else:
                kb.clear()


            self.screen.draw(self.paddle)
            self.screen.draw(self.ball)
            self.screen.show()
            self.ball.update()

    def manage_keys(self, ch):
        if ch == config.QUIT_CHAR:
            return True

        # elif ch == config.RELEASE_CHAR:
        #     self.ball.update()

        else:
            self.paddle.move(ch)
        return False
