from __future__ import print_function
import torch
import torch.nn as nn
import torch.utils.data
from torch.autograd import Variable
import torch.nn.functional as F
import math
import numpy as np


def convbn_3d(in_planes, out_planes, kernel_size, stride, pad, dilation=1):
    return nn.Sequential(nn.Conv3d(in_planes, out_planes, kernel_size=kernel_size, padding=pad, stride=stride, dilation=dilation, bias=False), nn.BatchNorm3d(out_planes))
