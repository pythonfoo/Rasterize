#! /usr/bin/env python

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

    x1, y1 = p1
    x2, y2 = p2
    c = (100, 255, 100)

    if x1 == x2:
        for i in range(y1, y2):
            set_pixel(buffer, x1, i, c)
            yield
    else:
        slope = (y2 - y1) / (x2 - x1)
        y_i = y1
        for i in range(x1, x2):
            set_pixel(buffer, i, int(y_i), c)
            y_i += slope
            yield




def main():

    buffer = np.zeros((SCREENSIZE_X, SCREENSIZE_Y, 3))

    clock = pygame.time.Clock()
    
    pygame.init()
    screen = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y), 0, 32)
    pygame.display.set_caption('pygame')

    x1, y1 = random.randrange(1,SCREENSIZE_X), random.randrange(1,SCREENSIZE_Y)
    x2, y2 = random.randrange(1,SCREENSIZE_X), random.randrange(1,SCREENSIZE_Y)

    drawer = draw_line(buffer, (x1, y1), (x2, y2))
    for _ in drawer:

    # for i in range(1200):
        # clock.tick(30)
        
        # draw_line(buffer, (x1+1, y1), (x2+1, y2))
        # draw_line(buffer, (x1+2, y1), (x2+2, y2))
        
        show_screen(screen, buffer)

        buffer *= 0.98

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                return


if __name__ == '__main__':

    main()

