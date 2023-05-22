import sys
import cv2
import os
import csv
import numpy as np
import utils.visualize as visualize
from multiprocessing import Pool
from cv2.dnn import NMSBoxes
from scipy.ndimage.measurements import label
import scipy.ndimage as ndimage
import copy
from gtdb import fit_box
from gtdb import box_utils
from gtdb import feature_extractor
import shutil
import time
from sklearn.cluster import AgglomerativeClustering


def read_math_regions(args):
    (image, pdf_name, page_num, math_files_list) = args
    original_width = image.shape[1]
    original_height = image.shape[0]
    intermediate_width_ratio = (original_width / intermediate_width)
    intermediate_height_ratio = (original_height / intermediate_height)
    annotations_map = {}
    for math_file in math_files_list:
        name = math_file.split(os.sep)[(- 1)]
        if (os.stat(math_file).st_size == 0):
            continue
        data = np.genfromtxt(math_file, delimiter=',')
        if (len(data.shape) == 1):
            data = data.reshape(1, (- 1))
        annotations_map[name] = data
    h = np.arange(0, ((n_horizontal - 1) + stride), stride)
    v = np.arange(0, ((n_vertical - 1) + stride), stride)
    for filename in annotations_map:
        data_arr = annotations_map[filename]
        patch_num = int(filename.split('_')[(- 1)].split('.csv')[0])
        x_offset = h[((patch_num - 1) % len(h))]
        y_offset = v[int(((patch_num - 1) / len(h)))]
        if (data_arr is None):
            continue
        final_width_ratio = (crop_size / final_width)
        final_height_ratio = (crop_size / final_height)
        data_arr[(:, 0)] = (data_arr[(:, 0)] * final_width_ratio)
        data_arr[(:, 2)] = (data_arr[(:, 2)] * final_width_ratio)
        data_arr[(:, 1)] = (data_arr[(:, 1)] * final_height_ratio)
        data_arr[(:, 3)] = (data_arr[(:, 3)] * final_height_ratio)
        data_arr[(:, 0)] = (data_arr[(:, 0)] + (x_offset * crop_size))
        data_arr[(:, 2)] = (data_arr[(:, 2)] + (x_offset * crop_size))
        data_arr[(:, 1)] = (data_arr[(:, 1)] + (y_offset * crop_size))
        data_arr[(:, 3)] = (data_arr[(:, 3)] + (y_offset * crop_size))
        data_arr[(:, 0)] = (data_arr[(:, 0)] * intermediate_width_ratio)
        data_arr[(:, 2)] = (data_arr[(:, 2)] * intermediate_width_ratio)
        data_arr[(:, 1)] = (data_arr[(:, 1)] * intermediate_height_ratio)
        data_arr[(:, 3)] = (data_arr[(:, 3)] * intermediate_height_ratio)
        data_arr[(:, 4)] = (data_arr[(:, 4)] * 100)
        annotations_map[filename] = data_arr
    math_regions = np.array([])
    for key in annotations_map:
        if (len(math_regions) == 0):
            math_regions = annotations_map[key][(:, :)]
        else:
            math_regions = np.concatenate((math_regions, annotations_map[key]), axis=0)
    math_regions = math_regions.astype(int)
    math_regions = math_regions[(- math_regions[(:, 4)]).argsort()]
    return math_regions
