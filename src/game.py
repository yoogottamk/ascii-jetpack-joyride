"""
This file contains the code which runs the game
"""

import time
import colorama as col
import numpy as np

from screen import Screen
from player import Mandalorian, Dragon
from objects import Ground
from obstacles import FireBeam

import config
import util
import graphics

class Game:
    def __init__(self):
        self.screen = Screen()
        self.player = Mandalorian()
        self.ground = Ground()

        # draw in this order
        self.background = [self.ground]
        self.obstacles = []
        self.top_level = [self.player]

    def clear(self):
        self.screen.clear()
        util.clear()

    def start(self):
        kb_inp = util.KBHit()

        while True:
            time.sleep(config.delay)
            tmp_obj = []

            if kb_inp.kbhit():
                ch = kb_inp.getch()

                if ch == "q":
                    break
                if ch == "1":
                    self.obstacles.append(FireBeam(np.array([config.WIDTH - 5., config.HEIGHT - 10.])))

                self.player.move(ch)

            self.clear()

            for classes in [self.background, self.obstacles, self.top_level]:
                for obj in classes:
                    if obj.update():
                        self.screen.draw(obj.get_object())
                        tmp_obj.append(obj)

            self.active_objects = tmp_obj

            self.screen.show()

    def __del__(self):
        #util.clear()
        #print(col.Style.RESET_ALL)
        #print(graphics.BYE)
        pass
