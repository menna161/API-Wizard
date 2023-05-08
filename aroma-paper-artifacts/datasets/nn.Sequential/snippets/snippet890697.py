import torch.nn as nn
import torch.nn.functional as F
import math
from torch.nn import init


def __init__(self, in_planes, planes, stride=1, droprate=0):
    super(PreActBlock, self).__init__()
    self.bn1 = nn.BatchNorm2d(in_planes)
    self.conv1 = conv3x3(in_planes, planes, stride)
    self.drop = (nn.Dropout(p=droprate) if (droprate > 0) else None)
    self.bn2 = nn.BatchNorm2d(planes)
    self.conv2 = conv3x3(planes, planes)
    if ((stride != 1) or (in_planes != (self.expansion * planes))):
        self.shortcut = nn.Sequential(nn.Conv2d(in_planes, (self.expansion * planes), kernel_size=1, stride=stride, bias=False))
