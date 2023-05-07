from shapely.geometry import LineString, Polygon, MultiPolygon
import numpy as np
import cv2
import shapely
from collections import defaultdict
from skimage.transform import rescale
import glob
from skimage import io
from tqdm import tqdm
import sys


def contours_hierarchy(mask):
    (image, contours, hierarchy) = cv2.findContours(((mask == 1) * 255).astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    return (contours, hierarchy)
