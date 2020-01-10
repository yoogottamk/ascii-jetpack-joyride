"""
This file is supposed to contain all confiuration parameters
"""

import os
import colorama as col

SCREEN_HEIGHT, SCREEN_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]

# default colors
bg_col = col.Back.BLUE
fg_col = col.Fore.BLACK

# delay bw frame updates
delay = 0.1
