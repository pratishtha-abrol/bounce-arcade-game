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
        on_ground = self.position[1] + self.height >= \
                        config.HEIGHT - config.SLIDER_LOC


        # if is colliding with roof
        if self.position[1] == 0:
            self.velocity[1] = max(0, self.velocity[1])

        if on_ground:
            self.velocity[1] = min(0, self.velocity[1])


        tmp_pos = self.position + self.velocity
        self.position[0] = int(np.round(np.clip(tmp_pos[0], 0, config.WIDTH)))
        self.position[1] = int(np.round(np.clip(tmp_pos[1], 0, config.HEIGHT - config.SLIDER_LOC)))

    @staticmethod
    def from_string(rep, position=np.array([0,0]), velocity=np.array([0.,0.]), color=""):
        arr = rep.split("\n")[1:-1]
        maxlen = len(max(arr, key=len))

        grid = np.array([list(x + (' ' * (maxlen - len(x)))) for x in arr])
        col = np.full(grid.shape, color)

        return Object(grid, position, velocity, col)