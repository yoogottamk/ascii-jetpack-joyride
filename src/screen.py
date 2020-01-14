"""
This file is supposed to contain all the logic related to
displaying stuff on screen
"""

import sys
import numpy as np
import colorama as col

import config
import util

class Screen:
    """
    This class manages the screen: whatever is printed, how the frames
    are updated, etc.
    """

    def __init__(self):
        self.width, self.height = config.WIDTH, config.HEIGHT
        self.clear()

    def clear(self):
        """
        This function clears the current frame
        """
        self.display = np.full((self.height, self.width), " ")
        self.color = util.tup_to_array((self.height, self.width), (col.Back.BLUE, col.Fore.BLACK))

    def draw(self, obj):
        """
        This function places an object on the frame
        """
        x, y = obj.position
        h, w = obj.height, obj.width

        x = int(x)
        y = int(y)
        h = int(h)
        w = int(w)

        disp, color = obj.get_rep()

        disp = disp[:, max(0, -x):min(config.WIDTH - x, w)]
        color = color[:, max(0, -x):min(config.WIDTH - x, w)]

        self.display[y:y+h, max(0, x):min(x+w, config.WIDTH)] = disp
        self.color[y:y+h, max(0, x):min(x+w, config.WIDTH)] = color

    def show(self):
        """
        This function displays the current frame on the screen
        """
        out = ""

        for i in range(self.height):
            for j in range(self.width):
                out += "".join(self.color[i][j]) + self.display[i][j]
            out += "\n"

        sys.stdout.write(out + col.Style.RESET_ALL)
