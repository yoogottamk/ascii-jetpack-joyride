"""
This is the file for storing classes for bullets
"""

import numpy as np
import colorama as col

from objects import GameObject
import config
import graphics
import util

class Bullet(GameObject):
    """
    Base class for all bullets
    """

    def __init__(self, rep, position, velocity, color):
        """
        Constructor for Bullet
        """
        self.position = position
        self.velocity = velocity

        super().__init__(rep, position, velocity, np.array([0., 0.]), 0, color)

    def update(self):
        """
        updates the bullets according to it's physics

        Returns:
            bool : draw this bullet in the next frame?
        """
        self.position += self.velocity

        return self.active and \
            self.position[0] + self.width >= 0 and \
            self.position[0] + self.width <= config.WIDTH

class MandalorianBullet(Bullet):
    """
    Class for bullets shot by Mandalorian
    """

    def __init__(self, position):
        velocity = np.array([2., 0.])
        rep = util.str_to_array(graphics.MANDALORIAN_BULLET)
        color = util.tup_to_array(rep.shape, (col.Back.WHITE, col.Fore.BLACK))

        super().__init__(rep, position, velocity, color)
