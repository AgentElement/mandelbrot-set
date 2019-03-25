import numpy as np
from PIL import Image
from numba import jit


@jit
def colorize_sinusoidal(x, max_iter):
    if x == max_iter:
        return 0, 0, 0

    red = int(np.sin(x * np.pi / (max_iter * 2)) * 256)
    green = int(np.sin(x * np.pi / max_iter) * 256)
    blue = int(np.cos(x * np.pi / (max_iter * 2)) * 256)
    return red, green, blue


@jit
def colorize_mono(x, max_iter):
    if x == max_iter:
        return 0, 0, 0

    red = int((x / max_iter) ** 2 * 256)
    blue = int((x / max_iter) ** 2 * 256)
    green = int((x / max_iter) ** 2 * 256)
    return red, green, blue


def generate_image(resolution=(1024, 256)):
    image = Image.new('RGB', resolution)
    for x in range(resolution[0]):
        for y in range(resolution[1]):
            image.putpixel((x, y), colorize_sinusoidal(x, resolution[0]))

    return image


if __name__ == '__main__':
    image = generate_image()
    image.show()

