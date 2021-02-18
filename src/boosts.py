import colorama
import numpy as np
import time

import config
import graphics
import util

class Boost():
    def __init__(self, rep=np.array([[" "]]), position=np.array([0.,0.]), color=np.array([[("","")]]), velocity=np.array([0.,0.])):
        self.rep = rep
        self.position = position
        self.height, self.width = self.rep.shape
        self.color = color
        self.velocity = velocity
        self.active = True
        self.move = False
        self.applied = False
        self.time = 0

    def get_position(self):
        return self.position

    def get_shape(self):
        return (self.height, self.width)

    def get_rep(self, frame=0):
        return self.rep, self.color

    def update(self):
        pos  = self.position
        self.position += self.velocity

        if (pos[1] > config.PADDLE_Y):
            self.destroy()

    def destroy(self):
        self.active = False
        self.move = False

    def apply(self):
        pass


class FastBall(Boost):
    def __init__(self, position):
        velocity = np.array([0, 1])
        rep = util.str_to_array(graphics.FAST_BALL)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)        


class ThruBall(Boost):
    def __init__(self, position):
        velocity = np.array([0, 1])
        rep = util.str_to_array(graphics.THRU_BALL)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class BallMultiplier(Boost):
    def __init__(self, position):
        velocity = np.array([0, 1])
        rep = util.str_to_array(graphics.BALL_MULTIPLIER)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class ExpandPaddle(Boost):
    def __init__(self, position):
        velocity = np.array([0, 1])
        rep = util.str_to_array(graphics.EXPAND_PADDLE)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class ShrinkPaddle(Boost):
    def __init__(self, position):
        velocity = np.array([0, 1])
        rep = util.str_to_array(graphics.SHRINK_PADDLE)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class PaddleGrab(Boost):
    def __init__(self, position):
        velocity = np.array([0, 1])
        rep = util.str_to_array(graphics.PADDLE_GRAB)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)
