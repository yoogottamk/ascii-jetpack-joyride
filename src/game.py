"""
This file contains the code which runs the game
"""

import time
import colorama as col
import numpy as np
import subprocess as sp

from screen import Screen
from player import Mandalorian
import config

class Game:
    def __init__(self):
        self.screen = Screen()
        self.mando = Mandalorian()

    def clear(self):
        self.screen.clear()
        sp.call("clear", shell=True)

    def start(self):
        while True:
            time.sleep(config.delay)
            self.clear()
            self.screen.draw(self.mando.get_object())
            self.mando.update()
            self.screen.show()
