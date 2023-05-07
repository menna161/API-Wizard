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


def world2pixel(x, fx, fy, ux, uy):
    x[(:, :, 0)] = (((x[(:, :, 0)] * fx) / x[(:, :, 2)]) + ux)
    x[(:, :, 1)] = (((x[(:, :, 1)] * fy) / x[(:, :, 2)]) + uy)
    return x
