import sys
from os import path, mkdir, listdir, makedirs
import numpy as np
import random
import timeit
import cv2
from tqdm import tqdm
from skimage import measure
from skimage.morphology import square, erosion, dilation
from skimage.morphology import remove_small_objects, watershed, remove_small_holes
from skimage.color import label2rgb
from scipy import ndimage
import pandas as pd
from sklearn.model_selection import KFold
from shapely.wkt import dumps
from shapely.geometry import shape, Polygon
from collections import defaultdict


def mask_to_polygons(mask, min_area=8.0):
    'Convert a mask ndarray (binarized image) to Multipolygons'
    (image, contours, hierarchy) = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if (not contours):
        return Polygon()
    cnt_children = defaultdict(list)
    child_contours = set()
    assert (hierarchy.shape[0] == 1)
    for (idx, (_, _, _, parent_idx)) in enumerate(hierarchy[0]):
        if (parent_idx != (- 1)):
            child_contours.add(idx)
            cnt_children[parent_idx].append(contours[idx])
    all_polygons = []
    for (idx, cnt) in enumerate(contours):
        if ((idx not in child_contours) and (cv2.contourArea(cnt) >= min_area)):
            assert (cnt.shape[1] == 1)
            poly = Polygon(shell=cnt[(:, 0, :)], holes=[c[(:, 0, :)] for c in cnt_children.get(idx, []) if (cv2.contourArea(c) >= min_area)])
            all_polygons.append(poly)
    if (len(all_polygons) > 1):
        print('more than one polygon!')
    wkt = dumps(all_polygons[0], rounding_precision=0)
    return wkt
