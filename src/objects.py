import math

class Shape(object):
    def __init__(self, position):
        self.position = position
        

class Ball(Shape):
    
    def __init__(self, radius, centre):
        self.radius = radius
        super(Ball, self).__init__(centre)