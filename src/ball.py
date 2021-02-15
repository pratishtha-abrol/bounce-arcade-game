import numpy as np
import colorama

import config

from objects import Object

BALL = r"""
()
"""

class Circle():

    def __init__(self, rep, position, color):
        self.circle = Object.from_string(rep, position=position, velocity=np.array([0.,-1]), color=color)

    def move(self, key):
        pass

    def update(self):
        # self.circle.update()

        # check if top hit
        if(self.circle.position[1] <= 0):
            self.circle.velocity[1] -= -1

        # check sides
        elif(self.circle.position[0] <= 0 or self.circle.position[0] >= config.WIDTH):
            self.circle.velocity[0] *= -1

        #check if ball lost
        elif(self.circle.position[1] > 48):
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "GAME LOST")
            exit(0)

        # else:
        self.circle.position[1] += self.circle.velocity[1]
        self.circle.position[0] += self.circle.velocity[0]

    def get_object(self):
        return self.circle


class Ball(Circle):

    def __init__(self):
        super().__init__(BALL, position=np.array([104,44]), color=colorama.Style.BRIGHT)
