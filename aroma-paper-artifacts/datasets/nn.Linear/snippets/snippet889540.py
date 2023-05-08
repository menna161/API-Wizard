import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from torch.nn import init
import math
import numpy as np


def __init__(self, base_inp, base_oup, stride):
    super(conv_3x3, self).__init__()
    self.stride = stride
    assert (stride in [1, 2])
    self.max_scale = channel_scale[(- 1)]
    self.base_oup = base_oup
    self.base_inp = base_inp
    self.max_oup_channel = int((self.max_scale * self.base_oup))
    self.fc11 = nn.Linear(1, 32)
    self.fc12 = nn.Linear(32, (((self.max_oup_channel * self.base_inp) * 3) * 3))
    self.first_bn = nn.ModuleList()
    for oup_scale in channel_scale:
        oup = int((self.base_oup * oup_scale))
        self.first_bn.append(nn.BatchNorm2d(oup))
