import torch
import torch.nn as nn
import torch.nn.functional as F
from .resnet import conv3x3, PreActResNet, PreActResNet_cifar


def __init__(self, in_planes, planes, stride=1):
    super(SE_PreActBlock, self).__init__()
    self.bn1 = nn.BatchNorm2d(in_planes)
    self.conv1 = conv3x3(in_planes, planes, stride)
    self.bn2 = nn.BatchNorm2d(planes)
    self.conv2 = conv3x3(planes, planes)
    if ((stride != 1) or (in_planes != (self.expansion * planes))):
        self.shortcut = nn.Sequential(nn.Conv2d(in_planes, (self.expansion * planes), kernel_size=1, stride=stride, bias=False))
    self.fc1 = nn.Conv2d(planes, (planes // 16), kernel_size=1)
    self.fc2 = nn.Conv2d((planes // 16), planes, kernel_size=1)
