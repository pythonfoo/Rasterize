def work(screen, buffer):

    step8(buffer, screen)
    show_screen(screen, buffer)
    wait()


def step0(buffer):
    """Simply draw the lines on the screen."""

    # oops, too many coordinates
    for (p1, c1), (p2, c2) in get_cube():
        draw_line(buffer, (p1, c1), (p2, c2))


def step1(buffer):
    """Simply draw the lines on the screen, forgetting z coordinates."""

    for (p1_v3, c1), (p2_v3, c2) in get_cube():
        p1 = p1_v3[0], p1_v3[1], c1
        p2 = p2_v3[0], p2_v3[1], c2

        draw_line(buffer, p1, p2)


def step2(buffer):
    """Simply draw the lines on the screen, forgetting z coordinates, and scaling up."""

    for (p1_v3, c1), (p2_v3, c2) in get_cube():
        p1 = p1_v3[0]*100, p1_v3[1]*100, c1
        p2 = p2_v3[0]*100, p2_v3[1]*100, c2

        draw_line(buffer, p1, p2)


def step3(buffer):
    """Simply draw the lines on the screen, forgetting z coordinates, and scaling up and moving somewhere."""

    for (p1_v3, c1), (p2_v3, c2) in get_cube():
        p1 = p1_v3[0]*100+100, p1_v3[1]*100+100, c1
        p2 = p2_v3[0]*100+100, p2_v3[1]*100+100, c2

        draw_line(buffer, p1, p2)


def step4(buffer):
    """Do some transformation, then draw on the screen"""

    for (p1, c1), (p2, c2) in get_cube():
        scale = vec3(100, 100, 100)
        move = vec3(100, 100, 100)
        p1 = move + scale * p1
        p2 = move + scale * p2
        draw_line_3d(buffer, (p1, c1), (p2, c2))


def step5(buffer):
    """Now do it in matrix form."""

    scale = np.array([[100, 0, 0, 0],
                    [0, 100, 0, 0],
                    [0, 0, 100, 0],
                    [0, 0, 0, 1],
                    ])
    move = np.array([[1, 0, 0, 1],
                    [0, 1, 0, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1],
                    ])

    scalemove = scale @ move

    for (p1, c1), (p2, c2) in get_cube():
        p1 = scale @ move @ p1
        p2 = scalemove @ p2
        draw_line_3d(buffer, (p1, c1), (p2, c2))


def step6(buffer):
    """Now do it in matrix form with the p parameter."""

    scale = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 100],
                    ])
    move = np.array([[1, 0, 0, 1],
                    [0, 1, 0, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1],
                    ])

    mat = scale @ move

    for (p1, c1), (p2, c2) in get_cube():
        p1 = rectify(mat @ p1)
        p2 = rectify(mat @ p2)
        draw_line_3d(buffer, (p1, c1), (p2, c2))


def step7(buffer):
    """Finally, projection!"""

    scale = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 100],
                    ])
    move = np.array([[1, 0, 0, 1],
                    [0, 1, 0, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1],
                    ])
    project = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0.1, 1],
                    ])

    mat = scale @ move @ project

    for (p1, c1), (p2, c2) in get_cube():
        p1 = rectify(mat @ p1)
        p2 = rectify(mat @ p2)
        draw_line_3d(buffer, (p1, c1), (p2, c2))


def step7a(buffer, screen):
    """Finally, projection!"""

    for i in range(180000):
        p = (1.2 + math.sin(i / 180 * 3.1415926))/2
        print(p)

        mat1 = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 100],
                        ])
        mat2 = np.array([[1, 0, 0, 1],
                        [0, 1, 0, 1],
                        [0, 0, 1, 1],
                        [0, 0, 0, 1],
                        ])
        mat3 = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, p/3, 1],
                        ])

        mat = mat1 @ mat2 @ mat3

        for (p1, c1), (p2, c2) in get_cube():
            p1 = rectify(mat @ p1)
            p2 = rectify(mat @ p2)
            draw_line_3d(buffer, (p1, c1), (p2, c2))
        show_screen(screen, buffer)
        buffer = np.zeros((SCREENSIZE_X, SCREENSIZE_Y, 3))

def step8(buffer, screen):
    """Finally, projection!"""

    for i in range(180000):
        angle = i / 180 * 3.1415926

        screenmove = np.array([[1, 0, 0, 0.02],
                        [0, 1, 0, 0.014],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                        ])
        scale = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 20],
                        ])
        move = np.array([[1, 0, 0, -0.5],
                        [0, 1, 0, -0.5],
                        [0, 0, 1, 7],
                        [0, 0, 0, 1],
                        ])
        project = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0.7, 1],
                        ])

        sin = math.sin
        cos = math.cos

        m1 = np.array([[1, 0, 0, -0.5],
                        [0, 1, 0, 0],
                        [0, 0, 1, -0.5],
                        [0, 0, 0, 1],
                        ])

        rot = np.array([[cos(angle), 0, -sin(angle), 0],
                        [0, 1, 0, 0],
                        [sin(angle), 0, cos(angle), 0],
                        [0, 0, 0, 1],
                        ])
        m2 = np.array([[1, 0, 0, 0.5],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0.5],
                        [0, 0, 0, 1],
                        ])

        rotm = m2 @ rot @ m1

        mat = screenmove @ (scale @ project @ move) @ rotm

        for (p1, c1), (p2, c2) in get_cube():
            p1 = rectify(mat @ p1)
            p2 = rectify(mat @ p2)
            draw_line_3d(buffer, (p1, c1), (p2, c2))
        show_screen(screen, buffer)
        buffer = np.zeros((SCREENSIZE_X, SCREENSIZE_Y, 3))




def get_cube():

    p = [
        (vec3(0, 0, 0), (50, 50, 50)),
        (vec3(1, 0, 0), (100, 50, 50)),
        (vec3(1, 0, 1), (100, 50, 100)),
        (vec3(0, 0, 1), (50, 50, 100)),
        (vec3(0, 1, 0), (50, 100, 50)),
        (vec3(1, 1, 0), (100, 100, 50)),
        (vec3(1, 1, 1), (100, 100, 100)),
        (vec3(0, 1, 1), (50, 100, 100)),
    ]
    lines = [
        (p[0], p[1]), (p[1], p[2]), (p[2], p[3]), (p[3], p[0]),
        (p[4], p[5]), (p[5], p[6]), (p[6], p[7]), (p[7], p[4]),
        (p[0], p[4]), (p[1], p[5]), (p[2], p[6]), (p[3], p[7]),
    ]

    return lines

def vec3(x, y, z):
    return np.array([x, y, z, 1])


def rectify(v):
    s = v[3]

    return vec3(v[0] * s, v[1] * s, v[2] * s)






########################################################################################################################
# the boring drawing stuff again
# region: boring stuff


import time

import math

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
        buffer[x, y] = c


def draw_line_3d(buffer, p1, p2):

    v1, c1 = p1
    v2, c2 = p2

    p1 = int(v1[0]), int(v1[1]), c1
    p2 = int(v2[0]), int(v2[1]), c2
    if v2[0] < v1[0]:
        p1, p2 = p2, p1

    draw_line(buffer, p1, p2)


def draw_line(buffer, p1, p2):

    # print((p1, p2))

    x1, y1, c1 = p1
    x2, y2, c2 = p2

    if x1 == x2:
        if y1 == y2:
            print("invalid line: {} -> {}".format(p1, p2))
            return
        y_range = (y2 - y1)
        slope_r = (c2[0] - c1[0]) / y_range
        slope_g = (c2[1] - c1[1]) / y_range
        slope_b = (c2[2] - c1[2]) / y_range

        r_i, g_i, b_i = c1
        for i in range(y1, y2):
            set_pixel(buffer, x1, i, (int(r_i), int(g_i), int(b_i)))
            r_i, g_i, b_i = r_i + slope_r, g_i + slope_g, b_i + slope_b
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


def wait():
    while True:
        event = pygame.event.wait()
        if event.type == QUIT or event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            return

def main():
    clock = pygame.time.Clock()

    pygame.init()

    buffer = np.zeros((SCREENSIZE_X, SCREENSIZE_Y, 3))

    screen = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y), 0, 32)
    pygame.display.set_caption('pygame')

    work(screen, buffer)
    # wait()

# endregion


if __name__ == '__main__':
    main()
