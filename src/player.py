"""
This file contains code for the player
This is the base class
"""

import colorama as col
import numpy as np

from objects import GameObject
import graphics
import config
import util
from bullets import MandalorianBullet, DragonBossBullet

class Player(GameObject):
    """
    This is the base class for all "Players"
    """

    def __init__(self, rep, position, gravity, color, lives, game):
        """
        Constructor for Player

        Args:
            rep (2D np.array) : How does the player look?
            position [px, py] : Initial position of the Player
            gravity (int)     : Amount of gravity
            color (bg, fg)    : Colors of the player
            lives (int)       : Number of lives the player has
            game (Game)       : The game object (for accessing other members)
        """
        self.game = game
        self.__lives = lives

        super().__init__(rep, position, np.array([0., 0.]), np.array([0., 0.]), gravity, color)

    def move(self, key):
        """
        Manages movements for the Player

        Args:
            key (str) : Which key was pressed?
        """

    def destroy(self):
        """
        Checks for lives and destroys
        """
        if self.__lives > 1:
            self.__lives -= 1
        else:
            self.__lives = 0
            self.set_active(False)

    def get_lives(self):
        """
        Returns how many lives are left
        """
        return self.__lives

    def decr_lives(self):
        """
        Reduces the lives by 1
        """
        self.__lives -= 1


class Mandalorian(Player):
    """
    This class is for managing the Mandalorian
    """

    def __init__(self, game):
        """
        Constructor for the Mandalorian
        """
        grid = util.str_to_array(graphics.MANDALORIAN)
        grid_col = util.tup_to_array(grid.shape, (col.Back.BLUE, col.Fore.BLACK))
        self.init_pos = np.array([10, config.MAX_HEIGHT], dtype='float64')

        super().__init__(grid, \
                self.init_pos.copy(),\
                0.45, grid_col, config.MANDALORIAN_LIVES, game)

        self.__controls = ["w", "a", "d"]
        self.shield_active = False

    def move(self, key):
        """
        Manages movements for the Player

        Args:
            key (str) : Which key was pressed?
        """
        key = key.lower()

        if key in self.__controls:
            if key == "w":
                self.add_velocity([0, -2])
            elif key == "a":
                self.add_velocity([-1, 0])
            elif key == "d":
                self.add_velocity([1, 0])

    def shoot(self):
        """
        Shoots a bullet
        """
        return MandalorianBullet(self.get_position() + np.array([2., 0.]))

    def destroy(self):
        """
        Manage destroy for Mandalorian
        """
        self.set_position(self.init_pos.copy())
        self.set_velocity(np.array([0., 0.]))
        lives = self.get_lives()

        if self.shield_active:
            return

        if lives > 1:
            self.decr_lives()
        else:
            self.decr_lives()
            self.set_active(False)
            self.game.over = True

    def activate_shield(self):
        """
        Activates shield on the player
        """
        self.shield_active = True
        grid_col = util.tup_to_array(self.get_shape(), (col.Back.YELLOW, config.FG_COL))
        self.set_color(grid_col)


    def deactivate_shield(self):
        """
        Deactivates shield on the player
        """
        self.shield_active = False
        grid_col = util.tup_to_array(self.get_shape(), (config.BG_COL, config.FG_COL))
        self.set_color(grid_col)


class Dragon(Player):
    """
    This class is for managing our Dragon
    """

    def __init__(self, game):
        """
        Constructor for the dragon
        """
        self.width = 60
        self.height = 7
        self.controls = ["w"]
        self.head = 0

        rep = np.full((self.height, self.width), " ")
        color = util.tup_to_array((self.height, self.width), (col.Back.BLACK, col.Fore.GREEN))

        super().__init__(rep, np.array([0., config.MAX_HEIGHT - self.height]), 0.3, color, 1, game)


    def move(self, key):
        """
        Manages movements for the Player

        Args:
            key (str) : Which key was pressed?
        """
        key = key.lower()

        if key in self.controls:
            if key == "w":
                self.add_velocity([0, -2])

    def destroy(self):
        """
        Manage destroy for Dragon
        """
        self.game.deactivate_dragon()

    def get_rep(self, phase_offset=0):
        """
        Returns the live representation of dragon
        """
        rep = np.full((self.height, self.width), " ")
        color = util.tup_to_array(rep.shape, (col.Back.BLACK, col.Fore.GREEN))

        dragon_head = util.str_to_array(graphics.DRAGON_HEAD)
        head_h, head_w = dragon_head.shape

        # phase_offset = 4 * (phase_offset // 4)

        _h, _w = self.get_shape()

        body_width = _w - head_w

        _y = np.sin(np.linspace(-np.pi, np.pi, body_width) + phase_offset)
        _y *= (_h / 2)
        _y += (_h / 2)

        _y = _y.astype(int)

        for i in range(body_width):
            rep[_y[i]][i] = "~"

            if _y[i] > self.height - 2:
                rep[_y[i] - 2][i] = "~"
            else:
                rep[_y[i] + 1][i] = "~"

            if _y[i] == 0:
                rep[2][i] = "~"
            else:
                rep[_y[i] - 1][i] = "~"

        beg_h = int(min(_y[-1], self.height - head_h))

        rep[beg_h:beg_h + head_h, -head_w:] = dragon_head

        self.head = self.get_position() + beg_h

        color = util.mask(rep, color)

        return rep, color

    def shoot(self):
        """
        Shoots the bullet for Dragon
        """
        _, _w = self.get_shape()
        return MandalorianBullet(self.head + np.array([_w, 0.]))


class DragonBoss(Player):
    """
    This class is for managing the Dragon Boss enemy
    """

    def __init__(self, game):
        """
        Constructor for the Dragon
        """
        grid = util.str_to_array(graphics.DRAGON)
        grid_col = util.tup_to_array(grid.shape, (col.Back.RED, col.Fore.BLACK))
        grid_col = util.mask(grid, grid_col)
        self.game = game

        super().__init__(grid, \
                    np.array([config.WIDTH - 50, 0], dtype="float64"), \
                    0, grid_col, config.DRAGONBOSS_LIVES, self.game)

    def update(self):
        player_y = self.game.player.get_position()[1]

        _h, _ = self.get_shape()

        if np.random.normal() > 0.99:
            self.game.objects["boss_bullet"].append( \
                    DragonBossBullet(self.get_position() + np.array([-2., 3.]), self.game.player))

        pos = self.get_position()
        self.set_position([pos[0], min(player_y, config.MAX_HEIGHT - _h)])

        return self.get_active()

    def destroy(self):
        """
        Reduces lives for dragon and end game if its over
        """
        lives = self.get_lives()

        if lives > 1:
            self.decr_lives()
        else:
            self.set_active(False)
            self.game.over = True
            self.game.score += 1000
