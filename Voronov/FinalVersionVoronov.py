from random import randint
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import datetime

start_time = datetime.datetime.now()

def get_image_pixels(filename):
    img = plt.imread(filename)
    if img.shape[-1] == 4:
        img = img[:, :, :-1]
    return img

src = get_image_pixels("wall-e.jpg")

n = len(src)
m = len(src[0])

a = [[[0, 0, float("inf")] for j in range(m)] for i in range(n)]
queue = deque()

for i in range(100000):
    x, y = randint(0, n - 1), randint(0, m - 1)
    a[x][y] = [x, y, 0]
    queue.append((x, y))
while queue:
    x, y = queue.popleft()
    x_r, y_r, z_r = a[x][y]
    sqr_z_r = (np.sqrt(z_r) + 1) ** 2
    if x + 1 < n:
        new_x = x + 1
        if y_r == y and a[new_x][y][2] > sqr_z_r:
            a[new_x][y] = [x_r, y, sqr_z_r]
            queue.append((new_x, y))
        else:
            if a[new_x][y_r][0] == x_r and a[new_x][y_r][1] == y_r:
                if a[x_r][y][0] == x_r and a[x_r][y][1] == y_r:
                    if a[new_x][y][2] > a[new_x][y_r][2] + a[x_r][y][2]:
                        a[new_x][y] = [x_r, y_r, a[new_x][y_r][2] + a[x_r][y][2]]
                        queue.append((new_x, y))
    if x - 1 > -1:
        new_x = x - 1
        if y_r == y and a[new_x][y][2] > sqr_z_r:
            a[new_x][y] = [x_r, y, sqr_z_r]
            queue.append((new_x, y))
        else:
            if a[new_x][y_r][0] == x_r and a[new_x][y_r][1] == y_r:
                if a[x_r][y][0] == x_r and a[x_r][y][1] == y_r:
                    if a[new_x][y][2] > a[new_x][y_r][2] + a[x_r][y][2]:
                        a[new_x][y] = [x_r, y_r, a[new_x][y_r][2] + a[x_r][y][2]]
                        queue.append((new_x, y))
    if y + 1 < m:
        new_y = y + 1

        if x_r == x and a[x][new_y][2] > sqr_z_r:
            a[x][new_y] = [x, y_r, sqr_z_r]
            queue.append((x, new_y))
        else:
            if a[x_r][new_y][0] == x_r and a[x_r][new_y][0] == y_r:
                if a[x][y_r][0] == x_r and a[x][y_r][1] == y_r:
                    if a[x][new_y][2] > a[x_r][new_y][2] + a[x][y_r][2]:
                        a[x][new_y] = [x_r, y_r, a[x_r][new_y][2] + a[x][y_r][2]]
                        queue.append((x, new_y))
    if y - 1 > -1:
        new_y = y - 1
        if x_r == x and a[x][new_y][2] > sqr_z_r:
            a[x][new_y] = [x, y_r, sqr_z_r]
            queue.append((x, new_y))
        else:
            if a[x_r][new_y][0] == x_r and a[x_r][new_y][0] == y_r:
                if a[x][y_r][0] == x_r and a[x][y_r][1] == y_r:
                    if a[x][new_y][2] > a[x_r][new_y][2] + a[x][y_r][2]:
                        a[x][new_y] = [x_r, y_r, a[x_r][new_y][2] + a[x][y_r][2]]
                        queue.append((x, new_y))

src = src.copy()
for i in range(len(src)):
    for j in range(len(src[0])):
        src[i, j] = src[a[i][j][0], [a[i][j][1]]]

plt.figure(figsize=(m / 100, n / 100))
plt.imshow(src, interpolation="nearest")
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.axis('off')
plt.show()

end_time = datetime.datetime.now()
total_time = end_time - start_time
print(f"Программа работала {total_time.total_seconds():.2f} секунд.")
