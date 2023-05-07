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


def generate_acb_scale_map_for(indices=None, image=np.zeros(0), max_bin_radius=100, step_size=0.125, s_to_n=40, num_processes=20):
    'Generate an adaptive circular bin map for the given image.\n    \n    Keyword arguments:\n    image          -- The image you want an adaptive circular bin map for (2D numpy array)\n    max_bin_radius -- The maximum bin radius for each circular bin (int)\n    step_size      -- The step size between different radii. (float)\n    s_to_n         -- The desired signal to noise ratio for each bin (int although can be float)\n    num_processes  -- The number of processes you want to use for your multiprocessing pool (int)\n    \n    returns -- The adaptive circular bin map and the signal to noise map (both 2D numpy arrays)\n    '
    radii_to_search = np.arange(start=1, stop=(max_bin_radius + step_size), step=step_size)
    acb_scale_map = np.zeros(image.shape)
    s_to_n_map = np.zeros(image.shape)
    arguments = [[image, index, radii_to_search, s_to_n] for index in indices]
    with mp.Pool(num_processes) as pool:
        results = list(tqdm(pool.imap(binary_search_radii_wrapper, arguments), total=len(arguments), desc='Calculating ACB Map'))
    np_res = np.array(results)
    print(np_res.shape)
    x = np_res[(:, 0)].astype(int)
    y = np_res[(:, 1)].astype(int)
    acb_scale_map[(x, y)] = np_res[(:, 2)]
    s_to_n_map[(x, y)] = np_res[(:, 3)]
    return (acb_scale_map, s_to_n_map)
