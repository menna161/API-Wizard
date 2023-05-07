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


def convbn_Transpose3d(in_planes, out_planes, kernel_size, stride, pad, output_padding, dilation, bias):
    return nn.Sequential(nn.ConvTranspose3d(in_planes, out_planes, kernel_size=kernel_size, stride=stride, padding=pad, output_padding=output_padding, dilation=dilation, bias=bias), nn.BatchNorm3d(out_planes), nn.ReLU(inplace=True))
