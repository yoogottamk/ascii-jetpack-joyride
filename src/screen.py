"""
This file is supposed to contain all the logic related to
displaying stuff on screen
"""

import numpy as np
import colorama as col
import sys

import config

class Screen:
    def __init__(self):
        self.width, self.height = config.WIDTH, config.HEIGHT
        self.clear()

    def clear(self):
        self.display = np.full((self.height, self.width), " ")
        self.fg = np.full((self.height, self.width), config.fg_col)
        self.bg = np.full((self.height, self.width), config.bg_col)

    def draw(self, obj):
        x, y = obj.position
        h, w = obj.shape

        self.display[y:y+h, x:x+w] = obj.rep
        self.fg[y:y+h, x:x+w] = obj.color

    def show(self):
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self.bg[i][j] + self.fg[i][j] + self.display[i][j])
            sys.stdout.write("|" + col.Back.RESET + "\n")

        sys.stdout.write(col.Style.RESET_ALL)
