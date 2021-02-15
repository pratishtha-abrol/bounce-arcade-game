import numpy as np
import config

class Object:

    def __init__(self, rep=np.array([[" "]]), position=np.array([0,0]), velocity=np.array([0.,0.]), color=np.array([[""]])):
        self.rep = rep
        self.position = position
        self.velocity = velocity
        self.width = self.rep.shape[1]
        self.height = self.rep.shape[0]
        self.color = color

    def update(self):
        pass

    @staticmethod
    def from_string(rep, position=np.array([0,0]), velocity=np.array([0.,0.]), color=""):
        arr = rep.split("\n")[1:-1]
        maxlen = len(max(arr, key=len))

        grid = np.array([list(x + (' ' * (maxlen - len(x)))) for x in arr])
        col = np.full(grid.shape, color)

        return Object(grid, position, velocity, col)