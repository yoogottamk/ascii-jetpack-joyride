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

class Player:
    """
    This is the base class for all "Players": Mandalorian, Dragon
    """

    def __init__(self, rep, position, gravity, color, game):
        """
        Constructor for Player

        Args:
            rep (str)         : How does the player look?
            position [px, py] : Initial position of the Player
            color (bg, fg)    : Colors of the player
        """
        self.player = GameObject.from_string(rep, position, \
                np.array([0., 0.]), np.array([0., 0.]), \
                gravity, color)
        self.game = game

    def move(self, key):
        """
        Manages movements for the Player

        Args:
            key (str) : Which key was pressed?
        """

    def update(self):
        """
        Updates the player's position, velocity, etc

        Returns:
            bool : Should the player be drawn in the next frame?
        """
        return self.player.update()

    def get_object(self):
        """
        Returns the player object, which has to be updated

        Returns:
            GameObject : The player object
        """
        return self.player


class Mandalorian(Player):
    """
    This class is for managing the Mandalorian
    """

    def __init__(self, game):
        """
        Constructor for the Mandalorian
        """
        super().__init__(graphics.MANDALORIAN, \
                np.array([10, config.MAX_HEIGHT], dtype='float64'), \
                0.5, (col.Back.BLUE, col.Fore.BLACK), game)
        self.controls = ["w", "a", "d"]
        self.player.lives = config.MANDALORIAN_LIVES

    def move(self, key):
        """
        Manages movements for the Player

        Args:
            key (str) : Which key was pressed?
        """
        key = key.lower()

        if key in self.controls:
            if key == "w":
                self.player.velocity[1] -= 2
            elif key == "a":
                self.player.velocity[0] -= 1
            elif key == "d":
                self.player.velocity[0] += 1


class DragonBoss(Player):
    """
    This class is for managing the Dragon Boss enemy
    """

    def __init__(self, game):
        """
        Constructor for the Dragon
        """
        self.counter = 0
        super().__init__(graphics.DRAGON, np.array([config.WIDTH - 50, 0], dtype="float64"), 0, (col.Back.RED, col.Fore.BLACK), game)
        self.player.lives = config.DRAGONBOSS_LIVES

    def update(self):
        self.counter += 1

        player_y = self.game.player.get_object().position[1]
        boss_obj = self.get_object()

        if np.random.random() > 0.9:
            self.counter = 0
            self.game.objects["boss_bullet"].append(DragonBossBullet(boss_obj.position + np.array([-2., 3.])))

        boss_obj.position[1] = min(player_y, config.MAX_HEIGHT - boss_obj.height)

        return boss_obj.active
