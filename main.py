from generator import JuliaGenerator, MandelbrotGenerator
from imager import Imager
import time
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--focus',
                        help='Focus of the generator.',
                        required=True)

    generator = parser.add_mutually_exclusive_group(required=True)

    generator.add_argument('-m', '--mandelbrot',
                           action='store_true',
                           help='Generates mandelbrot set. Active by default.')

    generator.add_argument('-j', '--julia',
                           help='Generates a julia set for C',
                           dest='c')

    parser.add_argument('-z', '--zoom',
                        help='Degree by which the image is zoomed in. The final zoom is affected by framerate and speed',
                        type=int,
                        default=0)

    parser.add_argument('--framerate',
                        help='Framerate of the image. Use only when generating a video with FFmpeg',
                        type=int,
                        default=-1)

    parser.add_argument('--speed',
                        help='Speed at which the image doubles its zoom every second.'
                             ' Used with framerate, does nothing otherwise. Defaults to 2.',
                        type=int,
                        default=2)

    parser.add_argument('--iterations',
                        help='Number of iterations before a complex number is declared to be in the set. '
                             '1024 is default',
                        type=int,
                        default=1024)

    parser.add_argument('-c', '--color',
                        help='Colorization function. See color_functions.py for more details. Linear is default.',
                        choices=[
                            'linear',
                            'sin',
                            'linear-sin',
                            'mono',
                            'linear-mono'
                        ],
                        default='linear')

    parser.add_argument('--save',
                        help='Saves the image as NAME',
                        dest='NAME')

    parser.add_argument('--hide',
                        help='Do not show the image once generated',
                        action='store_true')

    parser.add_argument('--time',
                        help='Return the required time to compute an image',
                        action='store_true')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
