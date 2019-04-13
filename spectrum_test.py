import numpy as np
from PIL import Image
from numba import jit


@jit
def colorize_sinusoidal(x, max_iter):
    if x == max_iter:
        return 0, 0, 0

    red = int(np.sin(x * np.pi / (max_iter * 2)) * 256) % max_iter
    green = int(np.sin(x * np.pi / max_iter) * 256) % max_iter
    blue = int(np.cos(x * np.pi / (max_iter * 2)) * 256) % max_iter
    return red, green, blue


@jit
def colorize_sinusoidal_long(x, max_iter, red_factor=2, green_factor=1, blue_factor=2):
    if x == max_iter:
        return 0, 0, 0

    red = 127 + int(np.sin(x * np.pi / (max_iter * red_factor)) * 128)
    green = 127 + int(np.sin(x * np.pi / (max_iter * green_factor)) * 128)
    blue = 127 + int(np.cos(x * np.pi / (max_iter * blue_factor)) * 128)
    return red, green, blue


@jit
def colorize_mono(x, max_iter):
    if x == max_iter:
        return 0, 0, 0

    color = int((x / max_iter) ** 2 * 256) % max_iter
    return color, color, color


def generate_image(resolution=(1024, 64), **kwargs):
    image = Image.new('RGB', resolution)
    for x in range(resolution[0]):
        for y in range(resolution[1]):
            image.putpixel((x, y), colorize_sinusoidal_long(x, resolution[0] // 8, **kwargs))

    return image


if __name__ == '__main__':
    for rf in range(10):
        for gf in range(10):
            for bf in range(10):
                image = generate_image(red_factor=(2 + rf / 10), green_factor=(1 + gf / 10), blue_factor=(2 + bf / 10))
                image.save(r'image_list\images_{}.png'.format(str(rf * 100 + gf * 10 + bf).zfill(3)))

