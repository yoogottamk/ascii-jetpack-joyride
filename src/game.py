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
from coins import Coins

import config
import util
import graphics

class Game:
    def __init__(self):
        self.screen = Screen()
        self.player = Mandalorian()
        self.ground = Ground()

        # draw in this order
        self.objects = {
            "background": [self.ground],
            "obstacles": [],
            "top_level": [self.player],
            "coins": []
        }

    def clear(self):
        self.screen.clear()
        util.clear()

    def start(self):
        kb_inp = util.KBHit()

        while True:
            time.sleep(config.DELAY)
            tmp_obj = {
                "background": [],
                "obstacles": [],
                "top_level": [],
                "coins": []
            }

            if kb_inp.kbhit():
                ch = kb_inp.getch()
                #kb_inp.clear()

                if ch == "q":
                    break
                if ch == "1":
                    self.objects["obstacles"].append(FireBeam(np.array([config.WIDTH, util.randint(0, config.MAX_HEIGHT - 6)], dtype='float64')))
                elif ch == "2":
                    self.objects["coins"].append(Coins(np.array([config.WIDTH, util.randint(0, config.MAX_HEIGHT - 4)], dtype='float64'), np.array([3, util.randint(3, 10)])))

                self.player.move(ch)

            self.clear()

            for obj_type in self.objects:
                for obj in self.objects[obj_type]:
                    if obj.update():
                        self.screen.draw(obj.get_object())
                        tmp_obj[obj_type].append(obj)

            self.objects = tmp_obj

            self.screen.show()

    def __del__(self):
        #util.clear()
        #print(col.Style.RESET_ALL)
        #print(graphics.BYE)
        pass
