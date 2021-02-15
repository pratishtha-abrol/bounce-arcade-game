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
        sp.call("clear", shell=True)

    def start(self):
        while True:
            time.sleep(config.delay)
            self.clear()
            self.screen.draw(self.slider.get_object())
            self.screen.draw(self.ball.get_object())
            self.screen.draw(self.brick.get_object())
            self.slider.update()
            self.screen.show()
