# mandelbrot-set

***

**Description**: This is a command line program used to generate images of mandelbrot and julia sets.
 

## Table of Contents

* [mandelbrot-set](#mandelbrot-set)
    * [What are Mandelbrot and julia sets?](#what-are-mandelbrot-and-julia-sets)
    
    * [Usage](#Usage)
    
    * [Installation](#Installation)

    * [Options](#Options)

    * [Colorization Functions](#colorization-functions)
    
## What are Mandelbrot and Julia Sets?

[Numberphile has a pretty good video exploring mandelbrot sets.](https://www.youtube.com/watch?v=NGMRB4O922I)

To explain mandelbrot sets, I'll start with julia sets.

Consider a real number, `R`. Now square this number repeatedly.
If the absolute value of that number is greater than one, it'll tend towards infinity.
If it's smaller than one, it'll shrink towards zero.
If it's exactly one, it'll stay at one without going anywhere.

We can see this here:

```-7 -> 49 -> 2401 ... +inf```

```0.7 -> 0.49 -> 0.2401 ... 0```

We can easily expand this definition to complex numbers.
In fact, all numbers whose absolute value is less than one will shrink towards 0,
and all numbers whose absolute value is greater than one will 'escape' to infinity.

Let's do something more interesting than just squaring the number. 
Let's add a constant, `C`, every time we square the number:

```
R -> R^2 + C
```

We can apply this repeatedly. Now, if the number is large enough,
it won't matter what value we use for `C`, the sequence will escape anyway.
In fact, if the absolute value of any element in the sequence is ever greater than 2,
the sequence will escape towards infinity. If the number never escapes, 
it belongs to the *julia* set of `C`.

Now, numbers that are in a julia set are not very interesting.
However, we can plot on the complex plane all numbers that aren't in the set.
We simply take the number of iterations required for that number to escape the set
(i.e. the number of times the julia function must be applied such that the 
absolute value of `R` exceeds 2.) and assign a color to each iteration.
This can create some *seriously* impressive fractals. Some julia sets 
(Like the julia set of `0`, a circle) aren't very interesting, while others 
(try `-0.761574 - 0.0847596i`!) can be beautiful.

The famous mandelbrot set can be thought of as a very specific variant of a julia set.
Instead of the julia function, you have this:

```
C = R
R -> R^2 + C
```

Instead of `C` being a constant value, the mandelbrot function sets `C` equal to `R` and proceeds normally.
Consequently, we don't need to select a constant, and there is only one mandelbrot set.
The edge of the mandelbrot set is a fractal and values close to it can be plotted the same way as described above.
This is where all the popular mandelbrot zoom videos on [YouTube](https://www.youtube.com/watch?v=PD2XgQOyCCk)
come from.

Obviously, every element in the set will take an infinite amount of time to escape
(by definition, elements in the set never escape), so we use a finite number of iterations to
approximate the boundary of the set. A large enough number of iterations is good
enough for almost all purposes.

## Usage

```bash
python mandelbrot-set.py [-h] -f FOCUS (-m | -j C) [-z ZOOM]
                         [--framerate FRAMERATE] [--speed SPEED]
                         [--iterations ITERATIONS]
                         [-c {linear,sin,linear-sin,mono,linear-mono}]
                         [--cutoff CUTOFF] [-r RESOLUTION RESOLUTION]
                         [--save NAME] [--hide] [--time]
```

## Installation
### With Virtual Environments (recommended) 

Once you clone the directory, simply execute the following:
```bash
$ cd mandelbrot-set
$ virtualenv venv
$ venv/scripts/activate
$ pip install requirements.txt
```

This sets up a virtual environment for the program.

***

### Manual Installation

`pip install` the following libraries (You can set up a virtual environment for this too.)
```bash
numpy
matplotlib
numba
Pillow
```
You should be good to go. 

## Options
### Required Arguments:

#### `-f FOCUS`
`--focus FOCUS`

Sets the focus (center) of your image.

```
// Valid arguments
$ python mandelbrot-set.py -f 0+0j -m
$ python mandelbrot-set.py --focus 0+0j -m
$ python mandelbrot-set.py -f -1 -m
$ python mandelbrot-set.py -f "0+0j" -m
$ python mandelbrot-set.py -f "0 + 0j" -m

// Invalid arguments
$ python mandelbrot-set.py -f 0 + 0j -m    <- Spaces aren't allowed, pass the number as a string instead
```

Note: `i`, `j`, `I`, and `J` all can be used to denote the imaginary constant.

***

#### `(-m | -j C)`
`--mandelbrot` or `--julia C`

Tells the program to generate either a mandelbrot set (`-m`) or the julia set of C (`-j C`).
Specifying one of these arguments is mandatory.

This will generate the 'default' mandelbrot set, centered around `0, 0`:

```bash
$ python mandelbrot-set.py -f 0+0j -m
```

On the other hand, this will generate the julia set for `-0.1 + 0.1j`, centered around the same point.

```bash
$ python mandelbrot-set.py -f 0+0j -j "-0.1 + 0.1j"
```

Note that the complex number argument for `-j` follows the same rules as that for `--focus`.

### Optional Arguments:
#### `-z ZOOM`
`--zoom ZOOM`

Zooms into the set by a factor of ZOOM. This defaults to `0`.

The vertical height of the image with the zoom set to 0 and with 0 as the focus
corresponds to a range of `+2j` to `-2j`. A zoom value of 1 halves that,
from `+j` to `-j`. The horizontal width is scaled so that the image retains a rectangular zoom.
The image will always correctly zoom to half its original size around the focus
 with every unit increase in the zoom.

The *actual* zoom changes with the `--framerate` and `--speed` options. By default, they are both set to 1. The final, scaled zoom is given by:

```python
scaled_zoom = zoom * speed / framerate
```

This is used only if you want to make a mandelbrot zoom with `ffmpeg`.
Visit the sections on [`--speed`](#--speed) and [`--framerate`](#--framerate) for more details.

***

#### `--speed SPEED`
To be used with `ffmpeg`.

Sets the speed of the zoom to `SPEED`. The speed of the zoom is the speed at which the zoom doubles every second.
A speed of 1 means the zoom doubles once every second, a speed of 2 means that the zoom doubles twice every second and so on.

***

#### `--framerate FRAMERATE`
To be used with `ffmpeg`.

Sets the framerate of the zoom to `FRAMERATE`.
Specify the same number when stitching the images together with `ffmpeg` for `--speed` to behave normally.

***

#### `-i ITERATIONS`
`--iterations ITERATIONS`

Sets the maximum number of iterations required before a complex number is declared to be in the set.
This also changes how the colorization function behaves. Higher values mean more detailed mandelbrot sets,
but take longer to computes. This defaults to `1024` iterations.

***

#### `-c COLOR`
`--color COLOR`

Sets the colorization function of the image. There are five options, with more under development:
```
--color linear
--color sin
--color mono
--color linear-sin
--color linear-mono
```
`linear` is the default option.

See the [colorization functions](#colorization-functions) section for more details on each of these.

***

#### `--cutoff CUTOFF`
Used only when the color function `--color sin` is used.
[See the section on this function for more details.](#sin)


Changing the value of `--cutoff` creates images that covers more
(if `--cutoff < --iterations`) or less (if `--cutoff > --iterations`) of the available color space.

If `--cutoff` less than `--iterations`, the `sin` colorization function will 
wrap around backwards to fill in higher values of iterations.

Defaults to `1024`.

***

#### `-r RESOLUTION RESOLUTION`
`--resolution RESOLUTION RESOLUTION`

Sets the resolution of the image. The first argument is the width (default: `1920`),
the second is the height (default: `1080`).

***

#### `--save NAME`

Saves the image as NAME. Note that the file format must be specified with the image name.
If you wish to save the image in another directory, the **relative path** must be provided.

***

#### `--hide`

Does not show the image once processed. Used with `--save`.

***

#### `--time`

Prints the amount of time required for the image to generate, in seconds.

***

## Colorization Functions


#### `linear-sin`
This function takes the fraction between the computed iterations of the
mandelbrot / julia function and the maximum number of iterations allowed.
With this fraction, it varies the RGB channels as follows:

* The blue channel decreases as the fraction approaches 1 (This follows a `cosine` function)
* The red channel increases as the fraction approaches 1 (This follows a `sine` function)
* The green channel increases as the fraction approaches 0.5, then decreases. (This follows the `sin(2x)` function)

***

#### `linear`

This function mimics the `linear-sin` function with linear functions.
This is the cheapest to compute and is therefore the default option.

***

#### `sin`
This is similar to linear_sin with two key differences: 
It squares the sinusoidal functions of `linear-sin` and it takes the fraction 
between the maximum number of iterations and the value of `--cutoff`.
Changing the value of `--cutoff` creates images that covers more
(if `--cutoff < --iterations`) or less (if `--cutoff > --iterations`) of the available color space.

As the `sin` color function is independent of `--iterations`,
it is recommended if you wish to compare the mandelbrot sets generated by varying `--iterations`. 

***

#### `mono`
Monochromatically colorizes the mandelbrot set proportional to the **square**
of the fraction between the computed iterations of the
mandelbrot / julia function and the maximum number of iterations allowed.
 
***

#### `linear-mono`
Monochromatically colorizes the mandelbrot set **linearly proportional** to
the fraction between the computed iterations of the
mandelbrot / julia function and the maximum number of iterations allowed.

***