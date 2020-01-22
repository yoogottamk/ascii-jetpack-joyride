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

        self.screen = Screen()
        self.ground = Ground()

        self.player = Mandalorian(self)
        self.dragon = Dragon(self)
        self.dragon_boss = DragonBoss(self)

        self.score = 0
        self.init_time = _t

        self.frame_count = 0

        self.shield_active = False
        self.shield_recharging = True
        self.last_shield = -1
        self.last_shield_charge = _t

        self.last_boost = -1

        self.dragon_active = False
        self.dragon_used = False

        self.boss_mode = False
        self.over = False

        # seperate them into different classes
        self.objects = {
            "background": [self.ground],
            "beams": [],
            "magnets": [],
            "player": [self.player],
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
        self.screen.clear()
        util.clear()

    def start(self):
        """
        Starts the game
        """
        kb_inp = util.KBHit()

        while True:
            if self.over:
                break

            self.frame_count += 1
            time.sleep(config.DELAY)

            if not self.boss_mode:
                self.score += 5 * config.DELAY + config.SPEEDOOST_ACTIVE

            if self.score >= config.BOSS_MIN_SCORE:
                if not self.boss_mode:
                    self.objects["boss"] = [self.dragon_boss]
                    self.deactivate_dragon()

                self.boss_mode = True

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

            if not self.boss_mode:
                self.spawn_obstacles()

            self.detect_collisions()

            for obj_type in self.objects:
                for obj in self.objects[obj_type]:
                    if obj.update():
                        self.screen.draw(obj, self.frame_count)
                        tmp_obj[obj_type].append(obj)

            self.objects = tmp_obj

            self.show_score()
            self.screen.show()

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
        self.objects["beams"].append(FireBeam( \
            np.array([config.WIDTH, util.randint(0, config.MAX_HEIGHT - 6)], \
                dtype='float64')))

    def spawn_magnet(self):
        """
        Spawns a magnet
        """
        self.objects["magnets"].append(Magnet( \
            np.array([config.WIDTH, config.MAX_HEIGHT - 3 \
                        if np.random.uniform() > 0.5 else 0], \
                    dtype='float64'), \
            self))

    def spawn_coins(self):
        """
        Spawns coins
        """
        self.objects["coins"] += Coins( \
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
        elif _ch == config.SHIELD_CHAR and not self.shield_recharging:
            self.player.activate_shield()
            self.shield_active = True
            self.last_shield = time.time()
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
        if self.dragon_active:
            self.dragon.move(_ch)
        else:
            self.player.move(_ch)

    def shoot_bullet(self):
        """
        This function manages shooting bullets in the game
        """
        if self.dragon_active:
            self.objects["player_bullet"].append(self.dragon.shoot())
        else:
            self.objects["player_bullet"].append(self.player.shoot())

    def show_score(self):
        """
        Prints the scoreboard
        """
        print(f"Score: {int(self.score)} | Shield: {self.shield_active}|{self.shield_recharging}" + " "*10)
        print(f"Time: {time.time() - self.init_time:.2f}" + " "*10)
        print(f"Lives: {self.player.get_lives()} | {config.BOOST_ACTIVE}" + " "*10)

    def detect_collisions(self):
        """
        Detects collision between various objects
        """
        for pairs in self.colliders:
            for hitter in self.objects[pairs[0]]:
                for target in self.objects[pairs[1]]:
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
                        self.score += 10

                    if pairs[1] == "beams":
                        self.score += 30

                    target.destroy()
                    if pairs[2]:
                        hitter.destroy()

    def activate_dragon(self):
        """
        Activates the dragon
        """
        if not self.dragon_used:
            self.dragon_used = True
            self.objects["player"] = [self.dragon]
            self.dragon_active = True

    def deactivate_dragon(self):
        """
        Deactivates the dragon
        """
        self.dragon_active = False
        self.objects["player"] = [self.player]

    def activate_boost(self):
        """
        Activates speed boost
        """
        config.BOOST_ACTIVE = 0.2
        self.last_boost = time.time()

    def update_shield(self):
        """
        Manages status of shield
        """
        _t = time.time()

        if self.shield_recharging:
            if _t - self.last_shield_charge > config.SHIELD_CHARGE:
                self.shield_recharging = False
        if self.shield_active:
            if _t - self.last_shield > config.SHIELD_OUT:
                self.shield_active = False
                self.player.deactivate_shield()
                self.shield_recharging = True
                self.last_shield_charge = _t

    def update_boost(self):
        """
        Manages status of speed boost
        """
        _t = time.time()

        if _t - self.last_boost > config.BOOST_OUT:
            config.BOOST_ACTIVE = 0

    def end_game(self):
        """
        Ends the game
        """
        if self.player.get_lives() == 0:
            print(graphics.LOST_MSG)
        elif self.over:
            print(graphics.WON_MSG)

    def __del__(self):
        self.end_game()
        print(col.Style.RESET_ALL)
        print(graphics.BYE)
        print("\033[?25h")
