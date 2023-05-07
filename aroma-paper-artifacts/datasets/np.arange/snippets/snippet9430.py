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


def calculate_effective_times(cluster: cluster.ClusterObj):
    start_time = time.time()
    scale_map = cluster.scale_map
    number_of_regions = cluster.number_of_regions
    nx = scale_map.shape[0]
    ny = scale_map.shape[1]
    effective_data_times = np.zeros(scale_map.shape)
    effective_background_times = np.zeros(scale_map.shape)
    for observation in cluster.observations:
        print('Starting observation {obs}'.format(obs=observation.id))
        high_energy_data = observation.acisI_high_energy_combined_image
        background = observation.backI_high_energy_combined_image
        sum_acis_high_energy = np.sum(high_energy_data)
        sum_back_high_energy = np.sum(background)
        bg_to_data_ratio = (sum_back_high_energy / sum_acis_high_energy)
        source_subtracted_data = observation.acisI_nosrc_combined_mask
        exposure_time = observation.acisI_high_energy_combined_image_header['EXPOSURE']
        (YY, XX) = np.meshgrid(np.arange(ny), np.arange(nx))
        counter = 0
        print('Starting effective exposure time calculations...')
        for x in range(nx):
            for y in range(ny):
                if (scale_map[(x, y)] >= 1):
                    radius = np.sqrt((((x - XX) ** 2) + ((y - YY) ** 2)))
                    region = np.where((radius <= scale_map[(x, y)]))
                    source_subtracted_area = np.sum(source_subtracted_data[region])
                    total_area = source_subtracted_data[region].size
                    fractional_area = (source_subtracted_area / total_area)
                    fractional_exposure_time = (fractional_area * exposure_time)
                    effective_data_times[(x, y)] = fractional_exposure_time
                    effective_background_times[(x, y)] = (fractional_exposure_time * bg_to_data_ratio)
                    counter += 1
                    if (((counter % 1000) == 0) or (counter == number_of_regions) or (counter == 1)):
                        time_elapsed = time.strftime('%H hours %M minutes %S seconds.', time.gmtime((time.time() - start_time)))
                        _update_effective_exposure_time(obsid=observation.id, current_region=counter, number_regions=number_of_regions, time_elapsed=time_elapsed)
        observation.effective_data_time = effective_data_times
        observation.effective_background_time = effective_background_times
