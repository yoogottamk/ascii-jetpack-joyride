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
        self.position += self.velocity

        return self.active and self.position[0] + self.width >= 0


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

        max_i, max_j = rep.shape

        for i in range(max_i):
            for j in range(max_j):
                if rep[i][j] == " ":
                    color[i][j] = (config.BG_COL, col.Fore.YELLOW)

        super().__init__(rep, position, np.array([-2., 0.]), color)
