"""
This file contains code which runs / manages everything else
"""

import colorama as col
import warnings

from game import Game

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    col.init()

    Game().start()
