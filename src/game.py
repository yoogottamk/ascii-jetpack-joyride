"""
This file contains the code which runs the game
"""

import time
import numpy as np

from screen import Screen
from player import Mandalorian#, Dragon
from objects import Ground
from obstacles import FireBeam
from coins import Coins
from bullets import MandalorianBullet

import config
import util

class Game:
    """
    This class manages the whole Game
    """

    def __init__(self):
        """
        Constructor for the Game
        """

        # hide the cursor
        print("\033[?25l", end='')

        self.screen = Screen()
        self.player = Mandalorian()
        self.ground = Ground()
        self.score = 0
        self.lives = config.INIT_LIVES
        self.init_time = time.time()

        # seperate them into different classes
        self.objects = {
            "background": [self.ground],
            "obstacles": [],
            "player": [self.player],
            "player_bullet": [],
            "coins": []
        }

        # convention is x -> target
        self.colliders = [
            ("obstacles", "player"),
            ("player", "coins"),
            ("player_bullet", "obstacles")
        ]

    def clear(self):
        """
        Clears the screen and the frame
        """
        self.screen.clear()
        util.clear()

    def start(self):
        """
        Starts the game
        """
        kb_inp = util.KBHit()

        while True:
            time.sleep(config.DELAY)
            self.score += 10 * config.DELAY

            tmp_obj = {
                "background": [],
                "obstacles": [],
                "player": [],
                "player_bullet": [],
                "coins": []
            }

            if kb_inp.kbhit():
                _ch = kb_inp.getch()

                if _ch == "q":
                    break
                if _ch == config.MANDALORIAN_BULLET_CHAR:
                    self.objects["player_bullet"].append(MandalorianBullet(self.player.get_object().position + np.array([2., 0.])))

                if config.DEBUG:
                    if _ch == "1":
                        self.objects["obstacles"].append(FireBeam( \
                                np.array([config.WIDTH, util.randint(0, config.MAX_HEIGHT - 6)], \
                                    dtype='float64')))
                    elif _ch == "2":
                        self.objects["coins"] += \
                                Coins( \
                                    np.array([config.WIDTH, util.randint(0, config.MAX_HEIGHT - 4)], \
                                        dtype='float64'),
                                    np.array([3, util.randint(3, 10)])).get_items()

                self.player.move(_ch)

            self.detect_collisions()

            self.clear()

            for obj_type in self.objects:
                for obj in self.objects[obj_type]:
                    if obj.update():
                        self.screen.draw(obj.get_object())
                        tmp_obj[obj_type].append(obj)

            self.objects = tmp_obj

            self.show_score()
            self.screen.show()

    def show_score(self):
        """
        Prints the scoreboard
        """
        print(f"Score: {int(self.score)}")
        print(f"Time: {time.time() - self.init_time:.2f}")
        print(f"Lives: {self.lives}")

    def detect_collisions(self):
        """
        Detects collision between various objects
        """
        for pairs in self.colliders:
            for hitter in pairs[0]:
                for target in pairs[1]:
                    pass

    def __del__(self):
        #util.clear()
        #print(col.Style.RESET_ALL)
        #print(graphics.BYE)
        print("\033[?25h")
