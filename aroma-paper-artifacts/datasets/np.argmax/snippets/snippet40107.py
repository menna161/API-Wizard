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


def predict_semantics(self, img):
    img = np.expand_dims(img, axis=0)
    img = ((img - 127.5) / 255.0)
    cats = self.seg_model.predict(img)[(0, :, :, 0:self.num_categories)]
    seg = np.argmax(cats, axis=2)
    return seg
