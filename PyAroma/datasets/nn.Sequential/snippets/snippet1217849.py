from __future__ import print_function
import torch
import torch.nn as nn
import torch.utils.data
from torch.autograd import Variable
import torch.nn.functional as F
import math
from .submodule import *
from .SparseConvNet import *


def __init__(self, inplanes):
    super(hourglass, self).__init__()
    self.conv1 = nn.Sequential(convbn_3d(inplanes, (inplanes * 2), kernel_size=3, stride=2, pad=1), nn.ReLU(inplace=True))
    self.conv2 = convbn_3d((inplanes * 2), (inplanes * 2), kernel_size=3, stride=1, pad=1)
    self.conv3 = nn.Sequential(convbn_3d((inplanes * 2), (inplanes * 2), kernel_size=3, stride=2, pad=1), nn.ReLU(inplace=True))
    self.conv4 = nn.Sequential(convbn_3d((inplanes * 2), (inplanes * 2), kernel_size=3, stride=1, pad=1), nn.ReLU(inplace=True))
    self.conv5 = nn.Sequential(nn.ConvTranspose3d((inplanes * 2), (inplanes * 2), kernel_size=3, padding=1, output_padding=1, stride=2, bias=False), nn.BatchNorm3d((inplanes * 2)))
    self.conv6 = nn.Sequential(nn.ConvTranspose3d((inplanes * 2), inplanes, kernel_size=3, padding=1, output_padding=1, stride=2, bias=False), nn.BatchNorm3d(inplanes))
