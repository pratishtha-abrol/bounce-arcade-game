import sys
import termios
import atexit
import random
from select import select
import numpy as np

import config

def clear():
    """
    This positions the cursor at (0, 0)
    """
    print("\033[0;0H")


def randint(beg, end):
    """
    This function returns a random integer between beg and end [inclusive]
    Args:
        beg (int) : lower limit of the random number
        end (int) : upper limit of the random number
    Returns:
        int       : A random number in the range [beg, end]
    """
    return random.randint(beg, end)


def str_to_array(rep):
    """
    This function returns a 2D np.array, which contains each character of
    the string rep
    Args:
        rep (string) : The string which has to be converted
    Returns:
        2D np.array  : Space padded array
    """
    arr = rep.split("\n")[1:-1]
    maxlen = len(max(arr, key=len))

    return np.array([list(x + (' ' * (maxlen - len(x)))) for x in arr])


def tup_to_array(shape, tup):
    """
    This function returns a 2D np.array, with the given shape, all elements
    initialized with the tuple tup
    Args:
        shape (nrows, ncols) : Shape of the 2D np.array
        tup (tuple)          : Tuple which is used to initialize the array
    Returns:
        2D np.array          : Array with all elements = tup
    """
    val = np.empty((), dtype=object)
    val[()] = tup

    return np.full(shape, val, dtype=object)


def mask(rep, color):
    """
    Masks the color array, only applying color on nonspace
    Args:
        rep (2D np.array)   : How does the object look
        color (2D np.array) : The color array
    Returns:
        2D np.array : space color set to bg
    """
    max_i, max_j = rep.shape

    for i in range(max_i):
        for j in range(max_j):
            if rep[i][j] == " ":
                color[i][j] = (config.BG_COL, config.FG_COL)

    return color

class KBHit:
    """
    Class to handle keyboard input
    """

    def __init__(self):
        # Save the terminal settings
        self.__fd = sys.stdin.fileno()
        self.__new_term = termios.tcgetattr(self.__fd)
        self.__old_term = termios.tcgetattr(self.__fd)

        # New terminal setting unbuffered
        self.__new_term[3] = (self.__new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.__fd, termios.TCSAFLUSH, self.__new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)


    def set_normal_term(self):
        termios.tcsetattr(self.__fd, termios.TCSAFLUSH, self.__old_term)


    @staticmethod
    def getch():
        # print("Character: ", sys.stdin.read(1))
        return sys.stdin.read(1)


    @staticmethod
    def kbhit():
        return select([sys.stdin], [], [], 0)[0] != []

    @staticmethod
    def clear():
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


