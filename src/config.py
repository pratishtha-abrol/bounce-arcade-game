"""
configuration parameters
"""

import os
import colorama

SCREEN_HEIGHT, SCREEN_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]
# SCREEN_HEIGHT = 55
# SCREEN_WIDTH = 210
HEIGHT = SCREEN_HEIGHT -1
WIDTH = SCREEN_WIDTH -1

PADDLE_X = WIDTH // 2 - 5
PADDLE_Y = HEIGHT - 6

MIN_HEIGHT = SCOREBOARD_HEIGHT = 3
MAX_HEIGHT = HEIGHT - PADDLE_Y

# delay between frames
DELAY = 0.1

# system colors
BG_COL = colorama.Back.BLACK
FG_COL = colorama.Fore.WHITE

# keyboard control
QUIT_CHAR = "q"
RELEASE_CHAR = " "

# game config
LIVES = 5
SCORE = 0
BRICKS_LEFT = 0
RESET = [False, False]