#! /usr/bin/env python

from time import sleep

import pygame
from pygame import surfarray
from pygame.locals import *
import numpy as np
import random

SCREENSIZE = (640, 480)
SCREENSIZE_X, SCREENSIZE_Y = SCREENSIZE


def show_screen(screen, screen_buffer):

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

