################################################################################
# Mandelbrot Set generator
#
# Version 0.3a
#
# Copyright (C) AgentElement
#
# MIT Licence
################################################################################


# IMPORTS:
# @numpy because numpy.
# @numba for the jit compiler responsible for speeding this up.
# @pillow (imported as PIL) to generate and manipulate each frame.
# It is assumed you have ffmpeg to stitch every frame together.
# @matplotlib and @os are used for debugging, nothing else at the moment.
import numpy as np
from numba import jit
from PIL import Image
import time
# import matplotlib
# import matplotlib.pyplot as plt
import os

# Just to know what image is being worked on.
SAVE_CTR = 0


# Saves the image in the mandelbrot_demo directory as mandelbrot_set_###.png
def save_img(image):
    global SAVE_CTR
    image.save(r"mandelbrot_demo\mandelbrot_set_{}.png".format(str(SAVE_CTR).zfill(3)))
    SAVE_CTR += 1


# Computes if a complex number z is in the set by returning the number of
# iterations z takes to diverge. max_iter is the maximum number of iterations
# allowed until z is declared to be in the set. Ideally this would be infinite,
# but memory is obviously finite. (If the number of iterations = max_iter, z is
# in the set).
@jit
def compute_mandelbrot(z: complex, max_iter):
    c = z
    for i in range(max_iter):
        if z.real * z.real + z.imag * z.imag > 4:
            return i
        z = z * z + c
    return max_iter


# Returns a 3-tuple (red, green, blue) depending on the fraction x / max_iter,
# where x is the number of iterations returned by compute_mandelbrot.
#
# The channels vary like this:
# Blue decreases as x approaches max_iter. Red increases. Green peaks when
# x / max_iter = 0.5 then decreases. All three channels follow a sinusoidal
# curve.
@jit
def colorize_sinusoidal(x, max_iter):
    if x == max_iter:
        return 0, 0, 0

    red = int(np.sin(x * np.pi / (max_iter * 2)) * 256)
    green = int(np.sin(x * np.pi / max_iter) * 256)
    blue = int(np.cos(x * np.pi / (max_iter * 2)) * 256)
    return red, green, blue


# Same as colorize_sinusoidal(), but monochromatic. Is squared as humans notice
# differences between darker colors more obviously.
@jit
def colorize_mono(x, max_iter):
    if x == max_iter:
        return 0, 0, 0

    red = int((x / max_iter) ** 2 * 256)
    blue = int((x / max_iter) ** 2 * 256)
    green = int((x / max_iter) ** 2 * 256)
    return red, green, blue


# Generates a mandelbrot set in a (x, y) numpy array with each element carrying
# the number of iterations. The array is bounded by four numbers
# (min_x, max_x, min_y, max_y) each determining the maximum and minimum
# real/imaginary values that are computed. Each element in the array directly
# corresponds to one pixel.
@jit
def generate_set(min_x, max_x, min_y, max_y, arr, iterations):
    # arr is a 2D np array containing the image.
    height = arr.shape[0]
    width = arr.shape[1]

    # This is the step value of a pixel.
    x_pixel = (max_x - min_x) / height
    y_pixel = (max_y - min_y) / width

    # computes the value for the mandelbrot set at each pixel.
    for x in range(height):
        re = min_x + x * x_pixel
        for y in range(width):
            im = min_y + y * y_pixel
            z = complex(re, im)
            mandelbrot_item = compute_mandelbrot(z, iterations)
            arr[x, y] = mandelbrot_item
    return arr


# Takes a resolution and generates the four bounding numbers used by
# generate_set(). The image will be focused around the focus parameter, and will
# be zoomed in by a factor of zoom/12. By default, this generates a 4K image.
@jit
def range_from_resolution(resolution=(3840, 2160), zoom=1, focus=0 + 0j):
    max_x_pixel, max_y_pixel = resolution[0], resolution[1]

    # the buffer zone is an area added to either side of an image to account for
    # a deviation from a perfect square, as is the norm for most modern screens.
    buffer_zone = 2 * (max_x_pixel - max_y_pixel) / max_y_pixel

    # The zoom value is divided by 12. This means that the image will double in
    # size every 12 frames. At 24 fps, the image will zoom in by a factor of 4
    # every second.
    scaled_zoom = zoom / 12

    min_x = ((-2.0 - buffer_zone) / 2 ** scaled_zoom + focus.real)
    max_x = ((2.0 + buffer_zone) / 2 ** scaled_zoom + focus.real)
    min_y = (-2.0 / 2 ** scaled_zoom + focus.imag)
    max_y = (2.0 / 2 ** scaled_zoom + focus.imag)

    return min_x, max_x, min_y, max_y


# This is a wrapper function that generates the numpy array and turns it into a
# colorized image.
@jit
def generate_image(resolution=(1920, 1080), zoom=1, focus=0 + 0j, iterations=256):
    image_array = np.empty(resolution, dtype=np.uint16)
    image = Image.new("RGB", resolution)

    image_array = generate_set(*range_from_resolution(resolution, zoom, focus), image_array, iterations)
    # -2.0, 1.0, -1.25, 1.25
    for x in range(resolution[1]):
        for y in range(resolution[0]):
            # Switch  colorize_sinusoidal() for colorize_mono()  here for a
            # monochromatic image.
            image.putpixel((y, x), colorize_sinusoidal(image_array[y][x], iterations))

    return image


@jit
def main():
    # Littered with debug code at the moment
    curr_time = time.time()
    # -0.761574 + -0.0847596j
    # 100000
    focus = -0.761574 + -0.0847596j
    image = generate_image((1920, 1080), np.log2(100000) * 12, focus, 1024)
    image.show()
    save_img(image)
    # convert_to_video()
    print("Mandelbrot set zoom at {} generated in {} seconds".format(focus, time.time() - curr_time))


def convert_to_video():
    pass
    # ffmpeg -framerate 24 -i mandelbrot_set_%03d.png mandelbrot_zoom.mp4


if __name__ == '__main__':
    main()
