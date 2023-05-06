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


def create_circle_regions(cluster):
    start_time = time.time()
    scale_map_fits = fits.open(cluster.scale_map_file)
    mask_fits = fits.open(cluster.combined_mask)
    region_map = cluster.scale_map_region_index
    scale_map = scale_map_fits[0].data
    mask = mask_fits[0].data
    bounds = scale_map.shape
    xvals = np.arange(bounds[1])
    yvals = np.arange(bounds[0])
    for observation in cluster.observations:
        print('Making circular fitting regions for observation {}'.format(observation.id))
        image_fits = fits.open(observation.acisI_comb_img)
        image_header = image_fits[0].header
        cdelt1p = image_header['CDELT1P']
        cdelt2p = image_header['CDELT2P']
        crval1p = image_header['CRVAL1P']
        crval2p = image_header['CRVAL2P']
        crpix1p = image_header['CRPIX1P']
        crpix2p = image_header['CRPIX2P']
        radii = ((mask * scale_map) * cdelt1p)
        newx = ((((xvals + 1) - crpix1p) * cdelt1p) + crval1p)
        newy = ((((yvals + 1) - crpix2p) * cdelt2p) + crval2p)
        (xx, yy) = np.meshgrid(newx, newy)
        non_zero_indices = np.nonzero(radii)
        nz_rad = radii[non_zero_indices]
        nz_x = xx[non_zero_indices]
        nz_y = yy[non_zero_indices]
        obs_regions = region_map[non_zero_indices]
        region_array = np.array([(i, j, k, l) for (i, j, k, l) in zip(nz_x, nz_y, nz_rad, obs_regions)])
        regions = [['circle({x},{y},{rad})'.format(x=x[0], y=x[1], rad=x[2]), int(x[3])] for x in region_array]
        observation.scale_map_region_list = regions
    end_time = time.time()
    print('Time elapsed making regions for fit: {:0.2f} (s)'.format((end_time - start_time)))
