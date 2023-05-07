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


def transform(img, label, matrix):
    '\n    img: [H, W]  label, [N,2]   \n    '
    img_out = cv2.warpAffine(img, matrix, (cropWidth, cropHeight))
    label_out = np.ones((keypointsNumber, 3))
    label_out[(:, :2)] = label[(:, :2)].copy()
    label_out = np.matmul(matrix, label_out.transpose())
    label_out = label_out.transpose()
    return (img_out, label_out)
