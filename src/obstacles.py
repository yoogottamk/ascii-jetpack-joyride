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
    def __init__(self, rep=np.array([[" "]]), position=np.array([0., 0.]),
                 velocity=np.array([0., 0.]), color=np.array([[""]])):
        super().__init__(rep, position, velocity, np.array([0., 0.]), 0., color)

    def update(self):
        self.position += self.velocity

        return self.position[0] + self.width >= 0


class FireBeam(Obstacle):
    def __init__(self, position, orientation=None):
        if orientation is None or orientation < 0 or orientation > config.FIREBEAM_MAX:
            orientation = util.randint(0, config.FIREBEAM_MAX - 1)

        rep = util.str_to_array(graphics.FIREBEAM[orientation])
        color = util.tup_to_array(rep.shape, (col.Back.RED, col.Fore.YELLOW))

        for i in range(rep.shape[0]):
            for j in range(rep.shape[1]):
                if rep[i][j] == " ":
                    color[i][j] = (config.bg_col, col.Fore.YELLOW)

        super().__init__(rep, position, np.array([-2., 0.]), color)
