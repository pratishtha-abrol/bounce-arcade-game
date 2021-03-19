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
from objects import Paddle, Ball, Brick, BrickArray, ExtraBalls, UFO
from boosts import Bullet, Bomb

class Game:
    
    def __init__(self):
        print("\033[?25l\033[2J", end='')
        self.screen = Screen()
        self.paddle = Paddle(graphics.PADDLE)
        self.ball = Ball()
        # self.brickarr = self.add_bricks()

        self.is_over = False
        self.frame_count = 0
        self.level = 1

        self.ufo = UFO(self)

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
            "boost_shoot": [],
            "extra_balls": [],
            "bullets": [],
            "bombs": [],
            "ufo": [self.ufo]
        }

        self.__colliders = [
            ("ball", "paddle", True),
            ("ball", "bricks", True),
            ("boosts", "paddle", False),
            ("extra_balls", "paddle", True),
            ("extra_balls", "bricks", True),
            ("bullets", "bricks", False),
            ("bombs", "paddle", False),
            ("ball", "ufo", True)
        ]

        self.thru = False
        self.grab = False
        self.held = False
        self.reflect = False
        self.fast = False
        self.exp = False
        self.shrink = False
        self.shoot = False
        self.num = 0
        self.multiplier_on = False

    def clear(self):
        self.screen.clear()
        # sp.call("clear", shell=True)
        print("\033[0;0H")

    def start(self):
        kb = util.KBHit()
        self.add_bricks()

        _st = time.time()
        ut = _st
        bt = _st

        while True:
            if self.is_over:
                break

            self.frame_count += 1
            time.sleep(config.DELAY)
            self.clear()
            _ct = time.time()

            if _ct > ut+10:
                for brick in self.__objects["bricks"]:
                    brick.update_position()
                    if (brick.position > config.PADDLE_Y-np.array([0,2])).all():
                        config.LIVES=0
                for boost in self.__objects["boosts"]:
                    boost.update_position()

                ut = _ct

            self.paddle.check_update()
            if self.level == 3:
                self.ufo.check_update()
                if _ct > bt + 5:
                    self.__objects["bombs"].append(Bomb(np.array([self.ufo.position[0] + self.ufo.width//2, self.ufo.position[1]])))
                    bt = _ct

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

            shoot_bullet_count = 0
            for boost in self.__objects["boost_shoot"]:
                if boost.position[1] > config.PADDLE_Y:
                    self.__objects["boost_shoot"].remove(boost)
                if boost.applied:
                    if _ct > boost.boost_time:
                        boost.applied = False
                        shoot_bullet_count -= 1
                        self.__objects["boost_shoot"].remove(boost)
                    else:
                        shoot_bullet_count += 1
            if shoot_bullet_count > 0:
                self.shoot = True
            else:
                self.shoot = False

            if self.shoot and self.shrink:
                self.paddle.rep = util.str_to_array(graphics.SHOOTING_SHRUNK_PADDLE)
                self.paddle.color = util.tup_to_array(util.str_to_array(graphics.SHOOTING_SHRUNK_PADDLE).shape, (colorama.Back.YELLOW, colorama.Fore.WHITE))
                self.paddle.height, self.paddle.width = self.paddle.rep.shape
            elif self.shoot and self.exp:
                self.paddle.rep = util.str_to_array(graphics.SHOOTING_EXPANDED_PADDLE)
                self.paddle.color = util.tup_to_array(util.str_to_array(graphics.SHOOTING_EXPANDED_PADDLE).shape, (colorama.Back.YELLOW, colorama.Fore.WHITE))
                self.paddle.height, self.paddle.width = self.paddle.rep.shape
            elif self.shoot:
                self.paddle.rep = util.str_to_array(graphics.SHOOTING_PADDLE)
                self.paddle.color = util.tup_to_array(util.str_to_array(graphics.SHOOTING_PADDLE).shape, (colorama.Back.YELLOW, colorama.Fore.WHITE))
                self.paddle.height, self.paddle.width = self.paddle.rep.shape
            elif self.shrink :
                # self.paddle.change(graphics.SHRINK_PADDLE)
                self.paddle.rep = util.str_to_array(graphics.SHRUNK_PADDLE)
                self.paddle.color = util.tup_to_array(util.str_to_array(graphics.SHRUNK_PADDLE).shape, (colorama.Back.YELLOW, colorama.Fore.WHITE))
                self.paddle.height, self.paddle.width = self.paddle.rep.shape
            elif self.exp :
                # self.paddle.change(graphics.EXPAND_PADDLE)
                self.paddle.rep = util.str_to_array(graphics.EXPANDED_PADDLE)
                self.paddle.color = util.tup_to_array(util.str_to_array(graphics.EXPANDED_PADDLE).shape, (colorama.Back.YELLOW, colorama.Fore.WHITE))
                self.paddle.height, self.paddle.width = self.paddle.rep.shape

            if not self.exp and not self.shrink and not self.shoot:
                self.paddle.rep = util.str_to_array(graphics.PADDLE)
                self.paddle.color = util.tup_to_array(util.str_to_array(graphics.PADDLE).shape, (colorama.Back.YELLOW, colorama.Fore.WHITE))
                self.paddle.height, self.paddle.width = self.paddle.rep.shape


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
                        # self.split = True
                        # if len(self.__objects["extra_balls"]) <= 5:
                            # self.manage_extra_balls()
                            # self.__objects["extra_balls"] += ExtraBalls(self.num).get_items()

            self.num = ball_multiplier_count
            # if self.num > 0:
            #     self.multiplier_on = False
            # self.balls = 2 ** (ball_multiplier_count - 1)
            self.balls = 1 + len(self.__objects["extra_balls"])
            self.check_balls()

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

            for bullet in self.__objects["bullets"]:
                self.screen.draw(bullet)

            for bomb in self.__objects["bombs"]:
                self.screen.draw(bomb)

            self.screen.draw(self.paddle)
            self.screen.draw(self.ball)
            if self.level == 3:
                if self.ufo.health != 0:
                    self.screen.draw(self.ufo)
                else:
                    self.__objects["ufo"].clear()
            
            self.screen.show()
            self.show_score(_st, _ct)
            for boost in self.__objects["boosts"]:
                if boost.move:
                    boost.update()
            if self.reflect:
                self.ball.reflect()
                self.reflect = False
            if not self.held:
                if self.fast:
                    self.ball.update(2)
                else:
                    self.ball.update(1)

            for bullet in self.__objects["bullets"]:
                bullet.update()

            for bomb in self.__objects["bombs"]:
                bomb.update()

            for extraball in self.__objects["extra_balls"]:
                if self.reflect:
                    extraball.reflect()
                if not self.held:
                    if self.fast:
                        extraball.update_extraball(2)
                    else:
                        extraball.update_extraball(1)

    def manage_keys(self, ch):
        if ch == config.QUIT_CHAR:
            return True

        elif ch == config.RELEASE_CHAR:
            if self.held:
                self.held = False
                self.reflect = True

        elif ch == config.SHOOT_CHAR:
            if self.shoot:
                self.shoot_bullet(np.array([self.paddle.position[0]+self.paddle.width//2, self.paddle.position[1]]))

        elif ch == config.PASS_CHAR:
            self.level +=1
            config.LEVEL +=1
            self.__objects["bricks"].clear()
            self.add_bricks()
            self.__objects["boosts"].clear()

        else:
            self.paddle.move(ch)
            if self.level == 3:
                self.ufo.move(ch)
            if self.held:
                self.ball.move(ch)
        return False

    def add_bricks(self):
        self.__objects["bricks"] += BrickArray(self).get_items()
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
                elif (brick.boost.rep == util.str_to_array(graphics.SHOOT_BULLETS)).all():
                    self.__objects["boost_shoot"].append(brick.boost)

    def check_balls(self):
        if self.num>1:
            if not self.multiplier_on:
                # if len(self.__objects["extra_balls"]) < self.num:
                    self.__objects["extra_balls"] += ExtraBalls(self.balls).get_items()  
                    self.multiplier_on = True
        elif self.num == 1:
            if not self.multiplier_on:
                self.__objects["extra_balls"] += ExtraBalls(1).get_items()
                self.multiplier_on = True

    def shoot_bullet(self, position):
        self.__objects["bullets"].append(Bullet(position))

    def show_score(self, st, ct):
        if config.LIVES == 0:
            print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t\tGAME OVER, YOU LOST :(")
            self.is_over = True
        if config.BRICKS_LEFT == 0:
            # print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t\tYOU WON :)")
            self.level += 1
            if self.level == 4:
                print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t\tYOU WON :)")
                self.is_over = True
            self.start()
            # self.is_over = True
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t|| BOUNCE ||\t\tSCORE: ", config.SCORE, "\tBRICKS LEFT: ", config.BRICKS_LEFT, "\tTIME: ", int(ct-st), "\tLIVES: ", "❤️  "*config.LIVES, "\tLEVEL: ", int(self.level))
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "="*config.WIDTH)
        if self.shoot:
            time_left = max(boost.boost_time for boost in self.__objects["boost_shoot"]) - ct
            print(colorama.Back.BLACK + colorama.Style.BRIGHT + "Shooting time available: "+ str(time_left))

        if config.LEVEL == 3:
            print("UFO health: "+ str(self.ufo.health))

    def detect_collisions(self):
        for pairs in self.__colliders:
            for hitter in self.__objects[pairs[0]]:
                for target in self.__objects[pairs[1]]:

                        if pairs[0] == "bombs":
                            if hitter.position[1] > config.PADDLE_Y:
                                for bomb in self.__objects["bombs"]:
                                    if hitter == bomb:
                                        self.__objects["bombs"].remove(hitter)

                        if pairs[0] == "boosts":
                            if hitter.position[1] > config.PADDLE_Y:
                                hitter.destroy()
                                self.__objects["boosts"].remove(hitter)

                        if pairs[0] == "extra_balls":
                            if hitter.position[1] > config.PADDLE_Y:
                                for ball in self.__objects["extra_balls"]:
                                    if hitter == ball:
                                        self.__objects["extra_balls"].remove(hitter)
                    
                        pos_h = hitter.get_position()
                        pos_t = target.get_position()

                        height_h, width_h = hitter.get_shape()
                        height_t, width_t = target.get_shape()

                        minx = min(pos_h[0], pos_t[0])
                        maxx = max(pos_h[0] + width_h, pos_t[0] + width_t)

                        miny = min(pos_h[1], pos_t[1])
                        maxy = max(pos_h[1] + height_h, pos_t[1] + height_t)

                        if maxx - minx > width_h + width_t \
                                or maxy - miny > height_h + height_t:
                            continue

                        if pairs[0] == "bullets":
                            self.__objects["bullets"].remove(hitter)

                        if pairs[0] == "bombs":
                            self.__objects["bombs"].remove(hitter)
                            config.LIVES -+1
                            config.RESET = [True, True, True]

                        if pairs[1] == "ufo":
                            self.ufo.health -=1
                                    
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
                                            for x in range(max(5, pos_t[0] - 10), min(pos_t[0]+ 20, config.WIDTH-5)):
                                                # x = pos_t[0]
                                                for y in range(pos_t[1]-4, pos_t[1]+4):
                                                    # y = pos_t[1]
                                                    if (brick.position == np.array([x, y])).all():
                                                        brick.destroy()
                                                        config.SCORE += 30
                                                        if brick.strength != 4:
                                                            config.SCORE += 10
                                                            config.BRICKS_LEFT -= 1

                                                        if brick.has_boost:
                                                            brick.boost.move = True
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
                                for boost in self.__objects["boost_multiplier"]:
                                    if hitter == boost:
                                        self.multiplier_on = False    
                        
                        if pairs[2]:
                            if not self.thru:
                                if pairs[1] == "bricks":
                                    if pos_h[0] == pos_t[0]+4:
                                        hitter.reflect()
                                    else:
                                        hitter.angle_reflect(pos_h[0] - pos_t[0] - 4)

                            if pairs[1] == "paddle" or pairs[1] == "ufo":
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

