"""
This file contains the code which runs the game
"""

import time
import colorama as col
import numpy as np

from screen import Screen
from player import Mandalorian, Dragon
from objects import Ground

import config
import util
import graphics

class Game:
    def __init__(self):
        self.screen = Screen()
        self.player = Mandalorian()
        self.ground = Ground()
        self.active_objects = [self.ground, self.player]

    def clear(self):
        self.screen.clear()
        util.clear()

    def start(self):
        kb_inp = util.KBHit()

        while True:
            time.sleep(config.delay)

            if kb_inp.kbhit():
                ch = kb_inp.getch()
                if ch == "q":
                    break
                self.player.move(ch)

            self.clear()

            for obj in self.active_objects:
                obj.update()
                self.screen.draw(obj.get_object())

            self.screen.show()

    def __del__(self):
        util.clear()
        print(col.Style.RESET_ALL)
        print(graphics.BYE)
