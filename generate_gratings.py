"""
Adapted from https://www.baskrahmer.nl/blog/generating-gratings-in-python-using-numpy
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal


def create_grating(sf, ori, offset, wave, rows, cols):
    """
    :param sf: spatial frequency (in pixels)
    :param ori: wave orientation (in degrees, [0-360])
    :param phase: wave phase (in degrees, [0-360])
    :param wave: type of wave ('sqr' or 'sin')
    :param imsize: image size (integer)
    :return: numpy array of shape (imsize, imsize)
    """
    ori = -ori - 90
    phase = offset/sf*360
    # Get x and y coordinates
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))

    # Get the appropriate gradient
    gradient = np.sin(ori * math.pi / 180) * x - np.cos(ori * math.pi / 180) * y

    # Plug gradient into wave function
    if wave == 'sin':
        grating = np.sin((2 * math.pi * gradient) / sf + (phase * math.pi) / 180)
    elif wave == 'sqr':
        grating = signal.square((2 * math.pi * gradient) / sf + (phase * math.pi) / 180)
    else:
        raise NotImplementedError

    return (grating+1)/2

def create_grating_set(sf, ori, vel, wave, rows, cols, frames):
    pts = np.linspace(0,1,num=frames)
    pts = pts*vel
    pts = np.floor(pts)
    gratings = np.zeros([frames,rows, cols])
    for i in range(frames):
        gratings[i,:,:] = create_grating(sf=sf, ori=ori, offset=pts[i], wave=wave, rows=rows, cols=cols)
    return gratings


if __name__ == '__main__':
    gratings = create_grating_set(sf=128, ori=45, vel=30, wave='sin', rows=24, cols=64, frames=30)
    plt.figure()
    for i in range(30):
        plt.subplot(3,10,i+1)
        plt.imshow(gratings[i,:,:], cmap='Greys_r')
        plt.title(i)
    plt.show()