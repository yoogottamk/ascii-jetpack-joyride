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
        self.__rep = rep
        self.__position = position
        self.__velocity = velocity
        self.__accel = accel
        self.__gravity = gravity
        self.__height, self.__width = self.__rep.shape
        self.__color = color
        self.__active = True

    def update(self):
        """
        Moves the object according to velocity and gravity applied

        Returns:
            bool: whether to destroy this object or not
        """
        is_on_ground = self.__position[1] + self.__height >= \
                        config.MAX_HEIGHT

        if np.isinf(self.__velocity[0]):
            self.__velocity[0] = 0

        # simulate drag
        self.__accel[0] = ((-1) ** int(self.__velocity[0] >= 0)) *\
                config.DRAG_CONST * (self.__velocity[0] ** 2)
        self.__accel[1] = self.__gravity * int(not is_on_ground)

        if self.__class__.__name__ != "Mandalorian":
            self.__velocity[0] += np.sign(self.__velocity[0]) * config.BOOST_ACTIVE

        self.__velocity += self.__accel

        # if is colliding with roof
        if self.__position[1] == 0:
            self.__velocity[1] = max(0, self.__velocity[1])

        if is_on_ground:
            self.__velocity[1] = min(0, self.__velocity[1])

        np.clip(self.__velocity, -5, 5)

        tmp_pos = self.__position + self.__velocity

        self.__position[0] = int(np.round(np.clip(tmp_pos[0], 0, config.WIDTH - self.__width)))
        self.__position[1] = int(np.round(np.clip(tmp_pos[1], 0, config.MAX_HEIGHT - self.__height)))

        return self.__active and self.__position[0] + self.__width >= 0

    def get_rep(self, frame=0):
        """
        Sends the string representation of the object
        with color
        """
        return self.__rep, self.__color

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
        self.__color = color

    def destroy(self):
        """
        Marks this object for destruction
        """
        self.__active = False

    def get_position(self):
        """
        Returns the position
        """
        return self.__position

    def set_position(self, pos):
        """
        Sets the position
        """
        self.__position = pos

    def add_position(self, pos):
        """
        Adds to the position
        """
        self.__position += pos

    def get_shape(self):
        """
        Returns the shape [h, w]
        """
        return (self.__height, self.__width)

    def get_velocity(self):
        """
        Returns the velocity
        """
        return self.__velocity

    def set_velocity(self, vel):
        """
        Sets the velocity
        """
        self.__velocity = np.array(vel)

    def add_velocity(self, vel):
        """
        Adds something to the velocity
        """
        self.__velocity += np.array(vel)

    def get_active(self):
        """
        Returns whether object is active or not
        """
        return self.__active

    def set_active(self, active):
        """
        Sets the active state of the object
        """
        self.__active = active

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
