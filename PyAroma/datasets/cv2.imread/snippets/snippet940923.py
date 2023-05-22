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


def create_speed_gdf_v0(image_path, geojson_path, mask_path_out_gray, bin_conversion_func, mask_burn_val_key='burnValue', buffer_distance_meters=2, buffer_cap_style=1, dissolve_by='speed_m/s', bin_conversion_key='speed_mph', verbose=False):
    '\n    Create buffer around geojson for speeds, use bin_conversion_func to\n    assign values to the mask\n    '
    try:
        inGDF = gpd.read_file(geojson_path)
    except:
        print('Empty mask for path:', geojson_path)
        (h, w) = cv2.imread(image_path, 0).shape[:2]
        mask_gray = np.zeros((h, w)).astype(np.uint8)
        skimage.io.imsave(mask_path_out_gray, mask_gray)
        return []
    projGDF = osmnx_funcs.project_gdf(inGDF)
    if verbose:
        print('inGDF.columns:', inGDF.columns)
    gdf_utm_buffer = projGDF.copy()
    gdf_utm_buffer['geometry'] = gdf_utm_buffer.buffer(buffer_distance_meters, buffer_cap_style)
    gdf_utm_dissolve = gdf_utm_buffer.dissolve(by=dissolve_by)
    gdf_utm_dissolve.crs = gdf_utm_buffer.crs
    gdf_buffer = gdf_utm_dissolve.to_crs(inGDF.crs)
    if verbose:
        print("gdf_buffer['geometry'].values[0]:", gdf_buffer['geometry'].values[0])
    speed_arr = gdf_buffer[bin_conversion_key].values
    burnVals = [bin_conversion_func(s) for s in speed_arr]
    gdf_buffer[mask_burn_val_key] = burnVals
    gdf_to_array(gdf_buffer, image_path, mask_path_out_gray, mask_burn_val_key=mask_burn_val_key, verbose=verbose)
    return gdf_buffer
