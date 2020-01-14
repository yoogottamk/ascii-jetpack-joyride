"""
This file contains some frequently used functions
"""

import sys
import termios
import atexit
from select import select
import random
import numpy as np

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


class KBHit:
    """
    Class to handle keyboard input
    A modified version of "https://stackoverflow.com/a/22085679"
    """

    def __init__(self):
        """
        Creates a KBHit object that you can call to do various keyboard things.
        """
        # Save the terminal settings
        self._fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self._fd)
        self.old_term = termios.tcgetattr(self._fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self._fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)


    def set_normal_term(self):
        """
        Resets to normal terminal
        """
        termios.tcsetattr(self._fd, termios.TCSAFLUSH, self.old_term)


    @staticmethod
    def getch():
        """
        Returns a keyboard character after kbhit() has been called.
        Should not be called in the same program as getarrow().
        """
        return sys.stdin.read(1)


    @staticmethod
    def kbhit():
        """
        Returns True if keyboard character was hit, False otherwise.
        """
        return select([sys.stdin], [], [], 0)[0] != []

    @staticmethod
    def clear():
        """
        Clears the input buffer
        """
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
