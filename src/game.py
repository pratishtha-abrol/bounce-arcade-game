"""
code to run the game
"""

import time
import colorama
import numpy as np
import random
import config
import util

from screen import Screen
from objects import Paddle, Ball, Brick

class Game:
    
    def __init__(self):
        print("\033[?25l\033[2J", end='')
        self.screen = Screen()
        self.paddle = Paddle()
        self.ball = Ball()
        self.brickarr = self.add_bricks()

        self.score = 0
        self.frame_count = 0

        self.__objects = {
            "ball": [self.ball],
            "paddle": [self.paddle],
            "bricks": self.brickarr
        }

        self.__colliders = [
            ("ball", "paddle", True),
            ("ball", "bricks", True)
        ]

    def clear(self):
        self.screen.clear()
        # sp.call("clear", shell=True)
        print("\033[0;0H")

    def start(self):
        kb = util.KBHit()

        while True:
            self.frame_count += 1
            time.sleep(config.DELAY)
            self.clear()

            if kb.kbhit():
                if self.manage_keys(kb.getch()):
                    print(colorama.Fore.RED + "YOU QUIT || SCORE: ", config.SCORE)
                    break
            else:
                kb.clear()

            self.detect_collisions()

            # brickarr = self.add_bricks()
            for brick in self.brickarr:
                self.screen.draw(brick)

            self.screen.draw(self.paddle)
            self.screen.draw(self.ball)
            
            self.screen.show()
            self.show_score()
            self.ball.update()

    def manage_keys(self, ch):
        if ch == config.QUIT_CHAR:
            return True

        # elif ch == config.RELEASE_CHAR:
        #     self.ball.update()

        else:
            self.paddle.move(ch)
        return False

    def add_bricks(self):
        brick =[]
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
                        brick.append(Brick(np.array([x,y]), s))
                        i += 1
                        if s != 4:
                            count += 1

        config.BRICKS_LEFT = count
        return brick

    def show_score(self):
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t|| BOUNCE ||\t\tSCORE: ", self.score, "\tBRICKS LEFT: ", config.BRICKS_LEFT, "\tLIVES: ", "❤️  "*config.LIVES)
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)

    def detect_collisions(self):
        for pairs in self.__colliders:
            for hitter in self.__objects[pairs[0]]:
                for target in self.__objects[pairs[1]]:
                    if(target == "bricks"):
                        i = 0 
                        for brick in self.brickarr:
                            i += 1
                            pos_h = hitter.get_position()
                            pos_b = brick.get_position()

                            height_h, width_h = hitter.get_shape()
                            height_b, width_b = brick.get_shape()

                            minx = min(pos_h[0], pos_b[0])
                            maxx = max(pos_h[0] + width_h, pos_b[0] + width_b)

                            miny = min(pos_h[1], pos_b[1])
                            maxy = max(pos_h[1] + height_h, pos_b[1] + height_b)

                            if maxx - minx >= width_h + width_b \
                                    or maxy - miny >= height_h + height_b:
                                continue

                            self. brickarr = self.destroy_brick(i)

                            if pairs[2]:
                                if pos_h[0] == pos_b[0]+4:
                                    self.ball.reflect()
                                else:
                                    self.ball.angle_reflect(pos_h[0] - pos_b[0] - 4)

                    else:
                        pos_h = hitter.get_position()
                        pos_t = target.get_position()

                        height_h, width_h = hitter.get_shape()
                        height_t, width_t = target.get_shape()

                        minx = min(pos_h[0], pos_t[0])
                        maxx = max(pos_h[0] + width_h, pos_t[0] + width_t)

                        miny = min(pos_h[1], pos_t[1])
                        maxy = max(pos_h[1] + height_h, pos_t[1] + height_t)

                        if maxx - minx >= width_h + width_t \
                                or maxy - miny >= height_h + height_t:
                            continue

                        if pairs[2]:
                            if pos_h[0] == pos_t[0]+4:
                                self.ball.reflect()
                            else:
                                self.ball.angle_reflect(pos_h[0] - pos_t[0] - 4)


    def destroy_brick(self, i):
        return self.brickarr.pop(i-1)