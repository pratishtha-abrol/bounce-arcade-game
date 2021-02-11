import env
import random
import os
import global_var
from colorama import Fore, Back, Style

def create_header():
    print("Bounceee")

def print_board():
    create_header()
    global_var.mp.render()