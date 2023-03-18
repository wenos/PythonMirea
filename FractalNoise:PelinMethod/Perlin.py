import random
import math
def noise(x, y, seed):
    n = int(x) + int(y) * 57 + seed
    n = (n << 13) ^ n
    t = (n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff
    return 1.0 - float(t) * 0.931322574615478515625e-9


def smooth_noise(x, y, seed):
    corners = (noise(x-1, y-1, seed)+noise(x+1, y-1, seed)+noise(x-1, y+1, seed)+noise(x+1, y+1, seed))/16
    sides   = (noise(x-1, y, seed)  +noise(x+1, y, seed)  +noise(x, y-1, seed)  +noise(x, y+1, seed))  /  8
    center  =  noise(x, y,seed) / 4
    return corners + sides + center

def interpolated_noise(x, y, seed):
    integer_X = int(x)
    fractional_X = x - integer_X

    integer_Y = int(y)
    fractional_Y = y - integer_Y

    v1 = smooth_noise(integer_X,     integer_Y, seed)
    v2 = smooth_noise(integer_X + 1, integer_Y, seed)
    v3 = smooth_noise(integer_X,     integer_Y + 1, seed)
    v4 = smooth_noise(integer_X + 1, integer_Y + 1, seed)

    i1 = interpolate(v1 , v2 , fractional_X)
    i2 = interpolate(v3 , v4 , fractional_X)

    return interpolate(i1 , i2 , fractional_Y)

def interpolate(a, b, x):
    ft = x * 3.1415927
    f = (1.0 - math.cos(ft)) * 0.5
    return  a*(1.0-f) + b*f



from PIL import Image
import random

def generate_noise_image(width, height, scale):
    seed = random.randint(0, 1000000)
    image = Image.new("L", (width, height))
    for y in range(height):
        for x in range(width):
            noise_value = 0
            frequency = 1 / scale
            amplitude = 1
            for _ in range(9):
                noise_value += interpolated_noise(x * frequency, y * frequency, seed) * amplitude
                frequency *= 2
                amplitude *= 0.5
            noise_value = int((noise_value + 1) * 127.5)
            image.putpixel((x, y), noise_value)
    return image

image1 = generate_noise_image(1024, 1024, 32)
image1.save("noise3.png")

image2 = generate_noise_image(1024, 1024, 32)
image2.save("noise4.png")









