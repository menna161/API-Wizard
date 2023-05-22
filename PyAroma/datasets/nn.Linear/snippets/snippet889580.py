import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from torch.nn import init
import math
import numpy as np


def __init__(self, base_inp, base_oup, stride, expand_ratio=6):
    super(bottleneck, self).__init__()
    self.max_overall_scale = overall_channel_scale[(- 1)]
    max_inp = base_inp
    max_oup = base_oup
    max_mid = (max_inp * expand_ratio)
    self.max_inp = base_inp
    self.max_oup = base_oup
    self.max_mid = max_mid
    self.stride = stride
    self.fc11 = nn.Linear(3, 64)
    self.fc12 = nn.Linear(64, (((max_mid * max_inp) * 1) * 1))
    self.fc21 = nn.Linear(3, 64)
    self.fc22 = nn.Linear(64, (((max_mid * 1) * 3) * 3))
    self.fc31 = nn.Linear(3, 64)
    self.fc32 = nn.Linear(64, (((max_oup * max_mid) * 1) * 1))
    self.bn1 = nn.ModuleList()
    for mid_scale in mid_channel_scale:
        mid = int((self.max_mid * mid_scale))
        self.bn1.append(nn.BatchNorm2d(mid, affine=False))
    self.bn2 = nn.ModuleList()
    for mid_scale in mid_channel_scale:
        mid = int((self.max_mid * mid_scale))
        self.bn2.append(nn.BatchNorm2d(mid, affine=False))
    self.bn3 = nn.ModuleList()
    for oup_scale in overall_channel_scale:
        oup = int((max_oup * oup_scale))
        self.bn3.append(nn.BatchNorm2d(oup, affine=False))
