import global_var

class Object() :

    def __init__(self, character, posx, posy):
        self._posx = posx
        self._posy = posy
        self._width = len(character[0])
        self._height = len(character)
        self._shape = character

    def render(self):
        for i in range(self._width):
            for j in range(self._height):
                global_var.mp.matrix[j+self._posy][i+self._posx] = self._shape[j][i]

    def xget(self):
        return self._posx
    
    def yget(self):
        return self._posy


class Ball(Object):

    def __init__(self, character, x, y, lives):
        super().__init__(character, x, y)
        self._lives = 5
        self._bricks = 50
        self._score = 0

    def lives(self):
        return self._lives

    def bricks(self):
        return self._bricks

    def score(self):
        return self._score

    def red_lives(self):
        self._lives -= 1

    def red_bricks(self):
        self._bricks -= 1

    def inc_score(self):
        self._score += 10