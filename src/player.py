"""
This file contains code for the player
This is the base class
"""

import colorama as col

from objects import GameObject
import graphics

class Player:
    def __init__(self, rep, position, color):
        self.player = GameObject.from_string(rep, position=position,
                velocity=0, gravity=1, color=color)

    def move(self, direction=0):
        pass

    def update(self):
        self.player.update()

    def get_object(self):
        return self.player

class Mandalorian(Player):
    def __init__(self):
        super().__init__(graphics.MANDALORIAN, [30, 10], col.Fore.BLACK)
