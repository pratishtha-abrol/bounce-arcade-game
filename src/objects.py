import numpy as np

class Object:

    def __init__(self, rep=np.array([[" "]]), position=[0,0], velocity=3, gravity=0, color=np.array([[""]])):
        self.position = position
        self.rep = rep
        self.color = color
        self.velocity = velocity
        self.gravity = gravity
        self.shape = self.rep.shape

    def update(self):
        self.position[0] = self.velocity
        self.position[1] = self.gravity

    @staticmethod
    def from_string(rep, position=[0,0], velocity=1, gravity=0, color=""):
        arr = rep.split("\n")[1:-1]
        maxlen = len(max(arr, key=len))

        grid = np.array([list(x + (' ' * (maxlen - len(x)))) for x in arr])
        col = np.full(grid.shape, color)

        return Object(grid, position, velocity, gravity, col)