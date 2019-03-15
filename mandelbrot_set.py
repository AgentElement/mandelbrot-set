# import matplotlib
# import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from PIL import Image
import time
import os

save_ctr = 0


def save_img(image):
    global save_ctr
    image.save(r"mandelbrot\mandelbrot_set_{}.png".format(str(save_ctr).zfill(3)))
    save_ctr += 1


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
def generate_set(min_x, max_x, min_y, max_y, arr, iterations):
    # arr is a 2D np array containing the image
    height = arr.shape[0]
    width = arr.shape[1]

    x_pixel = (max_x - min_x) / height
    y_pixel = (max_y - min_y) / width

    for x in range(height):
        re = min_x + x * x_pixel
        for y in range(width):
            im = min_y + y * y_pixel
            z = complex(re, im)
            mandelbrot_item = compute_mandelbrot(z, iterations)
            arr[x, y] = mandelbrot_item
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
def generate_image(resolution=(1920, 1080), zoom=1, focus=0+0j, iterations=256):
    image_array = np.empty(resolution, dtype=np.uint16)
    image = Image.new("RGB", resolution)

    image_array = generate_set(*range_from_resolution(resolution, zoom, focus), image_array, iterations)
    # -2.0, 1.0, -1.25, 1.25
    for x in range(resolution[1]):
        for y in range(resolution[0]):
            image.putpixel((y, x), colorize_sinusoidal(image_array[y][x], iterations))

    return image


@jit
def main():
    curtime = time.time()
    # -0.761574 + -0.0847596j
    # 100000
    focus = -0.761574 + -0.0847596j
    for i in range(0, 180):
        image = generate_image((1920, 1080), i, focus, 512)
        save_img(image)
    # convert_to_video()
    print("Mandelbrot set zoom at {} generated in {} seconds".format(focus, time.time() - curtime))


def convert_to_video():
    pass


if __name__ == '__main__':
    main()
