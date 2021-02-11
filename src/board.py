import env
import math, random
import numpy as np
from colorama import init, Fore, Back, Style

class Map () :

    height = int(env.row)
    width = int(env.col)

    def __init__(self):
        self.start_index = 0
        self.matrix = np.array([[" " for i in range(self.width)] for j in range(self.height)])
        self.create_sky()
        self.create_ground()

    def render(self):
        for y in range(3, self.height):
            pr = []
            for x in range(self.start_index, self.start_index + env.col):
                pr.append(self.matrix[y][x] + Style.RESET_ALL)
            print(''.join(pr))

    def create_ground(self):
        y = self.height - 1
        for x in range(self.width):
            self.matrix[y][x] = "T"


    def create_sky(self): 
        for x in range(self.width):
            self.matrix[3][x] = "-"

