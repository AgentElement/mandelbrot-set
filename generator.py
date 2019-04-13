import numpy as np
from numba import jit


class Generator:

    def __init__(self, resolution=(1920, 1080), focus=0 + 0j, framerate=24, speed=2, iterations=256):
        self.resolution = resolution
        self.focus = focus
        self.speed = speed
        self.framerate = framerate
        self.iterations = iterations
        self.arr = np.zeros(resolution, dtype=np.uint16)

    def __repr__(self):
        return "<mandelbrot_generator res: {}, focus: {}, framerate: {}, speed: {}, iterations: {}>".format(
            self.resolution, self.focus, self.framerate, self.speed, self.iterations)

    def __str__(self):
        return self.__repr__()

    # Computes if a complex number z is in the set by returning the number of
    # iterations z takes to diverge. max_iter is the maximum number of
    # iterations allowed until z is declared to be in the set. Ideally this
    # would be infinite, but memory is obviously finite. (If the number of
    # iterations = max_iter, z is in the set).
    @staticmethod
    @jit
    def compute_mandelbrot(z: complex, max_iter):
        c = z
        for i in range(max_iter):
            if z.real * z.real + z.imag * z.imag > 4:
                return i
            z = z * z + c
        return max_iter

    # Generates a mandelbrot set in a (x, y) numpy array with each element
    # carrying the number of iterations. The array is bounded by four numbers
    # (min_x, max_x, min_y, max_y) each determining the maximum and minimum
    # real/imaginary values that are computed. Each element in the array
    # directly corresponds to one pixel.
    @jit
    def generate_set(self, min_x, max_x, min_y, max_y, iterations):
        # arr is a 2D np array containing the image.
        height = self.arr.shape[0]
        width = self.arr.shape[1]

        # This is the step value of a pixel.
        x_pixel = (max_x - min_x) / height
        y_pixel = (max_y - min_y) / width

        # computes the value for the mandelbrot set at each pixel.
        for x in range(height):
            re = min_x + x * x_pixel
            for y in range(width):
                im = min_y + y * y_pixel
                z = complex(re, im)
                mandelbrot_item = self.compute_mandelbrot(z, iterations)
                self.arr[x, y] = mandelbrot_item

    # Takes a resolution and generates the four bounding numbers used by
    # generate_set(). The image will be focused around the focus parameter, and
    # will be zoomed in by a factor of zoom/speed. By default, this generates a 4K
    # image.
    @staticmethod
    @jit
    def range_from_resolution(resolution=(3840, 2160), zoom=1, focus=0 + 0j, framerate=-1, speed=2):
        max_x_pixel, max_y_pixel = resolution[0], resolution[1]

        # the buffer zone is an area added to either side of an image to account
        # for a deviation from a perfect square, as is the norm for most modern
        # screens.
        buffer_zone = 2 * (max_x_pixel - max_y_pixel) / max_y_pixel

        # The zoom value is divided by @speed. This means that the image will
        # double in size every @speed frames. At 24 fps, the image will zoom in
        # by a factor of 4 every second by default.
        scaled_zoom = zoom / (framerate / speed)

        min_x = ((-2.0 - buffer_zone) / 2 ** scaled_zoom + focus.real)
        max_x = ((2.0 + buffer_zone) / 2 ** scaled_zoom + focus.real)
        min_y = (-2.0 / 2 ** scaled_zoom + focus.imag)
        max_y = (2.0 / 2 ** scaled_zoom + focus.imag)

        return min_x, max_x, min_y, max_y

    def generate(self, zoom):
        self.generate_set(
            *self.range_from_resolution(
                self.resolution, zoom, self.focus, self.framerate, self.speed), self.iterations)
