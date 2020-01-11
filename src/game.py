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
        self.mando = Mandalorian()

    def clear(self):
        self.screen.clear()
        util.clear()

    def start(self):
        kb_inp = util.KBHit()

        while True:
            time.sleep(config.delay)

            if kb_inp.kbhit():
                ch = kb_inp.getch()
                self.mando.move(ch)

            self.clear()
            self.screen.draw(self.mando.get_object())
            self.mando.update()
            self.screen.show()
