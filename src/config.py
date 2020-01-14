"""
This file is supposed to contain all configuration parameters
"""

import os
import colorama as col

SCREEN_HEIGHT, SCREEN_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]

WIDTH = SCREEN_WIDTH - 10
HEIGHT = SCREEN_HEIGHT - 3

GROUND_HEIGHT = 5

MAX_HEIGHT = HEIGHT - GROUND_HEIGHT

DRAG_CONST = 0.05

# default colors
BG_COL = col.Back.BLUE
FG_COL = col.Fore.BLACK

BG_GROUND = col.Back.GREEN

# delay bw frame updates
DELAY = 0.05

# FireBeam orientations
FIREBEAM_MAX = 4
