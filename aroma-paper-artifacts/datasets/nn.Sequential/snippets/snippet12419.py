import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import numpy as np


def __init__(self, in_planes, planes, dropout_rate, stride=1):
    super(WideBasic, self).__init__()
    self.bn1 = nn.BatchNorm2d(in_planes, momentum=0.9)
    self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, padding=1, bias=True)
    self.dropout = nn.Dropout(p=dropout_rate)
    self.bn2 = nn.BatchNorm2d(planes, momentum=0.9)
    self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=True)
    self.shortcut = nn.Sequential()
    if ((stride != 1) or (in_planes != planes)):
        self.shortcut = nn.Sequential(nn.Conv2d(in_planes, planes, kernel_size=1, stride=stride, bias=True))
