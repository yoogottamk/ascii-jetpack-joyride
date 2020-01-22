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
        vel = self.get_velocity()
        self.add_velocity(np.array([np.sign(vel[0]) * config.BOOST_ACTIVE, 0]))

        self.add_position(self.get_velocity())

        pos = self.get_position()
        _h, _w = self.get_shape()

        self.set_position([pos[0], min(config.MAX_HEIGHT - _h, pos[1])])

        pos = self.get_position()

        return self.get_active() and \
            pos[0] + _w >= 0 and \
            pos[0] + _w <= config.WIDTH


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

    def __init__(self, position, player):
        velocity = np.array([-2., 0.])
        rep = util.str_to_array(graphics.BOSS_BULLET)
        color = util.tup_to_array(rep.shape, (col.Back.RED, col.Fore.YELLOW))

        self.player = player

        super().__init__(rep, position, velocity, color)

    def update(self):
        """
        Manages the bullet updates which are supposed to follow Mandalorian
        """
        vel = self.get_velocity()

        self.add_velocity([np.sign(vel[0]) * config.BOOST_ACTIVE, 0])

        y_diff = self.player.get_position()[1] - self.get_position()[1]

        vel = self.get_velocity()
        self.set_velocity([vel[0], int(np.random.normal() > 0.99) * np.sign(y_diff)])

        self.add_position(self.get_velocity())

        pos = self.get_position()
        _h, _w = self.get_shape()

        self.set_position([pos[0], min(config.MAX_HEIGHT - _h, pos[1])])

        pos = self.get_position()
        _h, _w = self.get_shape()

        return self.get_active() and \
            pos[0] + _w >= 0 and \
            pos[0] + _w <= config.WIDTH
