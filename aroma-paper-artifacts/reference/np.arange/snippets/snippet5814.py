import torch
from pytracking.features.featurebase import FeatureBase, MultiFeatureBase
from pytracking import TensorList
import pdb
import numpy as np


def average_feature_region(im, region_size):
    region_area = (region_size ** 2)
    maxval = 1.0
    iImage = integralVecImage(im)
    i1 = np.arange(region_size, iImage.size(2), region_size)
    i2 = np.arange(region_size, iImage.size(3), region_size)
    i1_ = (i1 - region_size)
    i2_ = (i2 - region_size)
    region_image = ((((iImage[(:, :, i1, :)][(..., i2)] - iImage[(:, :, i1, :)][(..., i2_)]) - iImage[(:, :, i1_, :)][(..., i2)]) + iImage[(:, :, i1_, :)][(..., i2_)]) / (region_area * maxval))
    return region_image
