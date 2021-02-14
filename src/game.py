import time
import colorama
import numpy as np
import subprocess as sp

import config
from slider import Slider
from screen import Screen

class Game:
    
    def __init__(self):
        self.screen = Screen()
        self.slider = Slider()

    def clear(self):
        self.screen.clear()
        sp.call("clear", shell=True)

    def start(self):
        while True:
            time.sleep(config.delay)
            self.clear()
            self.screen.draw(self.slider.get_object())
            self.slider.update()
            self.screen.show()
