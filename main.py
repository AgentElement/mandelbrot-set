from generator import Generator
from imager import Imager
import numpy as np
from PIL import Image


def main():
    gen = Generator(focus=-0.761574 + -0.0847596j, iterations=1024)
    imgr = Imager(gen)
    img = imgr.generate_image(100, color_type='mono')
    img.show()


if __name__ == '__main__':
    main()



