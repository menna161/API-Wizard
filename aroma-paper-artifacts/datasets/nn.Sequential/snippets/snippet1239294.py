import torch
import torch.nn as nn
import torchvision
from . import resnet, resnext
from lib.nn import SynchronizedBatchNorm2d
from torch.nn import BatchNorm2d as SynchronizedBatchNorm2d
from functools import partial


def conv3x3_bn_relu(in_planes, out_planes, stride=1):
    return nn.Sequential(conv3x3(in_planes, out_planes, stride), SynchronizedBatchNorm2d(out_planes), nn.ReLU(inplace=True))
