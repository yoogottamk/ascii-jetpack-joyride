"""
This file contains the code necessary for coins
"""

import numpy as np
import colorama as col

from objects import GameObject
import util

class Coins(GameObject):
    def __init__(self, position, shape):
        rep = np.full(shape, "$")
        color = util.tup_to_array(rep.shape, (col.Back.YELLOW, col.Fore.RED))

        super().__init__(rep, position, np.array([-2., 0.]), \
                np.array([0., 0.]), 0, color)

    def update(self):
        self.position += self.velocity

        return self.position[0] + self.width >= 0
