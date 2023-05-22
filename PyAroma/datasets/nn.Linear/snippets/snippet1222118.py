import os
import random
import time
import cv2
import numpy as np
import logging
import argparse
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.multiprocessing as mp
import torch.distributed as dist
import torch.nn.init as initer
from tensorboardX import SummaryWriter
import sys
from utils import dataset, transform, common
from models import fastscnn
from loss import diceloss


def weightsInit(model):
    for m in model.modules():
        if isinstance(m, nn.modules.conv._ConvNd):
            initer.kaiming_normal_(m.weight)
            if (m.bias is not None):
                initer.constant_(m.bias, 0)
        elif isinstance(m, nn.modules.batchnorm._BatchNorm):
            initer.normal_(m.weight, 1.0, 0.02)
            initer.constant_(m.bias, 0.0)
        elif isinstance(m, nn.Linear):
            initer.kaiming_normal_(m.weight)
            if (m.bias is not None):
                initer.constant_(m.bias, 0)
