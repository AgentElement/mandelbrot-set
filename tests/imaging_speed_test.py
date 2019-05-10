from src.generator import JuliaGenerator, MandelbrotGenerator
from src.imager import Imager
import time
import matplotlib.pyplot as plt


def time_gen_res(resolution, show_image=False):
    curr_time = time.process_time()

    generator = MandelbrotGenerator(focus=-0.761574-0.0847596j, zoom=12, resolution=resolution)
    imager = Imager(generator)
    image = imager.generate_image(color_type='linear', cutoff=None)
    if show_image:
        image.show()
    return time.process_time() - curr_time


def main():
    times = []
    resolutions = []
    for i in range(0, 6):
        resolution = (120 * 2 ** i, int(67.5 * 2 ** i))
        resolutions.append(resolution)
        time_to_generate = time_gen_res(resolution)
        print(time_to_generate)
        times.append(time_to_generate)

    res_arr = [i[0] * i[1] for i in resolutions]

    plt.plot(res_arr, times, 'ro', res_arr, times)
    plt.show()


if __name__ == '__main__':
    main()
