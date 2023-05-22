import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from functools import partial
from collections import OrderedDict
from config import config
from resnet import get_resnet50


def __init__(self, inplanes, planes, norm_layer, stride=1, dilation=[1, 1, 1], expansion=4, downsample=None, fist_dilation=1, multi_grid=1, bn_momentum=0.0003):
    super(Bottleneck3D, self).__init__()
    self.expansion = expansion
    self.conv1 = nn.Conv3d(inplanes, planes, kernel_size=1, bias=False)
    self.bn1 = norm_layer(planes, momentum=bn_momentum)
    self.conv2 = nn.Conv3d(planes, planes, kernel_size=(1, 1, 3), stride=(1, 1, stride), dilation=(1, 1, dilation[0]), padding=(0, 0, dilation[0]), bias=False)
    self.bn2 = norm_layer(planes, momentum=bn_momentum)
    self.conv3 = nn.Conv3d(planes, planes, kernel_size=(1, 3, 1), stride=(1, stride, 1), dilation=(1, dilation[1], 1), padding=(0, dilation[1], 0), bias=False)
    self.bn3 = norm_layer(planes, momentum=bn_momentum)
    self.conv4 = nn.Conv3d(planes, planes, kernel_size=(3, 1, 1), stride=(stride, 1, 1), dilation=(dilation[2], 1, 1), padding=(dilation[2], 0, 0), bias=False)
    self.bn4 = norm_layer(planes, momentum=bn_momentum)
    self.conv5 = nn.Conv3d(planes, (planes * self.expansion), kernel_size=(1, 1, 1), bias=False)
    self.bn5 = norm_layer((planes * self.expansion), momentum=bn_momentum)
    self.relu = nn.ReLU(inplace=False)
    self.relu_inplace = nn.ReLU(inplace=True)
    self.downsample = downsample
    self.dilation = dilation
    self.stride = stride
    self.downsample2 = nn.Sequential(nn.AvgPool3d(kernel_size=(1, stride, 1), stride=(1, stride, 1)), nn.Conv3d(planes, planes, kernel_size=1, stride=1, bias=False), norm_layer(planes, momentum=bn_momentum))
    self.downsample3 = nn.Sequential(nn.AvgPool3d(kernel_size=(stride, 1, 1), stride=(stride, 1, 1)), nn.Conv3d(planes, planes, kernel_size=1, stride=1, bias=False), norm_layer(planes, momentum=bn_momentum))
    self.downsample4 = nn.Sequential(nn.AvgPool3d(kernel_size=(stride, 1, 1), stride=(stride, 1, 1)), nn.Conv3d(planes, planes, kernel_size=1, stride=1, bias=False), norm_layer(planes, momentum=bn_momentum))
