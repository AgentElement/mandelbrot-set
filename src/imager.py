#  Copyright (c) 2019 AgentElement

from PIL import Image
from src.generator import Generator
from src import color_functions
import sys


class Imager:

    def __init__(self, generator: Generator):
        self.__generator = generator
        self.__save_ctr = 0

    def __repr__(self):
        return "<Imager containing: {} on counter {}>".format(self.__generator, self.__save_ctr)

    def __str__(self):
        return repr(self)

    def generate_image(self, color_type='sin', **kwargs):

        """
        This is a wrapper function that generates the numpy array and turns it
        into a colorized image. Returns the image as a byte array.

        :param color_type: Short string representations of a color function
        :param kwargs: Passed to the color function
        :return: PIL image
        """

        if kwargs['cutoff'] is None:
            del kwargs['cutoff']

        resolution = self.__generator._resolution
        iterations = self.__generator.iterations
        image = Image.new("RGB", resolution)
        self.__generator.generate()
        generated_array = self.__generator.arr

        if color_type not in color_functions.color_function_dict.keys():
            raise Exception('Not a valid colorization function!')

        color_function = color_functions.color_function_dict[color_type]
        if color_function is None:
            print('ERROR: {} has not been implemented yet.'.format(color_type))
            sys.exit(0)

        # -2.0, 1.0, -1.25, 1.25
        for x in range(resolution[1]):
            for y in range(resolution[0]):
                image.putpixel((y, x), color_function(generated_array[y][x], iterations, **kwargs))

        return image

    def save_image(self, image):

        """
        Saves the image in the mandelbrot_demo directory as mandelbrot_set_###.png

        :param image: PIL image
        """

        image.save(r"mandelbrot_demo\mandelbrot_set_{}.png".format(str(self.__save_ctr).zfill(3)))
        self.__save_ctr += 1
