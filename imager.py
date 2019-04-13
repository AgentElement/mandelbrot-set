import numpy as np
from PIL import Image
from numba import jit
from generator import Generator
import sys


class Imager:

    def __init__(self, generator: Generator):
        self.__generator = generator
        self.__save_ctr = 0

    def __repr__(self):
        return "<Imager: " + repr(self.__generator) + ">"

    def __str__(self):
        return repr(self)

    # Returns a 3-tuple (red, green, blue) depending on the fraction x/max_iter,
    # where x is the number of iterations returned by compute_mandelbrot.
    #
    # The channels vary like this:
    # Blue decreases as x approaches max_iter. Red increases. Green peaks when
    # x/max_iter = 0.5 then decreases. All three channels follow a sinusoidal
    # curve.
    @staticmethod
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
    @staticmethod
    @jit
    def colorize_mono(x, max_iter):
        if x == max_iter:
            return 0, 0, 0

        red = int((x / max_iter) ** 2 * 256)
        blue = int((x / max_iter) ** 2 * 256)
        green = int((x / max_iter) ** 2 * 256)
        return red, green, blue

    # This is a wrapper function that generates the numpy array and turns it
    # into a colorized image. Returns the image as a byte array.
    @jit
    def generate_image(self, zoom, color_type='sin'):
        resolution = self.__generator.resolution
        iterations = self.__generator.iterations
        image = Image.new("RGB", resolution)
        self.__generator.generate(zoom)
        image_array = self.__generator.arr

        color_function = None

        if color_type == 'sin':
            color_function = self.colorize_sinusoidal
        elif color_type == 'mono':
            color_function = self.colorize_mono

        # -2.0, 1.0, -1.25, 1.25
        for x in range(resolution[1]):
            for y in range(resolution[0]):
                image.putpixel((y, x), color_function(image_array[y][x], iterations))

        return image

    # Saves the image in the mandelbrot_demo directory as mandelbrot_set_###.png
    def save_image(self, image):
        image.save(r"mandelbrot_demo\mandelbrot_set_{}.png".format(str(self.__save_ctr).zfill(3)))
        self.__save_ctr += 1

