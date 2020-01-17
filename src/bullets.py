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
        super().__init__(rep, position, velocity, np.array([0., 0.]), 0, color)

    def update(self):
        """
        updates the bullets according to it's physics

        Returns:
            bool : draw this bullet in the next frame?
        """
        self.velocity += self.gravity
        self.position += self.velocity

        self.position[1] = min(config.MAX_HEIGHT - self.height, self.position[1])

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


class DragonBossBullet(Bullet):
    """
    Class for bullets shot by DragonBoss
    """

    def __init__(self, position):
        velocity = np.array([-2., 0.])
        rep = util.str_to_array(graphics.BOSS_BULLET)
        color = util.tup_to_array(rep.shape, (col.Back.RED, col.Fore.YELLOW))

        super().__init__(rep, position, velocity, color)
