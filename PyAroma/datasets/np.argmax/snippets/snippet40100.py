import tifffile
import glob
import cv2
import numpy as np
import numpy.linalg as la
import cv2 as cv
from osgeo import gdal
import os
import math
from skimage import img_as_ubyte
from copy import deepcopy
import epipolar
from rpc import RPC
from utm import *
from model_icnet import build_icnet
from densemapnet import DenseMapNet
from densemapnet import Settings


def get_most_frequent_category(cat_array):
    cats = np.zeros(NUM_CATEGORIES)
    for i in range(NUM_CATEGORIES):
        cats[i] = len(cat_array[(cat_array == i)])
    return np.argmax(cats)
