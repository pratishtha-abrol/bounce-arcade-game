import board
import objects
import env 

mp = board.Map()

TIME_REM = 0
SCORE = 0

bounce = objects.Ball(env.ball, 0, mp.height - len(env.ball) - 1, env.lives)