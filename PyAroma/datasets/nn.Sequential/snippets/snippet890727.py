import torch
import torch.nn as nn
import torch.nn.functional as F
from .resnet import conv3x3, PreActResNet, PreActResNet_cifar


def __init__(self, in_planes, planes, stride=1):
    super(SE_PreActBottleneck, self).__init__()
    self.bn1 = nn.BatchNorm2d(in_planes)
    self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
    self.bn2 = nn.BatchNorm2d(planes)
    self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
    self.bn3 = nn.BatchNorm2d(planes)
    self.conv3 = nn.Conv2d(planes, (self.expansion * planes), kernel_size=1, bias=False)
    if ((stride != 1) or (in_planes != (self.expansion * planes))):
        self.shortcut = nn.Sequential(nn.Conv2d(in_planes, (self.expansion * planes), kernel_size=1, stride=stride, bias=False))
    self.fc1 = nn.Conv2d((self.expansion * planes), ((self.expansion * planes) // 16), kernel_size=1)
    self.fc2 = nn.Conv2d(((self.expansion * planes) // 16), (self.expansion * planes), kernel_size=1)
