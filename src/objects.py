"""
This file will contain the generic object file
"""

import numpy as np
import colorama as col

import config
import util

class GameObject:
    """
    All objects should inherit from this class
    Has basic stuff like motion, gravity, color, static motion, etc
    """

    def __init__(self, rep=np.array([[" "]]), position=np.array([0., 0.]),
                 velocity=np.array([0., 0.]), accel=np.array([0., 0.]),
                 gravity=0, color=np.array([[("", "")]])):
        """
        Constructor for all objects

        Args:
            rep (2D np.array)   : The object representation (How does it look?)
            position ([x, y])   : Initial position of the object
            velocity ([vx, vy]) : Speed with which the object moves
            accel ([fx, fy])    : accel in both dir
            gravity (float)     : Gravitational accel on that object
            color (2D np.array) : Color of each character
        """
        self.rep = rep
        self.position = position
        self.velocity = velocity
        self.accel = accel
        self.gravity = gravity
        self.width = self.rep.shape[1]
        self.height = self.rep.shape[0]
        self.color = color
        self.active = True
        self.lives = 1

    def update(self):
        """
        Moves the object according to velocity and gravity applied

        Returns:
            bool: whether to destroy this object or not
        """
        is_on_ground = self.position[1] + self.height >= \
                        config.MAX_HEIGHT

        # simulate drag
        self.accel[0] = ((-1) ** int(self.velocity[0] >= 0)) *\
                config.DRAG_CONST * (self.velocity[0] ** 2)
        self.accel[1] = self.gravity * int(not is_on_ground)

        self.velocity += self.accel

        # if is colliding with roof
        if self.position[1] == 0:
            self.velocity[1] = max(0, self.velocity[1])

        if is_on_ground:
            self.velocity[1] = min(0, self.velocity[1])

        tmp_pos = self.position + self.velocity
        self.position[0] = int(np.round(np.clip(tmp_pos[0], 0, config.WIDTH - self.width)))
        self.position[1] = int(np.round(np.clip(tmp_pos[1], 0, config.MAX_HEIGHT - self.height)))

        return self.active and self.position[0] + self.width >= 0

    def get_rep(self):
        """
        Sends the string representation of the object
        with color
        """
        return self.rep, self.color

    @staticmethod
    def from_string(rep, position=np.array([0., 0.]),
                    velocity=np.array([0., 0.]), accel=np.array([0., 0.]),
                    gravity=0, color=("", "")):
        """
        Creates a GameObject from string

        Args:
            rep (2D np.array)   : The object representation (How does it look?)
            position ([x, y])   : Initial position of the object
            velocity ([vx, vy]) : Speed with which the object moves to left
            accel ([fx, fy])    : accel in both dir
            gravity (float)     : Gravitational accel on that object
            color (str, str)    : Color of each character (bg, fg)

        Returns:
            GameObject with all the parameters
        """
        grid = util.str_to_array(rep)
        color = util.mask(grid, util.tup_to_array(grid.shape, color))

        return GameObject(grid, position, velocity, accel, gravity, color)

    def set_color(self, color):
        """
        Changes the color
        """
        self.color = color

    def destroy(self):
        """
        Marks this object for destruction
        """
        if self.lives > 1:
            self.lives -= 1
        else:
            self.active = False

    def __del__(self):
        """
        For debugging
        """
        if config.DEBUG_ALL:
            print("Destroyed", self.__class__.__name__)


class Ground(GameObject):
    """
    This is the class for Ground
    """

    def __init__(self):
        """
        Constructor for Ground
        """
        rep = np.full((config.GROUND_HEIGHT, config.WIDTH), ".")
        color = util.tup_to_array(rep.shape, (col.Back.GREEN, col.Fore.BLACK))
        pos = np.array([0, config.MAX_HEIGHT])

        super().__init__(rep=rep, position=pos, color=color)

    def update(self):
        """
        Updates the ground

        Returns:
            bool : Should the ground be drawn in the next frame? (YES!)
        """
        return True
