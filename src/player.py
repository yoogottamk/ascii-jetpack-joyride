"""
This file contains code for the player
This is the base class
"""

import colorama as col
import numpy as np

from objects import GameObject
import graphics
import config

class Player:
    def __init__(self, rep, position, color):
        self.player = GameObject.from_string(rep, position=position,
                velocity=np.array([0., 0.]), force=np.array([0., 0.]),
                gravity=0.5, color=color)

    def move(self, key):
        pass

    def update(self):
        self.player.update()

    def get_object(self):
        return self.player


class Mandalorian(Player):
    def __init__(self):
        super().__init__(graphics.MANDALORIAN, position=np.array([10, config.MAX_HEIGHT]), color=col.Fore.BLACK)
        self.controls = ["w", "a", "d"]

    def move(self, key):
        key = key.lower()

        if key in self.controls:
            if key == "w":
                self.player.velocity[1] -= 2
            elif key == "a":
                self.player.velocity[0] -= 1
            elif key == "d":
                self.player.velocity[0] += 1


class Dragon(Player):
    def __init__(self):
        super().__init__(graphics.DRAGON, position=np.array([60, 10]), color=col.Fore.BLACK)
