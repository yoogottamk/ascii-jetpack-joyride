"""
This file contains the code necessary for coins
"""

import numpy as np
import colorama as col

from objects import GameObject
import util

class Coins(GameObject):
    """
    This class is for all the coins
    """

    def __init__(self, position, shape):
        """
        Initializes the coins object

        Args:
            position [px, py]     : Position where the coins will be placed
            shape [height, width] : Shape of the bundle of coins
        """
        rep = np.full(shape, "$")
        color = util.tup_to_array(rep.shape, (col.Back.YELLOW, col.Fore.RED))

        super().__init__(rep, position, np.array([-2., 0.]), \
                np.array([0., 0.]), 0, color)

    def update(self):
        """
        This function updates the object after each frame

        Returns:
            bool : Should the object be rendered in the next frame
        """
        self.position += self.velocity

        return self.position[0] + self.width >= 0
