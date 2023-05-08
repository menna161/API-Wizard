import torch.nn as nn
import torch.nn.functional as F
import math
from torch.nn import init


def __init__(self, in_planes, planes, stride=1, droprate=None):
    super(PreActBottleneck, self).__init__()
    self.bn1 = nn.BatchNorm2d(in_planes)
    self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
    self.bn2 = nn.BatchNorm2d(planes)
    self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
    self.bn3 = nn.BatchNorm2d(planes)
    self.conv3 = nn.Conv2d(planes, (self.expansion * planes), kernel_size=1, bias=False)
    if ((stride != 1) or (in_planes != (self.expansion * planes))):
        self.shortcut = nn.Sequential(nn.Conv2d(in_planes, (self.expansion * planes), kernel_size=1, stride=stride, bias=False))
