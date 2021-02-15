import colorama
import numpy as np

from objects import Object

SLIDER = r"""
          
"""

class Bar:

    def __init__(self, rep, position, color):
        self.bar = Object.from_string(rep, position=position, velocity=np.array([0.,0.]), color=color)

    def move(self, key):
        pass

    def update(self):
        self.bar.update()

    def get_object(self):
        return self.bar


class Slider(Bar):

    def __init__(self):
        super().__init__(SLIDER, position=np.array([100,45]), color=colorama.Back.YELLOW)
        self.controls = ["a", "d"]

    def move(self, key):
        key = key.lower()

        if key in self.controls:
            if key == "a":
                self.bar.velocity[0] -= 1
            elif key == "d":
                self.bar.velocity[0] += 1

class Brick(Bar):

    def __init__(self):
        super().__init__(SLIDER, position=np.array([100, 30]), color=colorama.Back.RED)