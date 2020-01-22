"""
This file contains all obstacles
"""

import numpy as np
import colorama as col

from objects import GameObject
import config
import util
import graphics

class Obstacle(GameObject):
    """
    This class will be the parent for all obstacles
    """

    def __init__(self, rep=np.array([[" "]]), position=np.array([0., 0.]),
                 velocity=np.array([0., 0.]), color=np.array([[""]])):
        """
        Constructor for obstacle

        Args:
            rep (2D np.array)   : How the obstacle looks
            position [px, py]   : Initial position of the obstacle
            velocity [vx, vy]   : Velocity of the object
            color (2D np.array) : Color of each pixel of the object
        """
        super().__init__(rep, position, velocity, np.array([0., 0.]), 0., color)

    def update(self):
        """
        Updates the obstacle's position

        Returns:
            bool : Should the object be rendered in the next frame?
        """
        vel = self.get_velocity()
        self.add_velocity(np.array([np.sign(vel[0]) * config.BOOST_ACTIVE, 0.]))

        self.add_position(self.get_velocity())

        pos = self.get_position()
        _, _w = self.get_shape()

        return self.get_active() and pos[0] + _w >= 0


class FireBeam(Obstacle):
    """
    Manages FireBeam
    """

    def __init__(self, position, orientation=None):
        """
        Constructor for FireBeam

        Args:
            position [px, py] : Initial position of the FireBeam
            orientation (int) : 0 -> config.FIREBEAM_MAX, type of FireBeam
        """
        if orientation is None or orientation < 0 or orientation > config.FIREBEAM_MAX:
            orientation = util.randint(0, config.FIREBEAM_MAX - 1)

        rep = util.str_to_array(graphics.FIREBEAM[orientation])
        color = util.tup_to_array(rep.shape, (col.Back.RED, col.Fore.YELLOW))

        super().__init__(rep, position, np.array([-2., 0.]), util.mask(rep, color))


class Magnet(Obstacle):
    """
    Manages the magnet obstacle
    """

    def __init__(self, position, game):
        """
        Constructor for Magnet

        Args:
            position [px, py] : Initial position of the Magnet
            game (Game)       : The game object
        """

        self.game = game
        rep = util.str_to_array(graphics.MAGNET)
        color = util.tup_to_array(rep.shape, (col.Back.MAGENTA, col.Fore.RED))

        super().__init__(rep, position, np.array([-2., 0.]), color=color)

    def update(self):
        """
        Update obstacle's position and attract Mandalorian
        """
        vel = self.get_velocity()
        self.add_velocity(np.array([np.sign(vel[0]) * config.BOOST_ACTIVE, 0.]))

        self.add_position(self.get_velocity())

        diff = np.linalg.norm(self.get_position() - self.game.get_player().get_position()) + 1

        self.game.get_player().add_velocity(0.3 * (self.get_position() - self.game.get_player().get_position()) / diff)

        pos = self.get_position()
        _, _w = self.get_shape()

        return self.get_active() and pos[0] + _w >= 0
