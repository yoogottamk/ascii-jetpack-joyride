"""
This file contains code for the player
This is the base class
"""

import colorama as col
import numpy as np

from objects import GameObject
import graphics
import config

class Player:
    """
    This is the base class for all "Players": Mandalorian, Dragon
    """

    def __init__(self, rep, position, color):
        """
        Constructor for Player

        Args:
            rep (str)         : How does the player look?
            position [px, py] : Initial position of the Player
            color (bg, fg)    : Colors of the player
        """
        self.player = GameObject.from_string(rep, position=position, \
                velocity=np.array([0., 0.]), accel=np.array([0., 0.]), \
                gravity=0.5, color=color)

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

    def __init__(self):
        """
        Constructor for the Mandalorian
        """
        super().__init__(graphics.MANDALORIAN, \
                position=np.array([10, config.MAX_HEIGHT]), \
                color=(col.Back.YELLOW, col.Fore.BLACK))
        self.controls = ["w", "a", "d"]

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


class Dragon(Player):
    """
    This class is for managing the Dragon
    """

    def __init__(self):
        """
        Constructor for the Dragon
        """
        super().__init__(graphics.DRAGON, position=np.array([60, 10]), color=col.Fore.BLACK)
