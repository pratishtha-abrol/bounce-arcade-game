import os
import colorama

SCREEN_HEIGHT, SCREEN_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]

# delay between frames
delay = 0.1

# system colors
bg_col = colorama.Back.BLACK
fg_col = colorama.Fore.WHITE