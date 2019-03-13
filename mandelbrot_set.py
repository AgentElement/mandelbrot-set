import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from PIL import Image
import time

save_ctr = 0


def save_img(fig):
    global save_ctr
    save_ctr += 1
    fig.savefig("mandelbrot_set_{}.png".format(save_ctr))


@jit
def compute_mandelbrot(z: complex, max_iter):
    c = z
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4:
            return i
        z = z * z + c
    return max_iter


@jit
def colorize_sinusoidal(x, max_iter):
    if x == max_iter:

        return 0, 0, 0
    red = int(np.sin(x * np.pi / (max_iter * 2)) * 256)
    green = int(np.sin(x * np.pi / max_iter) * 256)
    blue = int(np.cos(x * np.pi / (max_iter * 2)) * 256)
    return red, green, blue


@jit
def colorize_mono(x, max_iter):
    if x == max_iter:
        return 0, 0, 0

    red = int((x / max_iter) ** 2 * 256)
    blue = int((x / max_iter) ** 2 * 256)
    green = int((x / max_iter) ** 2 * 256)
    return red, green, blue


@jit
def generate_set(min_x, max_x, min_y, max_y, arr, itr):
    # arr is a 2D np array containing the image
    height = arr.shape[0]
    width = arr.shape[1]

    x_pixel = (max_x - min_x) / width
    y_pixel = (max_y - min_y) / height

    for x in range(width):
        re = min_x + x * x_pixel
        for y in range(height):
            im = min_y + y * y_pixel
            z = complex(re, im)
            mandelbrot_item = compute_mandelbrot(z, itr)
            arr[y, x] = mandelbrot_item
    return arr


@jit
def range_from_resolution(resolution=(3840, 2160), zoom=1, focus=0 + 0j):
    max_x_pixel, max_y_pixel = resolution[0], resolution[1]
    buffer_zone = 2 * (max_x_pixel - max_y_pixel) / max_y_pixel

    min_x = ((-2.0 - buffer_zone) / zoom + focus.real)
    max_x = ((2.0 + buffer_zone) / zoom + focus.real)
    min_y = (-2.0 / zoom + focus.imag)
    max_y = (2.0 / zoom + focus.imag)

    return min_x, max_x, min_y, max_y


@jit
def generate_image(resolution=(1920, 1080), zoom=1, focus=0+0j, iter=256):
    image_array = np.empty(resolution[::-1], dtype=np.uint16)
    image = Image.new("RGB", resolution)

    image_array = generate_set(*range_from_resolution(resolution, zoom, focus), image_array, iter)
    # -2.0, 1.0, -1.25, 1.25
    for x in range(resolution[1]):
        for y in range(resolution[0]):
            image.putpixel((y, x), colorize_sinusoidal(image_array[x][y], iter))

    return image


def main():
    curtime = time.time()
    # -0.761574 + -0.0847596j
    image = generate_image((1920 * 2, 1080 * 2), 100000, -0.761574 + -0.0847596j, 1024)
    image.save("temp.bmp")
    print(time.time() - curtime)


if __name__ == '__main__':
    main()
