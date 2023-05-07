import cv2
import torch
import torch.utils.data
import torch.optim.lr_scheduler as lr_scheduler
import numpy as np
import scipy.io as scio
import os
from PIL import Image
from torch.autograd import Variable
import model as model
import anchor as anchor
from tqdm import tqdm
import random_erasing
import logging
import time
import datetime
import random


def errorCompute(source, target, center):
    assert (np.shape(source) == np.shape(target)), 'source has different shape with target'
    Test1_ = source.copy()
    target_ = target.copy()
    Test1_[(:, :, 0)] = source[(:, :, 1)]
    Test1_[(:, :, 1)] = source[(:, :, 0)]
    Test1 = Test1_
    center_pixel = center.copy()
    centre_world = pixel2world(center.copy(), fx, fy, u0, v0)
    centerlefttop = centre_world.copy()
    centerlefttop[(:, 0, 0)] = (centerlefttop[(:, 0, 0)] - xy_thres)
    centerlefttop[(:, 0, 1)] = (centerlefttop[(:, 0, 1)] + xy_thres)
    centerrightbottom = centre_world.copy()
    centerrightbottom[(:, 0, 0)] = (centerrightbottom[(:, 0, 0)] + xy_thres)
    centerrightbottom[(:, 0, 1)] = (centerrightbottom[(:, 0, 1)] - xy_thres)
    lefttop_pixel = world2pixel(centerlefttop, fx, fy, u0, v0)
    rightbottom_pixel = world2pixel(centerrightbottom, fx, fy, u0, v0)
    for i in range(len(Test1_)):
        Xmin = max(lefttop_pixel[(i, 0, 0)], 0)
        Ymin = max(lefttop_pixel[(i, 0, 1)], 0)
        Xmax = min(rightbottom_pixel[(i, 0, 0)], ((320 * 2) - 1))
        Ymax = min(rightbottom_pixel[(i, 0, 1)], ((240 * 2) - 1))
        Test1[(i, :, 0)] = (((Test1_[(i, :, 0)] * (Xmax - Xmin)) / cropWidth) + Xmin)
        Test1[(i, :, 1)] = (((Test1_[(i, :, 1)] * (Ymax - Ymin)) / cropHeight) + Ymin)
        Test1[(i, :, 2)] = (source[(i, :, 2)] + center[i][0][2])
    labels = pixel2world(target_, fx, fy, u0, v0)
    outputs = pixel2world(Test1.copy(), fx, fy, u0, v0)
    errors = np.sqrt(np.sum(((labels - outputs) ** 2), axis=2))
    return np.mean(errors)
