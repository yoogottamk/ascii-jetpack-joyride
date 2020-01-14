"""
This file contains code which runs / manages everything else
"""

import colorama as col

from game import Game

if __name__ == "__main__":
    col.init()

    Game().start()
