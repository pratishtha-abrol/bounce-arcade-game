"""
configuration parameters
"""

import os
import colorama

# SCREEN_HEIGHT, SCREEN_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]
SCREEN_HEIGHT = 55
SCREEN_WIDTH = 210
HEIGHT = SCREEN_HEIGHT -1
WIDTH = SCREEN_WIDTH -1
SLIDER_LOC = 5

# delay between frames
delay = 0.05

# system colors
BG_COL = colorama.Back.BLACK
FG_COL = colorama.Fore.WHITE


QUIT_CHAR = "q"

LIVES = 5
SCORE = 0