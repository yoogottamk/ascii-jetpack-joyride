"""
This file contains the code necessary for coins
"""

import numpy as np
import colorama as col

from objects import GameObject
import util

class Coin(GameObject):
    """
    This class is for the coin
    """

    def __init__(self, position):
        rep = np.array([["$"]])
        super().__init__(rep, position, np.array([-2., 0.]), \
                   np.array([0., 0.]), 0, util.tup_to_array((1, 1), (col.Back.YELLOW, col.Fore.RED)))

    def update(self):
        """
        This function updates the coin after each frame

        Returns:
            bool : Should the object be rendered in the next frame
        """
        self.position += self.velocity

        return self.active and self.position[0] + self.width >= 0

class Coins:
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
        self.position = position
        self.shape = shape

        minx, miny = position
        maxx, maxy = minx + shape[1], miny + shape[0]

        minx = int(minx)
        maxx = int(maxx)
        miny = int(miny)
        maxy = int(maxy)

        self.coins = []

        for _x in range(minx, maxx):
            for _y in range(miny, maxy):
                self.coins.append(Coin((_x, _y)))

    def get_items(self):
        return self.coins
