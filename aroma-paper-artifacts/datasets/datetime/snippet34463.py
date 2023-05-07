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


def pixel2world(x, fx, fy, ux, uy):
    x[(:, :, 0)] = (((x[(:, :, 0)] - ux) * x[(:, :, 2)]) / fx)
    x[(:, :, 1)] = (((x[(:, :, 1)] - uy) * x[(:, :, 2)]) / fy)
    return x
