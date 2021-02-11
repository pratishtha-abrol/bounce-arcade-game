import env
import random
import os
import global_var
from colorama import Fore, Back, Style

def create_header():
    print("||  BOUNCE  ||    LIVES:    %s    |    BRICKS LEFT:    %s    |    SCORE:    %s" % (env.lives, global_var.BRICKS, global_var.SCORE))

def print_board():
    create_header()
    global_var.mp.render()