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


def writeTxt(result, center):
    resultUVD_ = result.copy()
    resultUVD_[(:, :, 0)] = result[(:, :, 1)]
    resultUVD_[(:, :, 1)] = result[(:, :, 0)]
    resultUVD = resultUVD_
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
    for i in range(len(result)):
        Xmin = max(lefttop_pixel[(i, 0, 0)], 0)
        Ymin = max(lefttop_pixel[(i, 0, 1)], 0)
        Xmax = min(rightbottom_pixel[(i, 0, 0)], ((320 * 2) - 1))
        Ymax = min(rightbottom_pixel[(i, 0, 1)], ((240 * 2) - 1))
        resultUVD[(i, :, 0)] = (((resultUVD_[(i, :, 0)] * (Xmax - Xmin)) / cropWidth) + Xmin)
        resultUVD[(i, :, 1)] = (((resultUVD_[(i, :, 1)] * (Ymax - Ymin)) / cropHeight) + Ymin)
        resultUVD[(i, :, 2)] = (result[(i, :, 2)] + center[i][0][2])
    resultReshape = resultUVD.reshape(len(result), (- 1))
    with open(os.path.join(save_dir, result_file), 'w') as f:
        for i in range(len(resultReshape)):
            for j in range((keypointsNumber * 3)):
                f.write((str(resultReshape[(i, j)]) + ' '))
            f.write('\n')
    f.close()
