"""
This file contains the code which runs the game
"""

import time
import numpy as np
import colorama as col

from screen import Screen
from player import Mandalorian, DragonBoss, Dragon
from objects import Ground
from obstacles import FireBeam, Magnet
from coins import Coins
import graphics
from background import Falcon

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

        _t = time.time()

        self.__screen = Screen()
        self.__ground = Ground()

        self.__player = Mandalorian(self)
        self.__dragon = Dragon(self)
        self.__dragon_boss = DragonBoss(self)

        self.__score = 0
        self.__init_time = _t

        self.__frame_count = 0

        self.__shield_active = False
        self.__shield_recharging = True
        self.__last_shield = -1
        self.__last_shield_charge = _t

        self.__last_boost = -1

        self.__dragon_active = False
        self.__dragon_used = False

        self.__boss_mode = False
        self.__over = False

        # seperate them into different classes
        self.__objects = {
            "background": [self.__ground],
            "beams": [],
            "magnets": [],
            "player": [self.__player],
            "boss": [],
            "boss_bullet": [],
            "player_bullet": [],
            "coins": []
        }

        # (x, y, z)
        # x destroys y on collision
        # y destroys x if z
        self.__colliders = [
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
        self.__screen.clear()
        util.clear()

    def start(self):
        """
        Starts the game
        """
        kb_inp = util.KBHit()

        while True:
            if time.time() - self.__init_time > config.TOTAL_TIME:
                self.__over = True

            if self.__over:
                break

            if self.__frame_count == 1000:
                self.__frame_count = 0
                self.__objects["background"].append(Falcon())


            self.__frame_count += 1
            time.sleep(config.DELAY)

            if not self.__boss_mode:
                self.__score += config.DELAY + config.SPEEDOOST_ACTIVE

            if self.__score >= config.BOSS_MIN_SCORE:
                if not self.__boss_mode:
                    self.__objects["boss"] = [self.__dragon_boss]
                    self.deactivate_dragon()

                self.__boss_mode = True

            self.update_shield()
            self.update_boost()

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
                if self.manage_keys(kb_inp.getch()):
                    break
            else:
                kb_inp.clear()

            self.clear()

            if not self.__boss_mode:
                self.spawn_obstacles()

            self.detect_collisions()

            for obj_type in self.__objects:
                for obj in self.__objects[obj_type]:
                    if obj.update():
                        self.__screen.draw(obj, self.__frame_count)
                        tmp_obj[obj_type].append(obj)

            self.__objects = tmp_obj

            self.show_score()
            self.__screen.show()

    def spawn_obstacles(self):
        """
        Spawns obstacles at random
        """
        if np.random.uniform() > 0.95:
            self.spawn_firebeam()
        if np.random.uniform() > 0.99:
            self.spawn_magnet()
        if np.random.uniform() > 0.9:
            self.spawn_coins()

    def spawn_firebeam(self):
        """
        Spawns a firebeam
        """
        self.__objects["beams"].append(FireBeam( \
            np.array([config.WIDTH, util.randint(0, config.MAX_HEIGHT - 6)], \
                dtype='float64')))

    def spawn_magnet(self):
        """
        Spawns a magnet
        """
        self.__objects["magnets"].append(Magnet( \
            np.array([config.WIDTH, config.MAX_HEIGHT - 3 \
                        if np.random.uniform() > 0.5 else 0], \
                    dtype='float64'), \
            self))

    def spawn_coins(self):
        """
        Spawns coins
        """
        self.__objects["coins"] += Coins( \
            np.array([config.WIDTH, \
                util.randint(0, config.MAX_HEIGHT - 4)], dtype='float64'),
            np.array([3, util.randint(3, 10)])).get_items()

    def manage_keys(self, _ch):
        """
        This function manages all key input
        """
        if _ch == config.QUIT_CHAR:
            return True

        if _ch == config.MANDALORIAN_BULLET_CHAR:
            self.shoot_bullet()
        elif _ch == config.SHIELD_CHAR and not self.__shield_recharging:
            self.__player.activate_shield()
            self.__shield_active = True
            self.__last_shield = time.time()
        elif _ch == config.DRAGON_CHAR:
            self.activate_dragon()
        elif _ch == config.SPEEDOOST_CHAR:
            self.activate_boost()

        self.move_player(_ch)

        return False

    def move_player(self, _ch):
        """
        Moves the active player in the game
        """
        if self.__dragon_active:
            self.__dragon.move(_ch)
        else:
            self.__player.move(_ch)

    def shoot_bullet(self):
        """
        This function manages shooting bullets in the game
        """
        if self.__dragon_active:
            self.__objects["player_bullet"].append(self.__dragon.shoot())
        else:
            self.__objects["player_bullet"].append(self.__player.shoot())

    def show_score(self):
        """
        Prints the scoreboard
        """
        _t = time.time()
        shield_recharge_left = config.SHIELD_CHARGE - (_t - self.__last_shield_charge)
        shield_left = config.SHIELD_OUT - (_t - self.__last_shield)

        print(f"🤑 {int(self.__score): >5} | 🕒 {config.TOTAL_TIME - (_t - self.__init_time): .2f}", " "*5)
        print(f"❤️  {self.__player.get_lives(): >5}", end='')
        if self.__boss_mode:
            print(f" | 😈  {self.__dragon_boss.get_lives(): >5}")
        else:
            print()
        print("🛡️" ,end='  ')
        if self.__shield_recharging:
            print("Ready in", f"{shield_recharge_left :.2f}")
        elif self.__shield_active:
            print("Time left", f"{shield_left :.2f}")
        else:
            print("Ready", " "*10)

    def detect_collisions(self):
        """
        Detects collision between various objects
        """
        for pairs in self.__colliders:
            for hitter in self.__objects[pairs[0]]:
                for target in self.__objects[pairs[1]]:
                    pos_h = hitter.get_position()
                    pos_t = target.get_position()

                    height_h, width_h = hitter.get_shape()
                    height_t, width_t = target.get_shape()

                    minx = min(pos_h[0], pos_t[0])
                    maxx = max(pos_h[0] + width_h, pos_t[0] + width_t)

                    miny = min(pos_h[1], pos_t[1])
                    maxy = max(pos_h[1] + height_h, pos_t[1] + height_t)

                    if maxx - minx >= width_h + width_t \
                            or maxy - miny >= height_h + height_t:
                        continue

                    if pairs[1] == "coins":
                        self.__score += 10

                    if pairs[1] == "beams":
                        self.__score += 30

                    target.destroy()
                    if pairs[2]:
                        hitter.destroy()

    def activate_dragon(self):
        """
        Activates the dragon
        """
        if not self.__dragon_used:
            self.__dragon_used = True
            self.__objects["player"] = [self.__dragon]
            self.__dragon_active = True

    def deactivate_dragon(self):
        """
        Deactivates the dragon
        """
        self.__dragon_active = False
        self.__objects["player"] = [self.__player]

    def activate_boost(self):
        """
        Activates speed boost
        """
        config.BOOST_ACTIVE = 0.2
        self.__last_boost = time.time()

    def update_shield(self):
        """
        Manages status of shield
        """
        _t = time.time()

        if self.__shield_recharging:
            if _t - self.__last_shield_charge > config.SHIELD_CHARGE:
                self.__shield_recharging = False
        if self.__shield_active:
            if _t - self.__last_shield > config.SHIELD_OUT:
                self.__shield_active = False
                self.__player.deactivate_shield()
                self.__shield_recharging = True
                self.__last_shield_charge = _t

    def update_boost(self):
        """
        Manages status of speed boost
        """
        _t = time.time()

        if _t - self.__last_boost > config.BOOST_OUT:
            config.BOOST_ACTIVE = 0

    def end_game(self):
        """
        Ends the game
        """
        if time.time() - self.__init_time > config.TOTAL_TIME:
            print(graphics.TIME_OUT)
        elif self.__player.get_lives() == 0:
            print(graphics.LOST_MSG)
        elif self.__over:
            print(graphics.WON_MSG)

    def set_over(self):
        """
        Marks the game for completion
        """
        self.__over = True

    def get_player(self):
        """
        Returns the player object
        """
        return self.__player

    def add_object(self, obj_type, obj):
        """
        Adds an object of type obj_type
        """
        self.__objects[obj_type].append(obj)

    def add_score(self, score):
        """
        Adds score to the game
        """
        self.__score += score

    def __del__(self):
        self.end_game()
        print(col.Style.RESET_ALL)
        print(graphics.BYE)
        print("\033[?25h")
