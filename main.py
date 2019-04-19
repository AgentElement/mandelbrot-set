from generator import JuliaGenerator, MandelbrotGenerator
from imager import Imager
import time
import sys


def main(focus=-0.761574 + -0.0847596j, zoom=0, iterations=1024, color_type='linear'):
    curr_time = time.time()
    gen = MandelbrotGenerator(focus=0, iterations=iterations, zoom=zoom, resolution=(1920, 1080))
    # print(gen.complex_from_pixel((1920 - 1080) / 2, 1080))
    imgr = Imager(gen)
    img = imgr.generate_image(color_type=color_type)
    img.show()
    print("Mandelbrot set zoom at {} generated in {} seconds".format(focus, time.time() - curr_time))


if __name__ == '__main__':
    main()


