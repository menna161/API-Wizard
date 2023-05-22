import os
import sys
import json
import math
import fiona
import shutil
import numpy as np
import geopandas as gpd
import random
import skimage
import argparse
import cv2
from json import JSONDecodeError
import osmnx_funcs
import apls_utils


def create_speed_gdf(image_path, geojson_path, mask_path_out_gray, bin_conversion_func, mask_burn_val_key='burnValue', bufferDistanceMeters=2, bufferRoundness=1, dissolve_by='speed_m/s', bin_conversion_key='speed_mph', zero_frac_thresh=0.05, verbose=False):
    'Create buffer around geojson for speeds, use bin_conversion_func to\n    assign values to the mask'
    try:
        inGDF = gpd.read_file(geojson_path)
    except:
        print("Can't read geosjson:", geojson_path)
        (h, w) = cv2.imread(image_path, 0).shape[:2]
        mask_gray = np.zeros((h, w)).astype(np.uint8)
        skimage.io.imsave(mask_path_out_gray, mask_gray)
        return []
    if (len(inGDF) == 0):
        print('Empty mask for path:', geojson_path)
        (h, w) = cv2.imread(image_path, 0).shape[:2]
        mask_gray = np.zeros((h, w)).astype(np.uint8)
        skimage.io.imsave(mask_path_out_gray, mask_gray)
        return []
    projGDF = osmnx_funcs.project_gdf(inGDF)
    if verbose:
        print('inGDF.columns:', inGDF.columns)
    gdf_utm_buffer = projGDF.copy()
    gdf_utm_buffer['geometry'] = gdf_utm_buffer.buffer(bufferDistanceMeters, bufferRoundness)
    gdf_utm_dissolve = gdf_utm_buffer.dissolve(by=dissolve_by)
    gdf_utm_dissolve.crs = gdf_utm_buffer.crs
    gdf_buffer = gdf_utm_dissolve.to_crs(inGDF.crs)
    if verbose:
        print("gdf_buffer['geometry'].values[0]:", gdf_buffer['geometry'].values[0])
    speed_arr = gdf_buffer[bin_conversion_key].values
    burnVals = [bin_conversion_func(s) for s in speed_arr]
    gdf_buffer[mask_burn_val_key] = burnVals
    apls_utils.gdf_to_array(gdf_buffer, image_path, mask_path_out_gray, mask_burn_val_key=mask_burn_val_key, verbose=verbose)
    im_bgr = cv2.imread(image_path, 1)
    im_gray = np.sum(im_bgr, axis=2)
    zero_frac = (1.0 - (float(np.count_nonzero(im_gray)) / im_gray.size))
    if (zero_frac >= zero_frac_thresh):
        print('zero_frac:', zero_frac)
        print('create_speed_gdf(): checking to ensure masks are null where image is null')
        mask_gray = cv2.imread(mask_path_out_gray, 0)
        zero_locs = np.where((im_gray == 0))
        mask_gray[zero_locs] = 0
        cv2.imwrite(mask_path_out_gray, mask_gray)
    return gdf_buffer
