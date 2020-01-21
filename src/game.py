"""
This file contains the code which runs the game
"""

import time
import numpy as np

from screen import Screen
from player import Mandalorian, DragonBoss, Dragon
from objects import Ground
from obstacles import FireBeam, Magnet
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

        # hide the cursor and clear the screen
        print("\033[?25l\033[2J", end='')

        self.screen = Screen()
        self.player = Mandalorian(self)
        self.ground = Ground()
        self.dragon_boss = DragonBoss(self)
        self.dragon = Dragon(self)
        self.score = 0
        self.init_time = time.time()
        self.frame_count = 0

        # seperate them into different classes
        self.objects = {
            "background": [self.ground],
            "beams": [],
            "magnets": [],
            "player": [self.dragon],
            "boss": [],
            "boss_bullet": [],
            "player_bullet": [],
            "coins": []
        }

        # (x, y, z)
        # x destroys y on collision
        # y destroys x if z
        self.colliders = [
            ("beams", "player", True),
            ("player", "coins", False),
            ("player_bullet", "beams", True),
            ("player_bullet", "boss", True),
            ("boss", "player", False),
            ("player_bullet", "boss_bullet", True),
            ("boss_bullet", "player", True)
        ]

    def clear(self):
        """
        Clears the screen and the frame
        """
        self.screen.clear(self.frame_count)
        util.clear()

    def start(self):
        """
        Starts the game
        """
        kb_inp = util.KBHit()

        while True and self.player.active:
            self.frame_count += 1
            time.sleep(config.DELAY)
            self.score += 10 * config.DELAY

            tmp_obj = {
                "background": [],
                "beams": [],
                "magnets": [],
                "player": [],
                "boss": [],
                "boss_bullet": [],
                "player_bullet": [],
                "coins": []
            }

            if kb_inp.kbhit():
                _ch = kb_inp.getch()

                if _ch == "q":
                    break
                if _ch == config.MANDALORIAN_BULLET_CHAR and \
                        len(self.objects["player_bullet"]) < config.BULLET_MAX:
                    self.objects["player_bullet"].append( \
                            MandalorianBullet(self.player.position + np.array([2., 0.])))
                if _ch == config.SHIELD_CHAR:
                    self.player.activate_shield()

                if config.DEBUG:
                    if _ch == "1":
                        self.objects["beams"].append(FireBeam( \
                                np.array([config.WIDTH, util.randint(0, config.MAX_HEIGHT - 6)], \
                                    dtype='float64')))
                    elif _ch == "2":
                        self.objects["coins"] += \
                                Coins( \
                                    np.array([config.WIDTH, \
                                        util.randint(0, config.MAX_HEIGHT - 4)], dtype='float64'),
                                    np.array([3, util.randint(3, 10)])).get_items()
                    elif _ch == "3":
                        self.objects["magnets"].append( \
                                Magnet( \
                                    np.array([config.WIDTH, config.MAX_HEIGHT - 4 \
                                                if np.random.normal() > 0.5 else 0], \
                                            dtype='float64'), \
                                    self))
                    elif _ch == "4":
                        self.objects["boss"].append(self.dragon_boss)

                self.dragon.move(_ch)
            else:
                kb_inp.clear()

            self.clear()

            self.detect_collisions()

            for obj_type in self.objects:
                for obj in self.objects[obj_type]:
                    if obj.update():
                        self.screen.draw(obj, self.frame_count)
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
        print(f"Lives: {self.player.lives}")

    def detect_collisions(self):
        """
        Detects collision between various objects
        """
        for pairs in self.colliders:
            for hitter in self.objects[pairs[0]]:
                for target in self.objects[pairs[1]]:
                    obj_h = hitter
                    obj_t = target

                    pos_h = obj_h.position
                    pos_t = obj_t.position

                    minx = min(pos_h[0], pos_t[0])
                    maxx = max(pos_h[0] + obj_h.width, pos_t[0] + obj_t.width)

                    miny = min(pos_h[1], pos_t[1])
                    maxy = max(pos_h[1] + obj_h.height, pos_t[1] + obj_t.height)

                    if maxx - minx >= obj_h.width + obj_t.width \
                            or maxy - miny >= obj_h.height + obj_t.height:
                        continue

                    obj_t.destroy()
                    if pairs[2]:
                        obj_h.destroy()

    def __del__(self):
        #util.clear()
        #print(col.Style.RESET_ALL)
        #print(graphics.BYE)
        print("\033[?25h")
