"""
This file will contain the generic object file
"""

import numpy as np

class GameObject:
    """
    All objects should inherit from this class
    Has basic stuff like motion, gravity, color, static motion, etc
    """

    def __init__(self, rep=np.array([[" "]]), position=[0, 0],
                 velocity=3, gravity=0, color=np.array([[""]])):
        """
        Constructor for all objects

        Args:
            rep (2D np.array)   : The object representation (How does it look?)
            position ([x, y])   : Initial position of the object
            velocity (int)      : Speed with which the object moves to left
            gravity (int)       : Speed with which the object moves down
            color (2D np.array) : Color of each character
        """
        self.position = position
        self.rep = rep
        self.color = color
        self.velocity = velocity
        self.gravity = gravity
        self.shape = self.rep.shape


    def update(self):
        """
        Moves the object according to velocity and gravity applied
        """
        self.position[0] -= self.velocity
        self.position[1] += self.gravity


    @staticmethod
    def from_string(rep, position=[0, 0], velocity=1, gravity=0, color=""):
        """
        Creates a GameObject from string

        Args:
            rep (2D np.array)   : The object representation (How does it look?)
            position ([x, y])   : Initial position of the object
            velocity (int)      : Speed with which the object moves to left
            gravity (int)       : Speed with which the object moves down
            color (2D np.array) : Color of each character

        Returns:
            GameObject with all the parameters
        """
        arr = rep.split("\n")[1:-1]
        maxlen = len(max(arr, key=len))

        grid = np.array([list(x + (' ' * (maxlen - len(x)))) for x in arr])
        col = np.full(grid.shape, color)

        return GameObject(grid, position, velocity, gravity, col)
