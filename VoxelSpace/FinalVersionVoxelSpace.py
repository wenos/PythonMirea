import pygame as pg
from numba import njit
import numpy as np
import sys

pg.init()
image = pg.image.load('Map0.png')
colormap = pg.surfarray.array3d(image)
image = pg.image.load('noise3.png')
heightmap = pg.surfarray.array2d(image)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALE = 400
camera = {
    "x"       : 792,
    "y"       : 32,
    "zfar"    : 1000,
    "height"  : 200,
    "angle"   : 1.5 * np.pi,
    "horizon" : 100
}

screen_array = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


@njit(fastmath=True)
def upd(x, y, zfar, height, angle, screen, horizon):
    screen[:] = np.array([0, 0, 0])
    sinangle = np.sin(angle)
    cosangle = np.cos(angle)

    plx = cosangle * zfar + sinangle * zfar
    ply = sinangle * zfar - cosangle * zfar

    prx = cosangle * zfar - sinangle * zfar
    pry = sinangle * zfar + cosangle * zfar
    for i in range(0, SCREEN_WIDTH):
        delta_x = (plx + (prx - plx) / SCREEN_WIDTH * i) / zfar
        delta_y = (ply + (pry - ply) / SCREEN_WIDTH * i) / zfar
        rx = x
        ry = y
        max_height = SCREEN_HEIGHT
        for z in range(1, zfar):
            rx += delta_x
            ry += delta_y
            proj_height = int((height - heightmap[int(rx) & 1023][(SCREEN_HEIGHT - int(ry)) & 1023]) / z * SCALE) + horizon
            if (proj_height < 0):
                proj_height = 0
            if proj_height > SCREEN_HEIGHT:
                proj_height = SCREEN_HEIGHT
            if proj_height < max_height:
                for y1 in range(proj_height, max_height):
                    screen[i][y1] = colormap[int(rx) & 1023][(SCREEN_HEIGHT - int(ry)) & 1023]
                max_height = proj_height
    return screen

screen = np.full((SCREEN_WIDTH, SCREEN_HEIGHT, 3), [0, 0, 0])

while True:
    pressed_key = pg.key.get_pressed()
    if pressed_key:
        if pressed_key[pg.K_UP]:
            camera["y"] += np.sin(camera["angle"])
            camera["x"] += np.cos(camera["angle"])
        if pressed_key[pg.K_DOWN]:
            camera["y"] -= np.sin(camera["angle"])
            camera["x"] -= np.cos(camera["angle"])
        if pressed_key[pg.K_z]: camera["height"] += 1
        if pressed_key[pg.K_x]: camera["height"] -= 1
        if pressed_key[pg.K_LEFT]: camera["angle"] -= 0.01
        if pressed_key[pg.K_RIGHT]: camera["angle"] += 0.01
        if pressed_key[pg.K_w]: camera["horizon"] += 10
        if pressed_key[pg.K_s]: camera["horizon"] -= 10
        screen_array.blit(pg.surfarray.make_surface(
            upd(camera["x"], camera["y"], camera["zfar"], camera["height"],
                camera["angle"], screen, camera["horizon"])), (0, 0))
        pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()