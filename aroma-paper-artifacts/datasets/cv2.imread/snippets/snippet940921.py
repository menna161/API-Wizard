import numpy as np
from osgeo import gdal, ogr, osr
import scipy.spatial
import geopandas as gpd
import rasterio as rio
import affine as af
import shapely
import time
import os
import sys
import cv2
import skimage
import subprocess
import matplotlib.pyplot as plt
from math import sqrt, radians, cos, sin, asin
import osmnx_funcs


def geojson_to_arr(image_path, geojson_path, mask_path_out_gray, buffer_distance_meters=2, buffer_cap_style=1, dissolve_by='speed_mph', mask_burn_val_key='burnValue', min_burn_val=0, max_burn_val=255, verbose=False):
    "\n    Create buffer around geojson for desired geojson feature, save as mask\n\n    Arguments\n    ---------\n    image_path : str\n        Path to input image corresponding to the geojson file.\n    geojson_path : str\n        Path to geojson file.\n    mask_path_out_gray : str\n        Output path of saved mask (should end in .tif).\n    buffer_distance_meters : float\n        Width of buffer around geojson lines.  Formally, this is the distance\n        to each geometric object.  Optional.  Defaults to ``2``.\n    buffer_cap_style : int\n        Cap_style of buffer, see: (https://shapely.readthedocs.io/en/stable/manual.html#constructive-methods)\n        Defaults to ``1`` (round).\n    dissolve_by : str\n        Method for differentiating rows in geodataframe, and creating unique\n        mask values.  Defaults to ``'speed_m/s'``.\n    mask_burn_value : str\n        Column to name burn value in geodataframe. Defaults to ``'burnValue'``.\n    min_burn_val : int\n        Minimum value to burn to mask. Rescale all values linearly with this\n        minimum value.  If <= 0, ignore.  Defaultst to ``0``.\n    max_burn_val : int\n        Maximum value to burn to mask. Rescale all values linearly with this\n        maxiumum value.  If <= 0, ignore.  Defaultst to ``256``.\n    verbose : bool\n        Switch to print relevant values.  Defaults to ``False``.\n\n    Returns\n    -------\n    gdf_buffer : geopandas dataframe\n        Dataframe created from geojson\n    "
    try:
        inGDF = gpd.read_file(geojson_path)
    except TypeError:
        print('Empty mask for path:', geojson_path)
        (h, w) = cv2.imread(image_path, 0).shape[:2]
        mask_gray = np.zeros((h, w)).astype(np.uint8)
        skimage.io.imsave(mask_path_out_gray, mask_gray)
        return []
    gdf_buffer = create_buffer_geopandas(inGDF, buffer_distance_meters=buffer_distance_meters, buffer_cap_style=buffer_cap_style, dissolve_by=dissolve_by, projectToUTM=False, verbose=verbose)
    if verbose:
        print('gdf_buffer.columns:', gdf_buffer.columns)
        print('gdf_buffer:', gdf_buffer)
    burn_vals_raw = gdf_buffer[dissolve_by].values.astype(float)
    if verbose:
        print('burn_vals_raw:', burn_vals_raw)
    if ((max_burn_val > 0) and (min_burn_val >= 0)):
        scale_mult = ((max_burn_val - min_burn_val) / np.max(burn_vals_raw))
        burn_vals = (min_burn_val + (scale_mult * burn_vals_raw))
    else:
        burn_vals = burn_vals_raw
    if verbose:
        print('np.unique burn_vals:', np.sort(np.unique(burn_vals)))
    gdf_buffer[mask_burn_val_key] = burn_vals
    gdf_to_array(gdf_buffer, image_path, mask_path_out_gray, mask_burn_val_key=mask_burn_val_key, verbose=verbose)
    return gdf_buffer
