from __future__ import print_function
import torch
import torch.nn as nn
import torch.utils.data
from torch.autograd import Variable
import torch.nn.functional as F
import math
import numpy as np


def __init__(self, inplanes, planes, stride, downsample, pad, dilation):
    super(BasicBlock, self).__init__()
    self.conv1 = nn.Sequential(convbn(inplanes, planes, 3, stride, pad, dilation), nn.ReLU(inplace=True))
    self.conv2 = convbn(planes, planes, 3, 1, pad, dilation)
    self.downsample = downsample
    self.stride = stride
