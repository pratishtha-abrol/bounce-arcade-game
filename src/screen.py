import numpy as np
import colorama
import sys

import config
import util

class Screen:

    def __init__(self):
        self.width, self.height = config.SCREEN_WIDTH-1, config.SCREEN_HEIGHT-1
        self.clear()

    def clear(self):
        self.display = np.full((self.height, self.width), " ")
        self.color = util.tup_to_array((self.height, self.width), (config.BG_COL, config.FG_COL))

    def draw(self, obj, frame=0):
        _x, _y = obj.get_position()
        _h, _w = obj.get_shape()
        _x = int(_x)
        _y = int(_y)
        _h = int(_h)
        _w = int(_w)

        disp, color = obj.get_rep(frame)

        disp = disp[:, max(0, -_x):min(config.WIDTH - _x, _w)]
        color = color[:, max(0, -_x):min(config.WIDTH - _x, _w)]

        self.display[_y:_y+_h, max(0, _x):min(_x+_w, config.WIDTH)] = disp
        self.color[_y:_y+_h, max(0, _x):min(_x+_w, config.WIDTH)] = color

    def show(self):
        out = ""

        for i in range(self.height):
            for j in range(self.width):
                out += "".join(self.color[i][j]) + self.display[i][j]
            out += "\n"

        sys.stdout.write(out + colorama.Style.RESET_ALL)