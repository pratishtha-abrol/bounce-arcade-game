import colorama

from objects import Object

SLIDER = r"""
=====
"""

class Bar:

    def __init__(self, rep, position, color):
        self.bar = Object.from_string(rep, position=position, velocity=0, gravity=1, color=color)

    def move(self, direction=0):
        pass

    def update(self):
        self.bar.update()

    def get_object(self):
        return self.bar


class Slider(Bar):
    def __init__(self):
        super().__init__(SLIDER, [30,10], colorama.Fore.YELLOW)
