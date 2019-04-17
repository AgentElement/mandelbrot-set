from PIL import Image
from generator import Generator
import color_functions


class Imager:

    def __init__(self, generator: Generator):
        self.__generator = generator
        self.__save_ctr = 0

    def __repr__(self):
        return "<Imager containing: {} on counter {}>".format(self.__generator, self.__save_ctr)

    def __str__(self):
        return repr(self)

    def generate_image(self, zoom, color_type='sin', **kwargs):

        """
        This is a wrapper function that generates the numpy array and turns it
        into a colorized image. Returns the image as a byte array.

        :param zoom: The factor by which the image zooms in
        :param color_type: Short string representations of a color function
        :param kwargs: Passed to the color function
        :return: PIL image
        """

        resolution = self.__generator.resolution
        iterations = self.__generator.iterations
        image = Image.new("RGB", resolution)
        self.__generator.generate(zoom)
        image_array = self.__generator.arr

        _color_function_dict = {
            'sin': color_functions.colorize_sinusoidal_squared,
            'linear_sin': color_functions.colorize_sinusoidal,
            'mono': color_functions.colorize_mono_squared,
            'linear_mono': color_functions.colorize_mono,
            'linear': color_functions.linear_colorize

        }

        color_function = _color_function_dict[color_type]
        if color_function is None:
            raise NotImplementedError

        # -2.0, 1.0, -1.25, 1.25
        for x in range(resolution[1]):
            for y in range(resolution[0]):
                image.putpixel((y, x), color_function(image_array[y][x], iterations, **kwargs))

        return image

    def save_image(self, image):

        """
        Saves the image in the mandelbrot_demo directory as mandelbrot_set_###.png

        :param image: PIL image
        """

        image.save(r"mandelbrot_demo\mandelbrot_set_{}.png".format(str(self.__save_ctr).zfill(3)))
        self.__save_ctr += 1
