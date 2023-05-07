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


def dataPreprocess(index, img, keypointsUVD, center, mean, std, lefttop_pixel, rightbottom_pixel, xy_thres=90, depth_thres=75, augment=True):
    imageOutputs = np.ones((cropHeight, cropWidth, 1), dtype='float32')
    labelOutputs = np.ones((keypointsNumber, 3), dtype='float32')
    if augment:
        RandomOffset_1 = np.random.randint(((- 1) * RandCropShift), RandCropShift)
        RandomOffset_2 = np.random.randint(((- 1) * RandCropShift), RandCropShift)
        RandomOffset_3 = np.random.randint(((- 1) * RandCropShift), RandCropShift)
        RandomOffset_4 = np.random.randint(((- 1) * RandCropShift), RandCropShift)
        RandomOffsetDepth = np.random.normal(0, RandshiftDepth, (cropHeight * cropWidth)).reshape(cropHeight, cropWidth)
        RandomOffsetDepth[np.where((RandomOffsetDepth < RandshiftDepth))] = 0
        RandomRotate = np.random.randint(((- 1) * RandRotate), RandRotate)
        RandomScale = ((np.random.rand() * RandScale[0]) + RandScale[1])
        matrix = cv2.getRotationMatrix2D(((cropWidth / 2), (cropHeight / 2)), RandomRotate, RandomScale)
    else:
        (RandomOffset_1, RandomOffset_2, RandomOffset_3, RandomOffset_4) = (0, 0, 0, 0)
        RandomRotate = 0
        RandomScale = 1
        RandomOffsetDepth = 0
        matrix = cv2.getRotationMatrix2D(((cropWidth / 2), (cropHeight / 2)), RandomRotate, RandomScale)
    new_Xmin = max((lefttop_pixel[(index, 0, 0)] + RandomOffset_1), 0)
    new_Ymin = max((lefttop_pixel[(index, 0, 1)] + RandomOffset_2), 0)
    new_Xmax = min((rightbottom_pixel[(index, 0, 0)] + RandomOffset_3), (img.shape[1] - 1))
    new_Ymax = min((rightbottom_pixel[(index, 0, 1)] + RandomOffset_4), (img.shape[0] - 1))
    imCrop = img[(int(new_Ymin):int(new_Ymax), int(new_Xmin):int(new_Xmax))].copy()
    imgResize = cv2.resize(imCrop, (cropWidth, cropHeight), interpolation=cv2.INTER_NEAREST)
    imgResize = np.asarray(imgResize, dtype='float32')
    imgResize[np.where((imgResize >= (center[index][0][2] + depth_thres)))] = center[index][0][2]
    imgResize[np.where((imgResize <= (center[index][0][2] - depth_thres)))] = center[index][0][2]
    imgResize = ((imgResize - center[index][0][2]) * RandomScale)
    imgResize = ((imgResize - mean) / std)
    label_xy = np.ones((keypointsNumber, 2), dtype='float32')
    label_xy[(:, 0)] = (((keypointsUVD[(index, :, 0)].copy() - new_Xmin) * cropWidth) / (new_Xmax - new_Xmin))
    label_xy[(:, 1)] = (((keypointsUVD[(index, :, 1)].copy() - new_Ymin) * cropHeight) / (new_Ymax - new_Ymin))
    if augment:
        (imgResize, label_xy) = transform(imgResize, label_xy, matrix)
    imageOutputs[(:, :, 0)] = imgResize
    labelOutputs[(:, 1)] = label_xy[(:, 0)]
    labelOutputs[(:, 0)] = label_xy[(:, 1)]
    labelOutputs[(:, 2)] = ((keypointsUVD[(index, :, 2)] - center[index][0][2]) * RandomScale)
    imageOutputs = np.asarray(imageOutputs)
    imageNCHWOut = imageOutputs.transpose(2, 0, 1)
    imageNCHWOut = np.asarray(imageNCHWOut)
    labelOutputs = np.asarray(labelOutputs)
    (data, label) = (torch.from_numpy(imageNCHWOut), torch.from_numpy(labelOutputs))
    return (data, label)
