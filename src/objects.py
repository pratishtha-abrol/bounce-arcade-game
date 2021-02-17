"""
file for all objects in the game
"""

import numpy as np
import colorama

import config
import graphics
import util

class Object:
    def __init__(self, rep=np.array([[" "]]), position=np.array([0,0]), color=np.array([[("","")]])):
        self.rep = rep
        self.position = position
        self.height, self.width = self.rep.shape
        self.color = color

    @staticmethod
    def from_string(rep, position=np.array([0,0]), color=""):
        grid = util.str_to_array(rep)
        color = util.mask(grid, util.tup_to_array(grid.shape, color))

        return Object(grid, position, color)

    def get_position(self):
        return self.position

    def get_shape(self):
        return (self.height, self.width)

    def get_rep(self, frame=0):
        return self.rep, self.color


class BarObject(Object):
    def __init__(self, rep, position, color):
        super().__init__(rep, position, color)


class Paddle(BarObject):
    def __init__(self):
        grid = util.str_to_array(graphics.PADDLE)
        grid_col = util.tup_to_array(grid.shape, (colorama.Back.YELLOW, colorama.Fore.BLACK))
        self.init_pos = np.array([config.PADDLE_X, config.PADDLE_Y], dtype='float64')

        self.controls = ["a", "d"]

        super().__init__(grid, self.init_pos.copy(), grid_col)

    def move(self, key):
        if key in self.controls:
            if key == "a":
                self.position += [-2., 0.]
            elif key == "d":
                self.position += [2., 0.]


class Brick(Object):
    def __init__(self, position, strength):
        self.strength = strength
        if self.strength == 1:
            grid = util.str_to_array(graphics.BRICK)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.MAGENTA, colorama.Fore.BLACK))
        elif self.strength == 2:
            grid = util.str_to_array(graphics.BRICK)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.GREEN, colorama.Fore.BLACK))
        elif self.strength == 3:
            grid = util.str_to_array(graphics.BRICK)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.BLUE, colorama.Fore.BLACK))
        else:
            grid = util.str_to_array(graphics.UNBREAKABLE_BRICK)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.WHITE, colorama.Fore.BLACK))



        super().__init__(grid, position, grid_col)


# class BrickArray():
#     def __init__(self, position, shape):
#         self.position = position
#         self.shape = shape

#         minx, miny = position
#         maxx, maxy = minx + 10*shape[1], miny + shape[0]

#         minx = int(minx)
#         maxx = int(maxx)
#         miny = int(miny)
#         maxy = int(maxy)

#         self.bricks = []

#         for _x in range(minx, maxx, 10):
#             for _y in range(miny, maxy):
#                 self.bricks.append(Brick(np.array((_x, _y), dtype='float64')))

#     def get_items(self):
#         return self.bricks


class CircleObject(Object):
    def __init__(self, rep, position, color, velocity, lives):
        self.velocity = velocity
        self.lives = lives
        super().__init__(rep, position, color)

    def update(self):
        pos = self.position
        if(pos[1] <= 5):
            self.velocity[1] *= -1

        # check sides
        elif(pos[0] <= 0 or pos[0] >= config.WIDTH):
            self.velocity[0] *= -1

        #check if ball lost
        elif(pos[1] > config.PADDLE_Y):
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "GAME LOST")
            exit(0)
            # self.destroy()

        # else:
        self.position += self.velocity

    def reflect(self):
        self.velocity *= -1
        self.position += self.velocity

    def angle_reflect(self, angle):
        self.velocity[0] += angle
        self.velocity[1] *= -1
        self.position += self.velocity


class Ball(CircleObject):
    def __init__(self):
        position = np.array([config.PADDLE_X+4, config.PADDLE_Y-1])
        velocity = np.array([0,-1])
        rep = util.str_to_array(graphics.BALL)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.WHITE))

        super().__init__(rep, position, color, velocity, config.LIVES)
        