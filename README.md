# bounce-arcade-game
a terminal based game built in python with OOPS concepts

## Libraries used
> Numpy
> Colorama
> Os
> Time
> Random
> Select
> Sys
> Terminos
> Atexit

## Keyboard Controls:
> - "a" : moves left
> - "d" : moves right
> - " " : release ball in case of paddle grab boost
> - "p" : skip level

## Boosts:

Note that each boost, except the ball multiplier functions for exactly 10 seconds, after which the game state neutralises.

- Ball Multiplier:
    Multiplies the number of balls already present on screen, the main ball retaind white colour, losing this will result in loss of a life. The other balls stay on screen as long as they do not pass the paddle possition

- Fast Ball:
    Makes the speed of the ball in y direction twice the original, thus increasing the speed

- Thru ball:
    Allows ball to break bricks and pass through them, irrespective of the strength

- Paddle Grab:
    Sticks the ball to the paddle on collision, allows to position, and releases on pressing " ". The released ball follows the trajectory it would have had it not been grabbed.

- Expand and Shrink Paddle:
    Increase and decrease paddle length by 4, respectively

- Paddle Shoot:
    Allows paddle to shoot bullets

## Levels:

3 levels. The last level is the super level. Press 'p' to skip levels.

## Exploding Bricks:

Some bricks on the screen may explode on collision, breaking those directlt adjacent to it.

## Falling bricks:

Bricks fall one unit down every 10 seconds into the game. Reset on level completion

## Collision rules:

The ball changes position depending on the place of colision, how far it is from the center of the object it is colliding with.
Bricks with strength 3, blue, require 3 hits to break, the ones with strength 2, green, require 2 and the magenta ones require just 1.
The unbreakable bricks, the white ones, will not break, irrespective of the number of hits, and can be broken only by an exploding brick.