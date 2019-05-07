#  Copyright (c) 2019 AgentElement

import numpy as np
from numba import jit


class Generator:
    def __init__(self, focus=0 + 0j, zoom=1, resolution=(3840, 2160), framerate=24, speed=2, iterations=256):
        self.zoom = zoom
        self._focus = focus
        self.resolution = resolution
        self.speed = speed
        self.framerate = framerate
        self.iterations = iterations
        self.arr = np.zeros(resolution, dtype=np.uint16)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    @jit
    def range_from_resolution(resolution=(3840, 2160), zoom=1, focus=0 + 0j, framerate=-1, speed=2):
        """
        Takes a resolution and generates the four bounding numbers used by
        generate_set(). The image will be focused around the focus parameter, and
        will be zoomed in by a factor of zoom/speed. By default, this generates a 4K
        image.

        :param resolution: Resolution of the image.
        :param zoom: Factor by which the image must be exponentially zoomed in.
        :param focus: Point around which the image is focused.
        :param framerate: Framerate of the zoom.
        :param speed: Speed at which the image doubles in size [/0.5 seconds].
        :return: Four bounding numbers for generate_set().
        """

        max_x_pixel, max_y_pixel = resolution[0], resolution[1]

        """
        The buffer zone is an area added to either side of an image to account
        for a deviation from a perfect square, as is the norm for most modern
        screens.
        """
        buffer_zone = 2 * (max_x_pixel - max_y_pixel) / max_y_pixel

        if framerate == -1:
            framerate, speed = 1, 1  # If static image, do nothing

        """
        The zoom value is multiplied by @speed and divided by @framerate. This
        means that the image will double in size every (framerate / speed)
        frames. At 24 fps, the image will zoom in by a factor of 4 every second
        by default.
        """
        scaled_zoom = zoom * speed / framerate

        min_x = ((-2.0 - buffer_zone) / 2 ** scaled_zoom + focus.real)
        max_x = ((2.0 + buffer_zone) / 2 ** scaled_zoom + focus.real)
        min_y = (-2.0 / 2 ** scaled_zoom + focus.imag)
        max_y = (2.0 / 2 ** scaled_zoom + focus.imag)

        return min_x, max_x, min_y, max_y

    @jit
    def complex_from_pixel(self, x_pixel, y_pixel):
        """
        returns a complex number corresponding to a pixel of a generated image,
        provided that the zoom and focus of the image correspond to that of the
        generator.
        :param x_pixel: The x-value of the pixel to be converted
        :param y_pixel: The y-value of the pixel to be converted
        :return: Complex
        """
        max_x_pixel, max_y_pixel = self.resolution[0], self.resolution[1]

        buffer_zone = 2 * (max_x_pixel - max_y_pixel) / max_y_pixel

        scaled_zoom = self.zoom * self.speed / self.framerate

        width = (2 + buffer_zone) / 2 ** (scaled_zoom - 1)  # Width of the image in complex space
        height = 1 / 2 ** (scaled_zoom - 2)  # Height of the image in complex space

        re = width * ((x_pixel / max_x_pixel) - 0.5) + self._focus.real
        im = height * ((y_pixel / max_y_pixel) - 0.5) + self._focus.imag

        return complex(re, im)

    def generate_set(self, min_x, max_x, min_y, max_y, iterations):
        pass

    def generate(self):
        pass


class MandelbrotGenerator(Generator):

    def __init__(self, focus=0 + 0j, zoom=1, resolution=(3840, 2160), framerate=24, speed=2, iterations=256):
        super().__init__(
            focus=focus, zoom=zoom, resolution=resolution, framerate=framerate, speed=speed, iterations=iterations
        )

    def __repr__(self):
        return "<mandelbrot_generator res: {}, framerate: {}, speed: {}, iterations: {}>".format(
            self.resolution, self.framerate, self.speed, self.iterations)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    @jit(nopython=True)
    def compute_mandelbrot(z: complex, max_iter: int):

        """
        Computes if a complex number z is in the set, returning the number of
        iterations required for divergence, up to max_iter.

        :param z: Complex number to be tested for divergence.
        :param max_iter: Maximum number of iterations before z is declared to
        be in the set.
        :return: Number of iterations for divergence (if divergence occurs),
        else max_iter.
        """

        c = z
        for i in range(max_iter):
            if z.real * z.real + z.imag * z.imag > 4:
                return i
            z = z * z + c
        return max_iter

    @jit
    def generate_set(self, min_x, max_x, min_y, max_y, iterations):

        """
        Generates a mandelbrot set in self.arr with each element carrying
        the number of iterations. The array is bounded by four numbers
        (min_x, max_x, min_y, max_y) each determining the maximum and minimum
        real/imaginary values that are computed. Each element in the array
        directly corresponds to one pixel. *args are passed to the computation
        function.

        :param min_x: Minimum x-value to be computed.
        :param max_x: Maximum x-value to be computed.
        :param min_y: Minimum y-value to be computed.
        :param max_y: Maximum x-value to be computed.
        :param iterations: number of iterations before the program determines
        convergence
        :return: None
        """

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
                self.arr[x, y] = self.compute_mandelbrot(z, iterations)

    def generate(self):
        self.generate_set(
            *self.range_from_resolution(
                self.resolution, self.zoom, self._focus, self.framerate, self.speed), self.iterations)


class JuliaGenerator(Generator):
    def __init__(self, focus=0 + 0j, zoom=1, resolution=(3840, 2160), framerate=24, speed=2, iterations=256, c=0 + 0j):
        super().__init__(
            focus=focus, zoom=zoom, resolution=resolution, framerate=framerate, speed=speed, iterations=iterations
        )
        self._c = c

    def __repr__(self):
        return "<julia_generator res: {}, framerate: {}, speed: {}, iterations: {}, c: {}>".format(
            self.resolution, self.framerate, self.speed, self.iterations, self._c)

    @staticmethod
    @jit(nopython=True)
    def compute_julia(z: complex, c: complex, max_iter: int):

        """
        Computes if a complex number z is in the julia set of c, returning the
        number of iterations required for divergence, up to max_iter.

        :param z: Complex number to be tested for divergence.
        :param c: Constant around which a julia set is constructed
        :param max_iter: Maximum number of iterations before z is declared to
        be in the set.
        :return: Number of iterations for divergence (if divergence occurs),
        else max_iter.
        """

        for i in range(max_iter):
            if z.real * z.real + z.imag * z.imag > 4:
                return i
            z = z * z + c
        return max_iter

    @jit
    def generate_set(self, min_x, max_x, min_y, max_y, iterations):

        """
        Generates a julia set in self.arr with each element carrying
        the number of iterations. The array is bounded by four numbers
        (min_x, max_x, min_y, max_y) each determining the maximum and minimum
        real/imaginary values that are computed. Each element in the array
        directly corresponds to one pixel. *args are passed to the computation
        function.

        :param min_x: Minimum x-value to be computed.
        :param max_x: Maximum x-value to be computed.
        :param min_y: Minimum y-value to be computed.
        :param max_y: Maximum x-value to be computed.
        :param iterations: number of iterations before the program determines
        convergence
        :return: None
        """

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
                self.arr[x, y] = self.compute_julia(z, self._c, iterations)

    def generate(self):
        self.generate_set(
            *self.range_from_resolution(
                self.resolution, self.zoom, self._focus, self.framerate, self.speed), self.iterations)
