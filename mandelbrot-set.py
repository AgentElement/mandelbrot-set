from generator import JuliaGenerator, MandelbrotGenerator
from imager import Imager
import time
import sys
import argparse
import re


def convert_to_complex(z):
    z = re.sub(r'@', '-', z)
    z = re.sub(r'[iIJ]', 'j', z)
    z = re.sub(r'[\'\" \t]', '', z)
    return complex(z)


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--focus',
                        help='Focus of the generator.',
                        required=True,
                        type=convert_to_complex)

    generator = parser.add_mutually_exclusive_group(required=True)

    generator.add_argument('-m', '--mandelbrot',
                           action='store_true',
                           help='Generates mandelbrot set. Active by default.')

    generator.add_argument('-j', '--julia',
                           help='Generates a julia set for C',
                           action='store',
                           type=convert_to_complex,
                           dest='c')

    parser.add_argument('-z', '--zoom',
                        help='Degree by which the image is zoomed in. '
                             'The final zoom is affected by framerate and speed',
                        action='store',
                        type=convert_to_complex,
                        default=0)

    parser.add_argument('--framerate',
                        help='Framerate of the image. '
                             'Use only when generating a video with FFmpeg',
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
                        help='Colorization function. See color_functions.py for more details. '
                             'Linear is default.',
                        choices=[
                            'linear',
                            'sin',
                            'linear-sin',
                            'mono',
                            'linear-mono'
                        ],
                        default='linear')

    parser.add_argument('--cutoff',
                        help='Number of iterations after which the colorization function repeats itself. '
                             'Only used when the \'sin\' option is selected as the color function.',
                        type=int)

    parser.add_argument('-r', '--resolution',
                        help='Resolution of the image to be generated.',
                        nargs=2,
                        default=[1920, 1080])

    parser.add_argument('--save',
                        help='Saves the image as NAME',
                        dest='NAME')

    parser.add_argument('--hide',
                        help='Do not show the image once generated',
                        action='store_true')

    parser.add_argument('--time',
                        help='Return the required time to compute an image',
                        action='store_true')

    args = sys.argv

    for i, j in enumerate(args):
        if len(j) < 2:
            continue
        if (j[1].isdigit() or j[1] == '.') and j[0] == '-':
            args[i] = '@' + j[1:]

    return parser.parse_args(args[1:])


def main():
    args = parse()

    start_time = time.time()

    if args.mandelbrot:
        generator = MandelbrotGenerator(focus=args.focus,
                                        zoom=args.zoom,
                                        resolution=args.resolution,
                                        framerate=args.framerate,
                                        speed=args.speed,
                                        iterations=args.iterations)

    else:
        generator = JuliaGenerator(focus=args.focus,
                                   zoom=args.zoom,
                                   resolution=args.resolution,
                                   framerate=args.framerate,
                                   speed=args.speed,
                                   iterations=args.iterations,
                                   c=args.c)

    imager = Imager(generator)
    image = imager.generate_image(color_type=args.color, cutoff=args.cutoff)

    if args.time:
        print('{} set generated in {} seconds'.format(
            'Mandelbrot' if args.mandelbrot else 'Julia',
            round(time.time() - start_time, 3)))

    if not args.hide:
        image.show()

    if args.NAME is not None:
        image.save(args.NAME)


if __name__ == '__main__':
    main()
