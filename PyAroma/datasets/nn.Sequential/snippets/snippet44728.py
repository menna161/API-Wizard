from __future__ import division, print_function
import sys
from copy import deepcopy
import math
import argparse
import torch
import torch.nn.init
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.backends.cudnn as cudnn
import os
from tqdm import tqdm
import numpy as np
import random
import cv2
import copy
import PIL
from EvalMetrics import ErrorRateAt95Recall
from Losses import loss_HardNet, loss_random_sampling, loss_L2Net, global_orthogonal_regularization
from W1BS import w1bs_extract_descs_and_save
from Utils import L2Norm, cv2_scale, np_reshape
from Utils import str2bool
import torch.nn as nn
import torch.nn.functional as F
import utils.w1bs as w1bs
from Loggers import Logger, FileLogger


def __init__(self):
    super(HardNet, self).__init__()
    self.features = nn.Sequential(nn.Conv2d(1, 32, kernel_size=3, padding=2, bias=False), nn.BatchNorm2d(32, affine=False), nn.ReLU(), nn.Conv2d(32, 32, kernel_size=3, padding=2, bias=False), nn.BatchNorm2d(32, affine=False), nn.ReLU(), nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=2, bias=False), nn.BatchNorm2d(64, affine=False), nn.ReLU(), nn.Conv2d(64, 64, kernel_size=3, padding=2, bias=False), nn.BatchNorm2d(64, affine=False), nn.ReLU(), nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=2, bias=False), nn.BatchNorm2d(128, affine=False), nn.ReLU(), nn.Conv2d(128, 128, kernel_size=3, padding=2, bias=False), nn.BatchNorm2d(128, affine=False), nn.ReLU(), nn.Dropout(0.3), nn.Conv2d(128, 128, kernel_size=8, bias=False), nn.BatchNorm2d(128, affine=False))
    self.features.apply(weights_init)
    return
