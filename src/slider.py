import colorama
import numpy as np

import config

from objects import Object
from util import KBHit

SLIDER = r"""
          
"""

kb = KBHit()

class Bar:

    def __init__(self, rep, position, velocity, color):
        self.bar = Object.from_string(rep, position=position, velocity=np.array([0.,0.]), color=color)

    def move(self, key):
        pass

    def update(self):
        self.bar.update()

    def get_object(self):
        return self.bar


class Slider(Bar):

    def __init__(self):
        super().__init__(SLIDER, position=np.array([100,45]), velocity=np.array([0.,0.]), color=colorama.Back.YELLOW)
        self.controls = ["a", "d"]

    def move(self, key):
        key = kb.getinput()

        if key in self.controls:
            if key == "a":
                self.bar.position[0] -= 2
            elif key == "d":
                self.bar.position[0] += 2


class Brick(Bar):

    def __init__(self):
        super().__init__(SLIDER, position=np.array([100, 30]), velocity=np.array([0.,0.]), color=colorama.Back.RED)