#include <stdio.h>
#include <time.h>
#include <complex.h>

#define WIDTH 1920
#define HEIGHT 1080


int compute_mandelbrot(float real, float imag, int max_iter)
{
    float creal = real;
    float cimag = imag;
    for (size_t i = 0; i < max_iter; i++)
    {
        if (real * real + imag * imag > 4)
        {
            return i;
        }
        real = real * real - imag * imag + creal;
        imag = (real * imag * 2 + cimag);
    }
    return max_iter;
}


int main()
{
    int numberOfPixels = WIDTH * HEIGHT;
    clock_t programTime = clock();
    for (size_t i = 0; i < numberOfPixels; i++)
    {
        compute_mandelbrot(0, 0, 1024);
    }
    programTime = clock() - programTime;
    printf("%d pixels computed in %f seconds\n", numberOfPixels, (float) programTime / CLOCKS_PER_SEC);
}
