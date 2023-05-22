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


def _get_road_buffer(geoJson, im_vis_file, output_raster, buffer_meters=2, burnValue=1, buffer_cap_style=6, useSpacenetLabels=False, plot_file='', figsize=(11, 3), fontsize=6, dpi=800, show_plot=False, valid_road_types=set([]), verbose=False):
    "\n    Wrapper around create_buffer_geopandas(), with plots\n    Get buffer around roads defined by geojson and image files\n    valid_road_types serves as a filter of valid types (no filter if len==0)\n    https://wiki.openstreetmap.org/wiki/Key:highway\n    valid_road_types = set(['motorway', 'trunk', 'primary', 'secondary',\n                            'tertiary',\n                            'motorway_link', 'trunk_link', 'primary_link',\n                            'secondary_link', 'tertiary_link',\n                            'unclassified', 'residential', 'service' ])\n    "
    try:
        inGDF_raw = gpd.read_file(geoJson)
    except:
        mask_gray = np.zeros(cv2.imread(im_vis_file, 0).shape)
        cv2.imwrite(output_raster, mask_gray)
        return ([], [])
    if useSpacenetLabels:
        inGDF = inGDF_raw
        try:
            inGDF['type'] = inGDF['road_type'].values
            inGDF['class'] = 'highway'
            inGDF['highway'] = 'highway'
        except:
            pass
    elif ((len(valid_road_types) > 0) and (len(inGDF_raw) > 0)):
        if ('highway' in inGDF_raw.columns):
            inGDF = inGDF_raw[inGDF_raw['highway'].isin(valid_road_types)]
            inGDF['type'] = inGDF['highway'].values
            inGDF['class'] = 'highway'
        else:
            inGDF = inGDF_raw[inGDF_raw['type'].isin(valid_road_types)]
            inGDF['highway'] = inGDF['type'].values
        if verbose:
            print('gdf.type:', inGDF['type'])
            if (len(inGDF) != len(inGDF_raw)):
                print('len(inGDF), len(inGDF_raw)', len(inGDF), len(inGDF_raw))
                print("gdf['type']:", inGDF['type'])
    else:
        inGDF = inGDF_raw
        try:
            inGDF['type'] = inGDF['highway'].values
            inGDF['class'] = 'highway'
        except:
            pass
    gdf_buffer = create_buffer_geopandas(inGDF, buffer_distance_meters=buffer_meters, buffer_cap_style=buffer_cap_style, dissolve_by='class', projectToUTM=True)
    if (len(gdf_buffer) == 0):
        mask_gray = np.zeros(cv2.imread(im_vis_file, 0).shape)
        cv2.imwrite(output_raster, mask_gray)
    else:
        gdf_to_array(gdf_buffer, im_vis_file, output_raster, burnValue=burnValue)
    mask_gray = cv2.imread(output_raster, 0)
    if plot_file:
        (fig, (ax0, ax1, ax2, ax3)) = plt.subplots(1, 4, figsize=figsize)
        try:
            gdfRoadLines = gpd.read_file(geoJson)
            gdfRoadLines.plot(ax=ax0, marker='o', color='red')
        except:
            ax0.imshow(mask_gray)
        ax0.axis('off')
        ax0.set_aspect('equal')
        ax0.set_title('Unfiltered Roads from GeoJson', fontsize=fontsize)
        im_vis = cv2.imread(im_vis_file, 1)
        img_mpl = cv2.cvtColor(im_vis, cv2.COLOR_BGR2RGB)
        ax1.imshow(img_mpl)
        ax1.axis('off')
        ax1.set_title('Raw Image', fontsize=fontsize)
        ax2.imshow(mask_gray)
        ax2.axis('off')
        ax2.set_title((('Roads Mask (' + str(np.round(buffer_meters))) + ' meter buffer)'), fontsize=fontsize)
        ax3.imshow(img_mpl)
        z = mask_gray.astype(float)
        z[(z == 0)] = np.nan
        palette = plt.cm.gray
        palette.set_over('orange', 1.0)
        ax3.imshow(z, cmap=palette, alpha=0.4, norm=matplotlib.colors.Normalize(vmin=0.5, vmax=0.9, clip=False))
        ax3.set_title('Raw Image + Buffered Roads', fontsize=fontsize)
        ax3.axis('off')
        plt.savefig(plot_file, dpi=dpi)
        if (not show_plot):
            plt.close()
    return (mask_gray, gdf_buffer)
