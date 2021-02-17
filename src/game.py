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

        self.score = 0
        self.frame_count = 0

        self.__objects = {
            "ball": [self.ball],
            "paddle": [self.paddle],
            "bricks": []
        }

    def clear(self):
        self.screen.clear()
        # sp.call("clear", shell=True)
        print("\033[0;0H")

    def start(self):
        kb = util.KBHit()

        brickarr = self.add_bricks()

        while True:
            self.frame_count += 1
            time.sleep(config.DELAY)
            self.clear()

            self.show_score()

            if kb.kbhit():
                if self.manage_keys(kb.getch()):
                    print(colorama.Fore.RED + "YOU QUIT || SCORE: ", config.SCORE)
                    break
            else:
                kb.clear()

            # brickarr = self.add_bricks()
            for brick in brickarr:
                self.screen.draw(brick)

            self.screen.draw(self.paddle)
            self.screen.draw(self.ball)
            
            self.screen.show()
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
        for x in range(5, config.WIDTH-5, 10):
            if(i==50):
                break
            xf = util.randint(0,1)
            if xf == 1:
                for y in range(13, config.HEIGHT- 20):
                    yf = util.randint(0,1)
                    if yf == 1:
                        brick.append(Brick(np.array([x,y]), util.randint(1, 4)))
                        i += 1

        config.BRICKS_LEFT = i
        return brick

    def show_score(self):
        print(colorama.Back.BLACK + colorama.Style.BRIGHT + "\t|| BOUNCE ||\t\tSCORE: ", self.score, "\tLIVES: ", "❤️  "*config.LIVES)
        print("="*config.WIDTH)

            
