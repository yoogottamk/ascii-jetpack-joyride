"""
This file contains code for the player
This is the base class
"""

import colorama as col
import numpy as np

from objects import GameObject
import graphics
import config
import util
from bullets import DragonBossBullet

class Player(GameObject):
    """
    This is the base class for all "Players": Mandalorian, Dragon
    """

    def __init__(self, rep, position, gravity, color, game):
        """
        Constructor for Player

        Args:
            rep (str)         : How does the player look?
            position [px, py] : Initial position of the Player
            gravity (int)     : Amount of gravity
            color (bg, fg)    : Colors of the player
            game (Game)       : The game object (for accessing other members)
        """
        self.game = game

        super().__init__(rep, position, np.array([0., 0.]), np.array([0., 0.]), gravity, color)

    def move(self, key):
        """
        Manages movements for the Player

        Args:
            key (str) : Which key was pressed?
        """


class Mandalorian(Player):
    """
    This class is for managing the Mandalorian
    """

    def __init__(self, game):
        """
        Constructor for the Mandalorian
        """
        grid = util.str_to_array(graphics.MANDALORIAN)
        grid_col = util.tup_to_array(grid.shape, (col.Back.BLUE, col.Fore.BLACK))
        self.init_pos = np.array([10, config.MAX_HEIGHT], dtype='float64')

        super().__init__(grid, \
                self.init_pos.copy(),\
                0.5, grid_col, game)

        self.controls = ["w", "a", "d"]
        self.shield_active = False
        self.lives = config.MANDALORIAN_LIVES

    def move(self, key):
        """
        Manages movements for the Player

        Args:
            key (str) : Which key was pressed?
        """
        key = key.lower()

        if key in self.controls:
            if key == "w":
                self.velocity[1] -= 2
            elif key == "a":
                self.velocity[0] -= 1
            elif key == "d":
                self.velocity[0] += 1

    def destroy(self):
        """
        Manage destroy for Mandalorian
        """
        if self.shield_active:
            self.deactivate_shield()
            return

        self.position = self.init_pos.copy()

        if self.lives > 1:
            self.lives -= 1
        else:
            self.active = False

    def activate_shield(self):
        """
        Activates shield on the player
        """
        self.shield_active = True
        grid_col = util.tup_to_array(self.rep.shape, (col.Back.YELLOW, config.FG_COL))
        self.set_color(grid_col)


    def deactivate_shield(self):
        """
        Deactivates shield on the player
        """
        self.shield_active = False
        grid_col = util.tup_to_array(self.rep.shape, (config.BG_COL, config.FG_COL))
        self.set_color(grid_col)


class DragonBoss(Player):
    """
    This class is for managing the Dragon Boss enemy
    """

    def __init__(self, game):
        """
        Constructor for the Dragon
        """
        grid = util.str_to_array(graphics.DRAGON)
        grid_col = util.tup_to_array(grid.shape, (col.Back.RED, col.Fore.BLACK))
        grid_col = util.mask(grid, grid_col)
        self.game = game

        super().__init__(grid, np.array([config.WIDTH - 50, 0], dtype="float64"), 0, grid_col, self.game)

        self.counter = 0
        self.lives = config.DRAGONBOSS_LIVES

    def update(self):
        self.counter += 1

        player_y = self.game.player.position[1]

        if np.random.normal() > 0.99:
            self.counter = 0
            self.game.objects["boss_bullet"].append( \
                    DragonBossBullet(self.position + np.array([-2., 3.]), self.game))

        self.position[1] = min(player_y, config.MAX_HEIGHT - self.height)

        return self.active
