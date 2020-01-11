"""
This file will contain the generic object file
"""

import numpy as np
import config

class GameObject:
    """
    All objects should inherit from this class
    Has basic stuff like motion, gravity, color, static motion, etc
    """

    def __init__(self, rep=np.array([[" "]]), position=np.array([0., 0.]),
                 velocity=np.array([0., 0.]), force=np.array([0., 0.]),
                 gravity=0, color=np.array([[""]])):
        """
        Constructor for all objects

        Args:
            rep (2D np.array)   : The object representation (How does it look?)
            position ([x, y])   : Initial position of the object
            velocity ([vx, vy]) : Speed with which the object moves
            force ([fx, fy])    : Force in both dir
            gravity (float)       : Gravitational force on that object
            color (2D np.array) : Color of each character
        """
        self.rep = rep
        self.position = position
        self.velocity = velocity
        self.force = force
        self.gravity = gravity
        self.width = self.rep.shape[1]
        self.height = self.rep.shape[0]
        self.color = color

    def update(self):
        """
        Moves the object according to velocity and gravity applied
        """
        is_on_ground = self.position[1] + self.height >= \
                        config.HEIGHT - config.GROUND_HEIGHT

        # simulate drag
        self.force[0] = ((-1) ** int(self.velocity[0] >= 0)) * 0.05 * (self.velocity[0] ** 2)
        self.force[1] = self.gravity * int(not is_on_ground)

        self.velocity += self.force

        # if is colliding with roof
        if self.position[1] == 0:
            self.velocity[1] = max(0, self.velocity[1])

        if is_on_ground:
            self.velocity[1] = min(0, self.velocity[1])

        print(self.force, self.velocity, (" " * 100))

        tmp_pos = self.position + self.velocity
        self.position[0] = int(np.round(np.clip(tmp_pos[0], 0, config.WIDTH)))
        self.position[1] = int(np.round(np.clip(tmp_pos[1], 0, config.HEIGHT - config.GROUND_HEIGHT)))

    def get_rep(self):
        """
        Sends the string representation of the object
        with color
        """
        return self.rep, self.color

    @staticmethod
    def from_string(rep, position=np.array([0., 0.]),
                    velocity=np.array([0., 0.]), force=np.array([0., 0.]),
                    gravity=0, color=""):
        """
        Creates a GameObject from string

        Args:
            rep (2D np.array)   : The object representation (How does it look?)
            position ([x, y])   : Initial position of the object
            velocity ([vx, vy]) : Speed with which the object moves to left
            force ([fx, fy])    : Force in both dir
            gravity (float)       : Gravitational force on that object
            color (str)         : Color of each character

        Returns:
            GameObject with all the parameters
        """
        arr = rep.split("\n")[1:-1]
        maxlen = len(max(arr, key=len))

        grid = np.array([list(x + (' ' * (maxlen - len(x)))) for x in arr])
        col = np.full(grid.shape, color)

        return GameObject(grid, position, velocity, force, gravity, col)
