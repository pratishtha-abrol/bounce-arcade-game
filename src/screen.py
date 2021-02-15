import numpy as np
import colorama
import sys

import config

class Screen:

    def __init__(self):
        self.width, self.height = config.SCREEN_WIDTH-1, config.SCREEN_HEIGHT-1
        self.clear()

    def clear(self):
        self.display = np.full((self.height, self.width), " ")
        self.fg = np.full((self.height, self.width), config.FG_COL)
        self.bg = np.full((self.height, self.width), config.BG_COL)

    def draw(self, obj):
        x, y = obj.position
        h, w = obj.height, obj.width

        self.display[y:y+h, x:x+w] = obj.rep
        self.fg[y:y+h, x:x+w] = obj.color

    def show(self):
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self.bg[i][j] + self.fg[i][j] + self.display[i][j])
            sys.stdout.write("|" + colorama.Back.RESET + "\n")

        sys.stdout.write(colorama.Style.RESET_ALL)