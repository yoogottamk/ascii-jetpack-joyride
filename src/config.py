"""
This file is supposed to contain all confiuration parameters
"""

import os
import colorama as col

SCREEN_HEIGHT, SCREEN_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]

#WIDTH = SCREEN_WIDTH - 10
HEIGHT = SCREEN_HEIGHT - 5

WIDTH = int(SCREEN_WIDTH / 2)
#HEIGHT = int(SCREEN_HEIGHT / 1.5)

# default colors
bg_col = col.Back.BLUE
fg_col = col.Fore.BLACK

bg_ground = col.Back.GREEN

# delay bw frame updates
delay = 0.1
