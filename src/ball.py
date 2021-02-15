import numpy as np
import colorama

import config

from objects import Object

BALL = r"""
()
"""

class Circle():

    def __init__(self, rep, position, color):
        self.circle = Object.from_string(rep, position=position, velocity=np.array([0.,0.]), color=color)

    def move(self, key):
        pass

    def update(self):
        self.circle.update()

    def get_object(self):
        return self.circle


class Ball(Circle):

    def __init__(self):
        super().__init__(BALL, position=np.array([104,44]), color=colorama.Style.BRIGHT)
