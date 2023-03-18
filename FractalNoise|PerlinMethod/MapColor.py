from PIL import Image
import random
import pygame as pg

pg.init()
image = pg.image.load('noise1.png')
heightmap = pg.surfarray.array2d(image)
image = pg.image.load('noise2.png')
watermap = pg.surfarray.array2d(image)
print(watermap)
print(heightmap)
map = {
    "BEACH": (248, 216, 184),
    "SCORCHED": (85, 85, 85),
    "BARE": (136, 136, 136),
    "TUNDRA": (221, 221, 255),
    "SNOW": (255, 255, 255),
    "TEMPERATE_DESERT": (210, 180, 140),
    "SHRUBLAND": (196, 204, 176),
    "GRASSLAND": (193, 209, 160),
    "TEMPERATE_RAIN_FOREST": (47, 111, 72),
    "SUBTROPICAL_DESERT": (201, 190, 185),
    "TROPICAL_SEASONAL_FOREST": (148, 194, 106),
    "TROPICAL_RAIN_FOREST": (0, 117, 94),
    "TEMPERATE_DECIDUOUS_FOREST": (50, 205, 50),
    "TAIGA": (0, 102, 51),
    "OCEAN": (0, 0, 128)
}
def lerp_color(color1, color2, t):
    r = int(color1[0] * (1 - t) + color2[0] * t)
    g = int(color1[1] * (1 - t) + color2[1] * t)
    b = int(color1[2] * (1 - t) + color2[2] * t)
    return (r, g, b)


def biome(e, m):
    if (e < 0.1):
        return map["OCEAN"]
    if (e < 0.12):
        return map["BEACH"]

    if (e > 0.8):
        if (m < 0.1):
            return map["SCORCHED"]
        if (m < 0.2):
            return map["BARE"]
        if (m < 0.5):
            return map["TUNDRA"]
        if (m < 0.8):
            return lerp_color(map["TUNDRA"], map["SNOW"], (m - 0.5) / 0.3)
        return map["SNOW"]

    if (e > 0.6):
        if (m < 0.33):
            return map["TEMPERATE_DESERT"]
        if (m < 0.66):
            return map["SHRUBLAND"]
        if (m < 0.8):
            return lerp_color(map["SHRUBLAND"], map["TAIGA"], (m - 0.66) / 0.14)
        return map["TAIGA"]

    if (e > 0.3):
        if (m < 0.16):
            return map["TEMPERATE_DESERT"]
        if (m < 0.33):
            return lerp_color(map["TEMPERATE_DESERT"], map["GRASSLAND"], (m - 0.16) / 0.17)
        if (m < 0.5):
            return lerp_color(map["GRASSLAND"], map["TEMPERATE_DECIDUOUS_FOREST"], (m - 0.33) / 0.17)
        if (m < 0.66):
            return lerp_color(map["TEMPERATE_DECIDUOUS_FOREST"], map["TEMPERATE_RAIN_FOREST"], (m - 0.5) / 0.16)
        return map["TEMPERATE_RAIN_FOREST"]
    if (m < 0.16): return map["SUBTROPICAL_DESERT"]
    if (m < 0.33): return map["GRASSLAND"]
    if (m < 0.66): return map["TROPICAL_SEASONAL_FOREST"]
    return map["TROPICAL_RAIN_FOREST"]

width = height = 1024
image = Image.new("RGB", (width, height))
for y in range(height):
    for x in range(width):
        e, m =heightmap[x][y] / 255, watermap[x][y] / 255
        image.putpixel((x, y), biome(e, m))
image.save("Map0.png")
