import colorama
import numpy as np
import time

import config
import graphics
import util

class Boost():
    def __init__(self, rep=np.array([[" "]]), position=np.array([0.,0.]), color=np.array([[("","")]]), velocity=np.array([0.,0.]), accelaration=np.array([0.,0.])):
        self.rep = rep
        self.position = position
        self.accelaration = np.array([0,1])
        self.height, self.width = self.rep.shape
        self.color = color
        self.velocity = velocity
        self.active = True
        self.move = False

        self.applied = False
        self.time = 0
        self.boost_time = 0

    def get_position(self):
        return self.position

    def get_shape(self):
        return (self.height, self.width)

    def get_rep(self, frame=0):
        return self.rep, self.color

    def update(self):
        pos  = self.position
        velocity = self.velocity
        velocity += self.accelaration
        self.position += velocity

        if (pos[1] > config.PADDLE_Y):
            self.destroy()

    def destroy(self):
        self.active = False
        self.move = False

    def apply(self):
        pass

    def update_position(self):
        self.position += np.array([0,1])


class FastBall(Boost):
    def __init__(self, position, game):
        # velocity = np.array([0, 1])
        velocity = game.ball.velocity
        rep = util.str_to_array(graphics.FAST_BALL)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)        


class ThruBall(Boost):
    def __init__(self, position, game):
        # velocity = np.array([0, 1])
        velocity = game.ball.velocity
        rep = util.str_to_array(graphics.THRU_BALL)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class BallMultiplier(Boost):
    def __init__(self, position, game):
        # velocity = np.array([0, 1])
        velocity = game.ball.velocity
        rep = util.str_to_array(graphics.BALL_MULTIPLIER)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class ExpandPaddle(Boost):
    def __init__(self, position, game):
        # velocity = np.array([0, 1])
        velocity = game.ball.velocity
        rep = util.str_to_array(graphics.EXPAND_PADDLE)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class ShrinkPaddle(Boost):
    def __init__(self, position, game):
        # velocity = np.array([0, 1])
        velocity = game.ball.velocity
        rep = util.str_to_array(graphics.SHRINK_PADDLE)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class PaddleGrab(Boost):
    def __init__(self, position, game):
        # velocity = np.array([0, 1])
        velocity = game.ball.velocity
        rep = util.str_to_array(graphics.PADDLE_GRAB)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)


class ShootBullet(Boost):
    def __init__(self, position, game):
        # velocity = np.array([0, 1])
        velocity = game.ball.velocity
        rep = util.str_to_array(graphics.SHOOT_BULLETS)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.CYAN))

        super().__init__(rep, position, color, velocity)



class Bullet():
    def __init__(self, position=np.array([0.,0.])):
        self.rep = util.str_to_array(graphics.BULLET)
        self.height, self.width = self.rep.shape
        self.color = util.tup_to_array(self.rep.shape, (colorama.Back.BLACK, colorama.Fore.RED))
        self.position = position
        self.velocity = np.array([0,-1])

    def get_position(self):
        return self.position

    def get_shape(self):
        return (self.height, self.width)

    def get_rep(self, frame=0):
        return self.rep, self.color

    def update(self):
        self.position+=self.velocity

class Bomb():
    def __init__(self, position=np.array([0.,0.])):
        self.rep = util.str_to_array(graphics.BOMB)
        self.height, self.width = self.rep.shape
        self.color = util.tup_to_array(self.rep.shape, (colorama.Back.BLACK, colorama.Fore.RED))
        self.position = position
        self.velocity = np.array([0,1])

    def get_position(self):
        return self.position

    def get_shape(self):
        return (self.height, self.width)

    def get_rep(self, frame=0):
        return self.rep, self.color

    def update(self):
        self.position+=self.velocity