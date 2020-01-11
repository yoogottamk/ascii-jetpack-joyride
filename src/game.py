"""
This file contains the code which runs the game
"""

import time
import colorama as col
import numpy as np
import subprocess as sp

from screen import Screen
from player import Mandalorian, Dragon
import config
import util

class Game:
    def __init__(self):
        self.screen = Screen()

    def clear(self):
        self.screen.clear()
        util.clear()

    def start(self):
        while True:
            time.sleep(config.delay)
            self.clear()
            self.screen.show()
