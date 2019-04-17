import numpy as np
from PIL import Image
from numba import jit
import matplotlib.pyplot as plt


################################################################################
# MAIN COLOR FUNCTIONS
################################################################################


@jit
def colorize_sinusoidal(x, max_iter):

    """
    Returns a 3-tuple (red, green, blue) depending on the fraction x/max_iter,
    where x is the number of iterations returned by compute_mandelbrot.

    The channels vary like this:
    Blue decreases as x approaches max_iter. Red increases. Green peaks when
    x / max_iter = 0.5 then decreases. All three channels follow a sinusoidal
    curve.

    :param x: Current iteration
    :param max_iter: Maximum iterations allowed
    :return: RGB tuple
    """

    if x == max_iter:
        return 0, 0, 0

    intensity = (np.pi / 2) * x / max_iter

    red = int(np.sin(intensity) * 256)
    green = int(np.sin(intensity * 2) * 256)
    blue = int(np.cos(intensity) * 256)
    return red, green, blue


@jit
def colorize_sinusoidal_squared(x, max_iter, cutoff=1024):

    """
    Similar to colorize_sinusoidal, but the sinusoidal functions are squared,
    allowing the function to be extended beyond x / cutoff > 1.

    For the first half-cycle, green peaks at 0.5, red increases, blue decreases.
    For the second half-cycle, red decreases and blue increases.

    :param x: Current iteration
    :param max_iter: Maximum iterations allowed.
    :param cutoff: number of iterations for the function to complete one half cycle
    :return: RGB tuple
    """
    if x == max_iter:
        return 0, 0, 0

    intensity = (np.pi / 2) * x / cutoff

    red = int(np.sin(intensity) ** 2 * 256)
    green = int(np.sin(intensity * 2) ** 2 * 256)
    blue = int(np.cos(intensity) ** 2 * 256)
    return red, green, blue


@jit
def colorize_sinusoidal_long(x, max_iter, red_factor=2, green_factor=1, blue_factor=2):

    """
    Similar to colorize_sinusoidal, except the sinusoidal functions are halved
    in magnitude and shifted upward to account for negative values. the color
    scale factors are used to change the frequency at which the channels
    oscillate

    :param x: Current iteration
    :param max_iter: Maximum iterations allowed
    :param red_factor: Changes the frequency of the red channel
    :param green_factor: Changes the frequency of the green channel
    :param blue_factor: Changes the frequency of the blue channel
    :return: RGB tuple
    """

    if x == max_iter:
        return 0, 0, 0

    intensity = np.pi * x / max_iter

    red = 127 + int(np.sin(intensity / red_factor) * 128)
    green = 127 + int(np.sin(intensity / green_factor) * 128)
    blue = 127 + int(np.cos(intensity / blue_factor) * 128)
    return red, green, blue


@jit
def linear_colorize(x, max_iter):

    """
    Mimics colorize_sinusoidal() with linear functions. Use this for
    cheaper computation.

    :param x: Current iteration
    :param max_iter: Maximum iterations allowed
    :return: RGB tuple
    """

    if x == max_iter:
        return 0, 0, 0

    intensity = x / max_iter

    red = int(intensity * 256)
    green = int(512 * (intensity if intensity < 0.5 else 1 - intensity))
    blue = int((1 - intensity) * 256)
    return red, green, blue


@jit
def colorize_mono(x, max_iter):

    """
    Returns a linear, direct, monochromatic tuple proportional to x / max_iter
    :param x: Current iteration
    :param max_iter: Maximum number of iterations allowed
    :return: RGB tuple
    """

    if x == max_iter:
        return 0, 0, 0

    color = int((x / max_iter) * 256) % max_iter
    return color, color, color


@jit
def colorize_mono_squared(x, max_iter):

    """
    Returns a linear, direct, monochromatic tuple proportional to (x/max_iter)^2\
    Use this for most monochromatic images, humans notice differences in
    exponential images more clearly. This isn't strictly exponential, but close
    enough for most purposes.

    :param x: Current iteration
    :param max_iter: Maximum number of iterations allowed
    :return: RGB tuple
    """

    if x == max_iter:
        return 0, 0, 0

    color = int((x / max_iter) ** 2 * 256) % max_iter
    return color, color, color


################################################################################
# COLOR SPECTRUM TESTING
################################################################################


def generate_image(color_function=colorize_sinusoidal_squared, resolution=(1024, 64), scale_factor=1, **kwargs):
    image = Image.new('RGB', resolution)
    for x in range(resolution[0]):
        for y in range(resolution[1]):
            image.putpixel((x, y), color_function(x, resolution[0] // scale_factor, **kwargs))

    return image


def generate_varied_spectrum_images():
    for rf in range(10):
        for gf in range(10):
            for bf in range(10):
                img = generate_image(red_factor=(2 + rf / 10), green_factor=(1 + gf / 10), blue_factor=(2 + bf / 10))
                img.save(r'image_list\images_{}.png'.format(str(rf * 100 + gf * 10 + bf).zfill(3)))


def plot_color_function(color_function=colorize_sinusoidal, max_iter=1024, scale_factor=1, **kwargs):
    color_array = [color_function(value, max_iter // scale_factor, **kwargs) for value in range(max_iter)]
    plt.plot([color_array[red][0] for red in range(max_iter)], color='red')
    plt.plot([color_array[green][1] for green in range(max_iter)], color='green')
    plt.plot([color_array[blue][2] for blue in range(max_iter)], color='blue')


if __name__ == '__main__':
    generate_image(color_function=colorize_sinusoidal_squared, scale_factor=1).show()
    plot_color_function(color_function=colorize_sinusoidal_squared, scale_factor=1)
    plt.show()
