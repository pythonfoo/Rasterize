#! /usr/bin/env python
"""
Drawing stuff
or: the power of linear interpolation
or: all the edge cases

In this module we'll learn how lines, polygons and filled polygons are drawn on the screen. We will do so from a very
high/abstract standpoint. We're not interested in making things fast, only in making them correct and understandable.

As such, we will not be using the [Bresenham algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm),
even though I encourage you to read and understand that, too.

The end goal of this file/lesson is to draw a filled triangle on the screen.
Read the source code for an in-depth explanation. There will be exercises in there, marked with "EX:". I encourage you
to try them out and play with them, until you find an answer.
"""

# See below for Part 0: pixels
# it's a boring part, so we'll move it to the end and simply not look at it.

########################################################################################################################
# Part 1: lines
"""
The first thing we need to achieve to do so is to get single pixels drawn on the screen. Once we have that, we can
compose these pixels to lines. Lines can be composed into triangles and triangles, finally, can be filled.
All of this will be achieved through the power of linear interpolation.

Linear interpolation is the process of going from one value to another value at linear speed. For example, let's say
you are at x = 0 and want to go to x = 5, with constant "speed", and you want to do so in one time unit. The question
then becomes: given a time `t`, between 0 and 1, at which point `x(t)` will you be? In our specific case, it should be
clear that `x(t) = 5 * t`.
So let's solve the general case: given a starting position x_0 and a stopping position x_1, what is x(t) for t in
[0, 1]? The answer is a simple linear interpolation:
  x(t) = x_0 + t * (x_1 - x_0)
As a python function, it could look like this:
"""
def lerp(x_0, x_1, t):
    return x_0 + t * (x_1 - x_0)
"""
That's nice, but not enough. We want to go from x_0 to x_1 not in one time unit, but between the times y_0 and y_1. To
get there we'll need to interpolate between y_0 and y_1 as well. Let's also assume that all numbers involved are
integers and we want to go integer steps. Then a function that gave us a list of all "steps" could look like this:
"""
def lerp(x_0, x_1, y_0, y_1):
    """Go from (x0, y0) to (x1, y1) in integer steps ofer y0 -> y1."""
    # we are going to take this many steps:
    steps = y_1 - y_0
    # and we need to divide the target difference (x_1 - x_0) in this many steps:
    slope = (x_1 - x_0) / steps
    # this is a floating point number, and that's ok. We'll need to take care to round our emitted values!

    # x_i and y_i will be our running variables
    # We'll start at x_i = x_0 and y_i = y_0
    x_i = x_0
    for y_i in range(y_0, y_1 + 1):
        x_i += slope                    # this will now also be a float, and we still cannot round. EX: Why not?
        yield (int(x_i), y_i)           # this is our step result. EX: Why do we not need to convert y_i to int?

# TODO: continue



from time import sleep

import pygame
from pygame import surfarray
from pygame.locals import *
import numpy as np
import random

SCREENSIZE = (640, 480)
SCREENSIZE_X, SCREENSIZE_Y = SCREENSIZE


def show_screen(screen, screen_buffer):
    """Just a convenience function for showing a numpy buffer on the screen."""

    surfarray.blit_array(screen, screen_buffer)
    pygame.display.flip()

    
def set_pixel(buffer, x, y, c):
    if 0 <= x < SCREENSIZE_X and 0 <= y <= SCREENSIZE_Y:
        buffer[x,y] = c

    
def draw_line(buffer, p1, p2):

    x1, y1, c1 = p1
    x2, y2, c2 = p2

    
    if x1 == x2:
        y_range = (y2 - y1)
        slope_r = (c2[0] - c1[0]) / y_range
        slope_g = (c2[1] - c1[1]) / y_range
        slope_b = (c2[2] - c1[2]) / y_range

        r_i, g_i, b_i = c1
        for i in range(y1, y2):
            set_pixel(buffer, x1, i, (int(r_i), int(g_i), int(b_i)))
            r_i, g_i, b_i = r_i + slope_r, g_i + slope_g, b_i + slope_b
            yield x1, i, (r_i, g_i, b_i)
    else:
        x_range = (x2 - x1)
        slope = (y2 - y1) / x_range
        slope_r = (c2[0] - c1[0]) / x_range
        slope_g = (c2[1] - c1[1]) / x_range
        slope_b = (c2[2] - c1[2]) / x_range

        y_i = y1
        r_i, g_i, b_i = c1
        for i in range(x1, x2):
            set_pixel(buffer, i, int(y_i), (int(r_i), int(g_i), int(b_i)))
            y_i += slope
            r_i, g_i, b_i = r_i + slope_r, g_i + slope_g, b_i + slope_b
            yield (i, int(y_i), (r_i, g_i, b_i))
            

def linedraw(screen, buffer, p1, p2):
    
    print((p1, p2))
    input("ready?")
    
    drawer = draw_line(buffer, p1, p2)
    for _ in drawer:

        show_screen(screen, buffer)
        sleep(0.01)

    buffer *= .5

def linedraw_two(screen, buffer, p1, p2, q1, q2):
    
    print((p1, p2))
    print(" and")
    print((q1, q2))
    # input("ready?")
    
    drawer1 = draw_line(buffer, p1, p2)
    drawer2 = draw_line(buffer, q1, q2)
    for px, py, pc in drawer1:
        qx, qy, qc = next(drawer2)

        for _ in draw_line(buffer, (px, py, pc), (qx, qy, qc)):
            pass
        
        # show_screen(screen, buffer)
        # sleep(0.01)

    show_screen(screen, buffer)
    buffer *= .5

    
    
def main():

    clock = pygame.time.Clock()
    
    pygame.init()

    buffer = np.zeros((SCREENSIZE_X, SCREENSIZE_Y, 3))

    screen = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y), 0, 32)
    pygame.display.set_caption('pygame')

    # linedraw(screen, buffer, (10, 400, (0,0,255)), (400, 10, (255, 0, 0)))
    # linedraw(screen, buffer, (10, 400), (400, 100))
    # linedraw(screen, buffer, (10, 400), (400, 200))
    # linedraw(screen, buffer, (10, 400), (400, 300))
    # linedraw(screen, buffer, (10, 400), (400, 400))

    # input("now the other way!")

    # linedraw(screen, buffer, (10, 400), (300, 10))
    # linedraw(screen, buffer, (10, 400), (200, 10))
    # linedraw(screen, buffer, (10, 400), (100, 10))
    # linedraw(screen, buffer, (10, 400), (90, 10))
    # linedraw(screen, buffer, (10, 400), (50, 10))
    # linedraw(screen, buffer, (10, 400), (40, 10))
    # linedraw(screen, buffer, (10, 400), (30, 10))
    # linedraw(screen, buffer, (10, 400), (20, 10))
    # linedraw(screen, buffer, (10, 400), (10, 10))

    linedraw_two(screen, buffer,
                 (10, 230, (1,1,100)), (400, 10, (1,100,1)),
                 (10, 230, (0,0,255)), (400, 460, (255,0,0)))
    # linedraw(screen, buffer, (400, 10), (400, 460))
    
    # input("done")

    

if __name__ == '__main__':

    main()

