import os
import sys
import termios
import atexit
from select import select

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


