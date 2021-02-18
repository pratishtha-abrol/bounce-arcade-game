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
from objects import Paddle, Ball, Brick, BrickArray

class Game:
    
    def __init__(self):
        print("\033[?25l\033[2J", end='')
        self.screen = Screen()
        self.paddle = Paddle()
        self.ball = Ball()
        # self.brickarr = self.add_bricks()

        self.is_over = False
        self.frame_count = 0

        self.__objects = {
            "ball": [self.ball],
            "paddle": [self.paddle],
            "bricks": []
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
        self.add_bricks()

        while True:
            self.frame_count += 1
            time.sleep(config.DELAY)
            self.clear()

            if kb.kbhit():
                if self.manage_keys(kb.getch()):
                    print(colorama.Fore.RED + "YOU QUIT || SCORE: ", config.SCORE)
                    break
                kb.clear()
            else:
                kb.clear()

            

            self.detect_collisions()

            if config.BRICKS_LEFT == 0:
                print(colorama.Back.BLACK + colorama.Style.BRIGHT + "YOU WON\tSCORE: ", config.SCORE)

            for brick in self.__objects["bricks"]:
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
        self.__objects["bricks"] += BrickArray().get_items()

    def show_score(self):
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t|| BOUNCE ||\t\tSCORE: ", config.SCORE, "\tBRICKS LEFT: ", config.BRICKS_LEFT, "\tLIVES: ", "❤️  "*config.LIVES)
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)

    def detect_collisions(self):
        for pairs in self.__colliders:
            for hitter in self.__objects[pairs[0]]:
                for target in self.__objects[pairs[1]]:
                    
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

                        if pairs[1] == "bricks":
                            if target.strength != 4:
                                config.SCORE += 30
                                if target.strength == 1:
                                    target.destroy()
                                    config.BRICKS_LEFT -= 1
                                    self.__objects["bricks"].remove(target)
                                else:
                                    target.strength -= 1
                                    target.implement_strength()

                        if pairs[2]:
                            if pos_h[0] == pos_t[0]+4:
                                self.ball.reflect()
                            else:
                                self.ball.angle_reflect(pos_h[0] - pos_t[0] - 4)

