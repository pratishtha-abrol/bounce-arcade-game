"""
file for all objects in the game
"""

import numpy as np
import colorama

import config
import graphics
import util
import boosts

class Object:
    def __init__(self, rep=np.array([[" "]]), position=np.array([0.,0.]), color=np.array([[("","")]])):
        self.rep = rep
        self.position = position
        self.height, self.width = self.rep.shape
        self.color = color

    @staticmethod
    def from_string(rep, position=np.array([0.,0.]), color=""):
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

    def check_update(self):
        if config.RESET[0]:
            self.position = np.array([config.PADDLE_X, config.PADDLE_Y], dtype='float64')
            config.RESET[0] = False

    def move(self, key):
        if key in self.controls:
            if key == "a":
                if self.position[0] > 3:
                    self.position += [-4., 0.]
            elif key == "d":
                if self.position[0] < config.WIDTH - 10:
                    self.position += [4., 0.]

    def expand_paddle(self):
        self.rep = util.str_to_array(graphics.BIG_PADDLE)

    def shrink_paddle(self):
        self.rep = util.str_to_array(graphics.SMALL_PADDLE)

    def paddle_normal(self):
        self.rep = util.str_to_array(graphics.PADDLE)


class Brick(Object):
    def __init__(self, position, strength):
        self.strength = strength
        self.active = True
        self.has_boost = False
        self.is_explosive = False
        # flag = util.randint(1,20)
        flag =1
        if flag == 1:
            self.has_boost = True
            self.boost = boosts.FastBall(np.array([position[0]+3, position[1]]))
        elif flag == 2:
            self.has_boost = True
            self.boost = boosts.ThruBall(np.array([position[0]+3, position[1]]))
        elif flag == 3:
            self.has_boost = True
            self.boost = boosts.BallMultiplier(np.array([position[0]+3, position[1]]))
        elif flag == 4:
            self.has_boost = True
            self.boost = boosts.ExpandPaddle(np.array([position[0]+3, position[1]]))
        elif flag == 5:
            self.has_boost = True
            self.boost = boosts.ShrinkPaddle(np.array([position[0]+3, position[1]]))
        elif flag == 6:
            self.has_boost = True
            self.boost = boosts.PaddleGrab(np.array([position[0]+3, position[1]]))
        elif flag == 14:
            self.is_explosive = True


        if self.strength == 1:
            grid = util.str_to_array(graphics.BRICK_1)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.MAGENTA, colorama.Fore.BLACK))
        elif self.strength == 2:
            grid = util.str_to_array(graphics.BRICK_2)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.GREEN, colorama.Fore.BLACK))
        elif self.strength == 3:
            grid = util.str_to_array(graphics.BRICK_3)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.BLUE, colorama.Fore.BLACK))
        else:
            grid = util.str_to_array(graphics.UNBREAKABLE_BRICK)
            grid_col = util.tup_to_array(grid.shape, (colorama.Back.WHITE, colorama.Fore.BLACK))

        super().__init__(grid, position, grid_col)

    def destroy(self):
        self.active = False

    def implement_strength(self):
        if self.strength == 1:
            self.color = util.tup_to_array(self.rep.shape, (colorama.Back.MAGENTA, colorama.Fore.BLACK))
        if self.strength == 2:
            self.color = util.tup_to_array(self.rep.shape, (colorama.Back.GREEN, colorama.Fore.BLACK))

class BrickArray():
    def __init__(self):
        self.bricks = []

        i=0
        count = 0
        for x in range(max(5, config.WIDTH//2 - 60), min(config.WIDTH//2 + 60, config.WIDTH - 5), 10):
            xf = util.randint(0,1)
            if xf == 1:
                for y in range(13, config.HEIGHT- 20):
                    if i==50:
                        break
                    yf = util.randint(0,1)
                    if yf == 1:
                        s = util.randint(1, 4)
                        self.bricks.append(Brick(np.array([x,y]), s))
                        i += 1
                        if s != 4:
                            count += 1

        config.BRICKS_LEFT = count

    def get_items(self):
        return self.bricks


class CircleObject(Object):
    def __init__(self, rep, position, color, velocity, lives):
        self.velocity = velocity
        self.lives = lives 

        self.controls = ["a", "d"]
        super().__init__(rep, position, color)

    def update(self, x):
        pos = self.position
        # check top
        if(pos[1] <= 5):
            self.velocity[1] *= -1

        # check sides
        elif(pos[0] <= 3 or pos[0] >= config.WIDTH-1):
            self.velocity[0] *= -1

        #check if ball lost
        elif(pos[1] > config.PADDLE_Y):
            # print(colorama.Fore.RED + colorama.Style.BRIGHT + "GAME LOST")
            # exit(0)
            # self.destroy()
            config.LIVES -= 1
            if config.LIVES != 0:
                config.RESET[0] = True
                config.RESET[1] = True

        # else:
        self.position[0] += self.velocity[0]
        self.position[1] += x * self.velocity[1]

        if config.RESET[1] == True:
            self.position = np.array([config.PADDLE_X+4, config.PADDLE_Y-1])
            self.velocity = np.array([0,-1])
            config.RESET[1] = False

    def reflect(self):
        self.velocity[1] *= -1
        self.position += self.velocity

    def angle_reflect(self, angle):
        self.velocity[0] += round(angle / 4, 0)
        self.velocity[1] *= -1
        self.position += self.velocity

    def pause(self):
        pos = self.position
        self.position[0] = pos[0]
        self.position[1] = pos[1] -1

    def move(self,key):
        if key in self.controls:
            if key == "a":
                self.position += [-4, 0]
            elif key == "d":
                self.position += [4, 0]


class Ball(CircleObject):
    def __init__(self):
        position = np.array([config.PADDLE_X+4, config.PADDLE_Y-1])
        velocity = np.array([0,-1])
        rep = util.str_to_array(graphics.BALL)
        color = util.tup_to_array(rep.shape, (colorama.Back.BLACK, colorama.Fore.WHITE))

        super().__init__(rep, position, color, velocity, config.LIVES)
