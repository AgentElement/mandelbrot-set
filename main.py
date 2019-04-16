from generator import Generator
from imager import Imager
import numpy as np
from PIL import Image
import time


def main():
    gen = Generator(focus=-0.761574 + -0.0847596j, iterations=1024)
    imgr = Imager(gen)
    img = imgr.generate_image(200, color_type='sin')
    img.show()


if __name__ == '__main__':
    main()



