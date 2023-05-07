import cluster
import pypeline_io as io
import numpy as np
import time
import argparse
import data_operations as do
from astropy.io import fits
import multiprocessing as mp
import ciao_contrib.runtool as rt
import ciao
from tqdm import tqdm
import ciao
import ciao
from ciao_contrib import runtool as rt
from ciao_contrib import runtool as rt
import ciao
import shockfinder


def binary_search_radii(image=np.zeros(0), index=(0, 0), search_radii=np.arange(1, 100.125, 0.125), s_to_n=40):
    'Use a binary search algorithm to find the smallest radius circular bin, centered at the given index,\n    that affords the desired signal to noise ratio. \n    \n    Keyword arguments:\n    image        -- The image you are binning (2d numpy array)\n    index        -- The pixel within the image the circular bin is centered on (e.g. [0,0])\n    search_radii -- The various radii to search through in an effort to find the smallest (1D numpy array)\n    s_to_n       -- The desired signal to noise ratio each bin must achieve.\n    \n    returns      -- x,y (the seperated index argument), bin radius, signal to noise\n    '
    radii = search_radii
    left = 0
    right = radii.shape[0]
    (nx, ny) = image.shape
    (x, y) = index
    max_radii = search_radii[(- 1)]
    buff_radius = int((max_radii + 2))
    x1 = (x - buff_radius)
    x1 = (0 if (x1 < 0) else x1)
    x2 = (x + buff_radius)
    x2 = (nx if (x2 > nx) else x2)
    y1 = (y - buff_radius)
    y1 = (0 if (y1 < 0) else y1)
    y2 = (y + buff_radius)
    y2 = (ny if (y2 > ny) else y2)
    small_image = image[(x1:x2, y1:y2)]
    radius = generate_radius_map(x, y, nx, ny)[(x1:x2, y1:y2)]
    if (np.sum(small_image[(radius <= radii[(- 1)])]) == 0):
        return (x, y, 0, 0)
    last_good_radii = None
    last_good_s_to_n = 0
    while (left < right):
        middle = int(((left + right) / 2))
        r = radii[middle]
        indices_within_r = (radius <= r)
        total_counts = np.sum(small_image[indices_within_r])
        noise_total = np.sqrt(total_counts)
        signal_to_noise = (total_counts / noise_total)
        if (signal_to_noise < s_to_n):
            left = (middle + 1)
        else:
            last_good_radii = r
            last_good_s_to_n = signal_to_noise
            right = middle
    if (r <= 100):
        return (x, y, last_good_radii, last_good_s_to_n)
    else:
        counter += 1
        return (x, y, 0, 0)
