from __future__ import division, print_function
import sys
from copy import deepcopy
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
from EvalMetrics import ErrorRateAt95Recall
from Loggers import Logger, FileLogger
from W1BS import w1bs_extract_descs_and_save
from Utils import L2Norm, cv2_scale, np_reshape
from Utils import str2bool
import torch.utils.data as data
import torch.utils.data as data_utils
import torch.nn.functional as F
from Losses import loss_HardNet, loss_random_sampling, loss_L2Net
import faiss
from matplotlib.pyplot import figure, imshow, axis
from pytorch_sift import SIFTNet
import utils.w1bs as w1bs


def weights_init(m):
    if isinstance(m, nn.Conv2d):
        nn.init.orthogonal(m.weight.data, gain=0.7)
        nn.init.constant(m.bias.data, 0.01)
    if isinstance(m, nn.Linear):
        nn.init.orthogonal(m.weight.data, gain=0.01)
        nn.init.constant(m.bias.data, 0.0)
