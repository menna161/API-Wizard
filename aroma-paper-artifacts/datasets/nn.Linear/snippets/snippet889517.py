import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from torch.nn import init
import math
import numpy as np


def __init__(self, input_size=224, num_classes=1000):
    super(MobileNetV1, self).__init__()
    self.feature = nn.ModuleList()
    self.feature.append(conv_3x3(3, 32, 2))
    self.feature.append(dw3x3_pw1x1(32, 64, 1))
    self.feature.append(dw3x3_pw1x1(64, 128, 2))
    self.feature.append(dw3x3_pw1x1(128, 128, 1))
    self.feature.append(dw3x3_pw1x1(128, 256, 2))
    self.feature.append(dw3x3_pw1x1(256, 256, 1))
    self.feature.append(dw3x3_pw1x1(256, 512, 2))
    for i in range(5):
        self.feature.append(dw3x3_pw1x1(512, 512, 1))
    self.feature.append(dw3x3_pw1x1(512, 1024, 2))
    self.feature.append(dw3x3_pw1x1(1024, 1024, 1))
    self.pool1 = nn.AvgPool2d(7)
    self.fc = nn.Linear(1024, 1000)
