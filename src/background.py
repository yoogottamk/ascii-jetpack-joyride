"""
This file will manage all background graphics
"""

import numpy as np

from objects import GameObject
import graphics
import util
import config

class Background(GameObject):
    """
    This is the base class for all decorations
    """

    def __init__(self, rep, position, velocity):
        """
        Constructor for background
        """
        color = util.tup_to_array(rep.shape, (config.BG_COL, config.FG_COL))

        super().__init__(rep, position, velocity, np.array([0., 0.]), 0, color)

    def update(self):
        """
        Updates the background object
        """
        vel = self.get_velocity()
        self.add_velocity(np.array([np.sign(vel[0]) * config.BOOST_ACTIVE, 0.]))

        self.add_position(self.get_velocity())

        pos = self.get_position()
        _, _w = self.get_shape()

        return self.get_active() and pos[0] + _w >= 0


class Falcon(Background):
    """
    This will be the base class for Millenium Falcon
    """

    def __init__(self):
        """
        Constructor for falcon
        """
        rep = util.str_to_array(graphics.FALCON)

        position = np.array([config.WIDTH, 1.])

        super().__init__(rep, position, np.array([-4., 0.]))
