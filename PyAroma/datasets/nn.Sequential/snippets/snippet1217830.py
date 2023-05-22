import torch.utils.data
from torch.nn import functional as F
import math
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
from torch.nn.parameter import Parameter
from torch.nn.functional import pad
from torch.nn.modules import Module
from torch.nn.modules.utils import _single, _pair, _triple


def convbn_3d(in_planes, out_planes, kernel_size, stride, pad, dilation):
    return nn.Sequential(Conv3d(in_planes, out_planes, kernel_size=kernel_size, stride=stride, padding=pad, dilation=dilation, bias=False), nn.BatchNorm3d(out_planes))
