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


def create_optimizer(model, new_lr):
    if (args.optimizer == 'sgd'):
        optimizer = optim.SGD(model.parameters(), lr=new_lr, momentum=0.9, dampening=0.9, weight_decay=args.wd)
    elif (args.optimizer == 'adam'):
        optimizer = optim.Adam(model.parameters(), lr=new_lr, weight_decay=args.wd)
    else:
        raise Exception('Not supported optimizer: {0}'.format(args.optimizer))
    return optimizer