import numpy as np
import colorama

import config

class Screen:

    def __init__(self):
        self.width, self.height = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self.clear()

    def clear(self):
        self.display = np.full((self.height, self.width), " ")
        self.bg = np.full((self.height, self.width), config.bg_col)
        self.fg = np.full((self.height, self.width), config.fg_col)

    def draw(self, obj):
        x, y = obj.position
        h, w = obj.shape

        self.display[y:y+h, x:x+w] = obj.rep
        self.fg[y:y+h, x:x+w] = obj.color

    def show(self):
        out = ""

        for i in range(self.height):
            for j in range(self.width):
                out += self.bg[i][j] + self.fg[i][j] + self.display[i][j]
            print(out)
            out = ""

        print(out)