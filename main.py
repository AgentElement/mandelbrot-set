from generator import Generator
from imager import Imager
import time


def main():
    focus = -0.761574 + -0.0847596j
    curr_time = time.time()
    gen = Generator(focus=focus, iterations=1024)
    imgr = Imager(gen)
    img = imgr.generate_image(200, color_type='linear')
    img.show()
    print("Mandelbrot set zoom at {} generated in {} seconds".format(focus, time.time() - curr_time))


if __name__ == '__main__':
    main()



