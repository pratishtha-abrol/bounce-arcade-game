"""
code to run the game
"""

import time
import colorama
import numpy as np
import random
import config
import util
import graphics

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
            "bricks": [],
            "boosts": [],
            "boost_multiplier": [],
            "boost_shrink": [],
            "boost_expand": [],
            "boost_grab": [],
            "boost_fast": [],
            "boost_thru": [],
            "extra_balls": []
        }

        self.__colliders = [
            ("ball", "paddle", True),
            ("ball", "bricks", True),
            ("boosts", "paddle", False),
            ("extra_balls", "paddle", True),
            ("extra_balls", "bricks", True)
        ]

        self.thru = False

    def clear(self):
        self.screen.clear()
        # sp.call("clear", shell=True)
        print("\033[0;0H")

    def start(self):
        kb = util.KBHit()
        self.add_bricks()

        _st = time.time()

        while True:
            if self.is_over:
                break

            self.frame_count += 1
            time.sleep(config.DELAY)
            self.clear()
            _ct = time.time()

            self.paddle.check_update()

            if kb.kbhit():
                if self.manage_keys(kb.getch()):
                    print(colorama.Fore.RED + "YOU QUIT || SCORE: ", config.SCORE)
                    break
                kb.clear()
            else:
                kb.clear()

            self.detect_collisions()
                    
            for boost in self.__objects["boosts"]:
                if boost.active == True:
                    self.screen.draw(boost)

            for brick in self.__objects["bricks"]:
                self.screen.draw(brick)

            self.screen.draw(self.paddle)
            self.screen.draw(self.ball)
            
            self.screen.show()
            self.show_score(_st, _ct)
            self.ball.update()
            for boost in self.__objects["boosts"]:
                if boost.move:
                    boost.update()

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
        for brick in self.__objects["bricks"]:
            if brick.has_boost:
                self.__objects["boosts"].append(brick.boost)
                if (brick.boost.rep == graphics.BALL_MULTIPLIER).all():
                    self.__objects["boost_multiplier"].append(brick.boost)
                elif (brick.boost.rep == graphics.SHRINK_PADDLE).all():
                    self.__objects["boost_shrink"].append(brick.boost)
                elif (brick.boost.rep == graphics.EXPAND_PADDLE).all():
                    self.__objects["boost_expand"].append(brick.boost)
                elif (brick.boost.rep == graphics.PADDLE_GRAB).all():
                    self.__objects["boost_grab"].append(brick.boost)
                elif (brick.boost.rep == graphics.FAST_BALL).all():
                    self.__objects["boost_fast"].append(brick.boost)
                elif (brick.boost.rep == graphics.THRU_BALL).all():
                    self.__objects["boost_thru"].append(brick.boost)

    def show_score(self, st, ct):
        if config.LIVES == 0:
            print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t\tNO LIVES LEFT :(")
            self.is_over = True
        if config.BRICKS_LEFT == 0:
            print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t\tYOU WON :)")
            self.is_over = True
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t|| BOUNCE ||\t\tSCORE: ", config.SCORE, "\tBRICKS LEFT: ", config.BRICKS_LEFT, "\tTIME: ", int(ct-st), "\tLIVES: ", "❤️  "*config.LIVES)
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)

    def detect_collisions(self):
        for pairs in self.__colliders:
            for hitter in self.__objects[pairs[0]]:
                for target in self.__objects[pairs[1]]:

                        if pairs[0] == "boosts":
                            if hitter.position[1] > config.PADDLE_Y:
                                hitter.destroy()
                                if not hitter.applied:
                                    self.__objects["boosts"].remove(hitter)
                    
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
                                    if target.has_boost:
                                        target.boost.move = True
                                    config.BRICKS_LEFT -= 1
                                    self.__objects["bricks"].remove(target)
                                else:
                                    target.strength -= 1
                                    target.implement_strength()

                        if pairs[0] == "boosts":
                            if hitter.active:
                                hitter.applied = True
                                config.SCORE += 10
                                hitter.time = time.time()
                                hitter.boost_time = time.time()+10
                                hitter.destroy()
                            # self.__objects["boosts"].remove(hitter)                        
                        
                        if pairs[2]:
                            if pairs[1] == "bricks":
                                if pos_h[0] == pos_t[0]+4:
                                    hitter.reflect()
                                else:
                                    hitter.angle_reflect(pos_h[0] - pos_t[0] - 4)

                            if pairs[1] == "paddle":
                                if pos_h[0] == pos_t[0]+4:
                                    hitter.reflect()
                                else:
                                    hitter.angle_reflect(pos_h[0] - pos_t[0] - 4)

