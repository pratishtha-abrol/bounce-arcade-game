import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# class Shape():

#     def __init__(self, position):
#         self.position = position


# class Ball(Shape):

#     def __init__(self, radius, centre):
#         self.radius = radius
#         super(Ball, self).__init__(centre)


# c1 = Ball(1.0, (0.5, 1.0))
# c2 = Ball(1.5, (-0.5, 2.0))
# c3 = Ball(0.5, (0,0))


# bounds of the room
xlim = (0,30)
ylim = (1,20)

# position of the ball
xy = np.array((3.0,18.0))
# velocity of the ball
v = np.array((0,0.3))

delta_t = 0.001

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=xlim, ylim=ylim)
ax.grid()

scatter, = ax.plot([], [], 'o', color='green', markersize=20)


def init():
    return []

def animate(t):
    # t is time in seconds
    global xy, v
    
    if xy[0] <= xlim[0]:
        # hit the left wall, reflect x component
        v[0] = np.abs(v[0])
        
    elif xy[0] >= xlim[1]:
        v[0] = - np.abs(v[0])
        
    if xy[1] <= ylim[0]:
        v[1] = np.abs(v[1])
        
    elif xy[1] >= ylim[1]:
        v[1] = - np.abs(v[1])
    
    # delta t is 0.1
    delta_v = delta_t 
    v += delta_v
    
    xy += v
    
    xy[0] = np.clip(xy[0], xlim[0], xlim[1])
    xy[1] = np.clip(xy[1], ylim[0], ylim[1])

    scatter.set_data(xy)
    # have to return an iterable
    return scatter,

# interval in milliseconds
# we're watching in slow motion (delta t is shorter than interval)
ani = animation.FuncAnimation(fig, animate, np.arange(0,100,delta_t), init_func=init, interval=10, blit=True)

plt.show()