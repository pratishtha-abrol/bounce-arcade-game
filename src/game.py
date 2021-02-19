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
from objects import Paddle, Ball, Brick, BrickArray, ExtraBalls

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
        self.grab = False
        self.held = False
        self.reflect = False
        self.fast = False
        self.exp = False
        self.shrink = False
        self.num = 0

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

            thru_ball_count = 0
            for boost in self.__objects["boost_thru"]:
                if boost.position[1] > config.PADDLE_Y:
                    self.__objects["boost_thru"].remove(boost)
                if boost.applied:
                    # self.screen.draw(boost)
                    if _ct > boost.boost_time:
                        boost.applied = False
                        thru_ball_count -= 1
                        self.__objects["boost_thru"].remove(boost)
                    else:
                        thru_ball_count += 1
            if thru_ball_count > 0:
                self.thru = True
            else:
                self.thru = False  


            paddle_grab_count = 0
            for boost in self.__objects["boost_grab"]:
                if boost.position[1] > config.PADDLE_Y:
                    self.__objects["boost_grab"].remove(boost)
                if boost.applied:
                    # self.screen.draw(boost)
                    if _ct > boost.boost_time:
                        boost.applied = False
                        paddle_grab_count -= 1
                        self.__objects["boost_grab"].remove(boost)
                    else:
                        paddle_grab_count += 1
            if paddle_grab_count > 0:
                self.grab = True
            else:
                self.grab = False  


            fast_ball_count = 0
            for boost in self.__objects["boost_fast"]:
                if boost.position[1] > config.PADDLE_Y:
                    self.__objects["boost_fast"].remove(boost)
                if boost.applied:
                    # self.screen.draw(boost)
                    if _ct > boost.boost_time:
                        boost.applied = False
                        fast_ball_count -= 1
                        self.__objects["boost_fast"].remove(boost)
                    else:
                        fast_ball_count += 1
            if fast_ball_count > 0:
                self.fast = True
            else:
                self.fast = False

            
            expand_paddle_count = 0
            for boost in self.__objects["boost_expand"]:
                if boost.position[1] > config.PADDLE_Y:
                    self.__objects["boost_expand"].remove(boost)
                if boost.applied:
                    # self.screen.draw(boost)
                    if _ct > boost.boost_time:
                        boost.applied = False
                        expand_paddle_count -= 1
                        self.__objects["boost_expand"].remove(boost)
                    else:
                        expand_paddle_count += 1
            if expand_paddle_count > 0:
                self.exp = True
            else:
                self.exp = False

            
            shrink_paddle_count = 0
            for boost in self.__objects["boost_shrink"]:
                if boost.position[1] > config.PADDLE_Y:
                    self.__objects["boost_shrink"].remove(boost)
                if boost.applied:
                    # self.screen.draw(boost)
                    if _ct > boost.boost_time:
                        boost.applied = False
                        shrink_paddle_count -= 1
                        self.__objects["boost_shrink"].remove(boost)
                    else:
                        shrink_paddle_count += 1
            if shrink_paddle_count > 0:
                self.shrink = True
            else:
                self.shrink = False


            ball_multiplier_count = 0
            for boost in self.__objects["boost_multiplier"]:
                if boost.position[1] > config.PADDLE_Y:
                    self.__objects["boost_multiplier"].remove(boost)
                if boost.applied:
                    # self.screen.draw(boost)
                    if _ct > boost.boost_time:
                        boost.applied = False
                        ball_multiplier_count -= 1
                        self.__objects["boost_multiplier"].remove(boost)
                    else:
                        ball_multiplier_count += 1
                        if len(self.__objects["extra_balls"]) <= 5:
                            self.num = 1 + len(self.__objects["extra_balls"])
                            self.__objects["extra_balls"] += ExtraBalls(self.num).get_items()



            if kb.kbhit():
                if self.manage_keys(kb.getch()):
                    print(colorama.Fore.RED + "YOU QUIT || SCORE: ", config.SCORE)
                    break
                kb.clear()
            else:
                kb.clear()

            self.detect_collisions()   
                    
            for boost in self.__objects["boosts"]:
                self.screen.draw(boost)

            for brick in self.__objects["bricks"]:
                self.screen.draw(brick)

            for extraball in self.__objects["extra_balls"]:
                self.screen.draw(extraball)

            self.screen.draw(self.paddle)
            self.screen.draw(self.ball)
            
            self.screen.show()
            self.show_score(_st, _ct)
            if self.reflect:
                self.ball.reflect()
                self.reflect = False
            if not self.held:
                if self.fast:
                    self.ball.update(2)
                else:
                    self.ball.update(1)

            for extraball in self.__objects["extra_balls"]:
                if self.reflect:
                    extraball.reflect()
                if not self.held:
                    if self.fast:
                        extraball.update_extraball(2)
                    else:
                        extraball.update_extraball(1)

            for boost in self.__objects["boosts"]:
                if boost.move:
                    boost.update()

    def manage_keys(self, ch):
        if ch == config.QUIT_CHAR:
            return True

        elif ch == config.RELEASE_CHAR:
            if self.held:
                self.held = False
                self.reflect = True

        else:
            self.paddle.move(ch)
            if self.held:
                self.ball.move(ch)
        return False

    def add_bricks(self):
        self.__objects["bricks"] += BrickArray().get_items()
        for brick in self.__objects["bricks"]:
            if brick.has_boost:
                self.__objects["boosts"].append(brick.boost)
                if (brick.boost.rep == util.str_to_array(graphics.BALL_MULTIPLIER)).all():
                    self.__objects["boost_multiplier"].append(brick.boost)
                elif (brick.boost.rep == util.str_to_array(graphics.SHRINK_PADDLE)).all():
                    self.__objects["boost_shrink"].append(brick.boost)
                elif (brick.boost.rep == util.str_to_array(graphics.EXPAND_PADDLE)).all():
                    self.__objects["boost_expand"].append(brick.boost)
                elif (brick.boost.rep == util.str_to_array(graphics.PADDLE_GRAB)).all():
                    self.__objects["boost_grab"].append(brick.boost)
                elif (brick.boost.rep == util.str_to_array(graphics.FAST_BALL)).all():
                    self.__objects["boost_fast"].append(brick.boost)
                elif (brick.boost.rep == util.str_to_array(graphics.THRU_BALL)).all():
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
                                self.__objects["boosts"].remove(hitter)

                        if pairs[0] == "extra_balls":
                            if hitter.position[1] > config.PADDLE_Y:
                                self.__objects["extra_balls"].remove(hitter)
                    
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
                                    if target.is_explosive:
                                        for brick in self.__objects["bricks"]:
                                            # if brick.position[0] == pos_t[0]:
                                            #     brick.destroy()
                                            #     if brick.strength != 4:
                                            #         config.BRICKS_LEFT -= 1
                                            #     self.__objects["bricks"].remove(brick)
                                            # if brick.position[1] == pos_t[1]:
                                            #     brick.destroy()
                                            #     if brick.strength != 4:
                                            #         config.BRICKS_LEFT -= 1
                                            #     self.__objects["bricks"].remove(brick)
                                            for x in range(max(5, pos_t[0] - 10), min(pos_t[0]+ 20, config.WIDTH-5)):
                                                # x = pos_t[0]
                                                for y in range(pos_t[1]-4, pos_t[1]+4):
                                                    # y = pos_t[1]
                                                    if (brick.position == np.array([x, y])).all():
                                                        brick.destroy()
                                                        if brick.strength != 4:
                                                            config.BRICKS_LEFT -= 1
                                                        self.__objects["bricks"].remove(brick)

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
                                self.__objects["boosts"].remove(hitter)                        
                        
                        if pairs[2]:
                            if not self.thru:
                                if pairs[1] == "bricks":
                                    if pos_h[0] == pos_t[0]+4:
                                        hitter.reflect()
                                    else:
                                        hitter.angle_reflect(pos_h[0] - pos_t[0] - 4)

                            if pairs[1] == "paddle":
                                if not self.grab:
                                    if pos_h[0] == pos_t[0]+4:
                                        hitter.reflect()
                                    else:
                                        hitter.angle_reflect(pos_h[0] - pos_t[0] - 4)
                                else:
                                    pos = pos_h
                                    pos[1] -= 1
                                    hitter.pause(pos_h)
                                    self.held = True

