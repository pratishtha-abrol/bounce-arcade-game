"""
code to run the game
"""

import time
import colorama
import numpy as np
import subprocess as sp

import config
import util

from slider import Slider, Brick
from screen import Screen
from ball import Ball

class Game:
    
    def __init__(self):
        print("\033[?25l\033[2J", end='')
        self.screen = Screen()
        self.slider = Slider()
        self.ball = Ball()
        self.brick = Brick()

    def clear(self):
        self.screen.clear()
        # sp.call("clear", shell=True)
        print("\033[0;0H")

    def start(self):
        kb = util.KBHit()

        while True:
            time.sleep(config.delay)
            self.clear()

            if kb.kbhit():
                if self.manage_keys(kb.getch()):
                    break
            else:
                kb.clear()

            self.screen.draw(self.slider.get_object())
            self.screen.draw(self.ball.get_object())
            self.screen.draw(self.brick.get_object())
            self.slider.update()
            self.ball.update()
            self.screen.show()

    def manage_keys(self, ch):
        if ch == config.QUIT_CHAR:
            return True

        else:
            self.slider.move(ch)
        return False
