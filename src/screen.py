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
        self.fg = np.full((self.height, self.width), col.Fore.BLACK)

    def draw(self, obj):
        x, y = obj.position
        h, w = obj.height, obj.width

        self.display[y:y+h, x:x+w], self.fg[y:y+h, x:x+w] = obj.get_rep()

    def show(self):
        out = col.Back.BLUE

        for i in range(self.height):
            for j in range(self.width):
                out += self.fg[i][j] + self.display[i][j]
            out += "|\n"

        sys.stdout.write(out + col.Style.RESET_ALL)
