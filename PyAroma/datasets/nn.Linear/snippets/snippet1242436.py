import torch.optim
from torchvision import datasets, transforms
import torch.nn.functional as F
from kymatio import Scattering2D
import torch
import argparse
import kymatio.datasets as scattering_datasets
import torch.nn as nn
from numpy.random import RandomState
import numpy as np


def __init__(self, in_channels, k=2, n=4, num_classes=10, standard=False):
    super(Scattering2dResNet, self).__init__()
    self.inplanes = (16 * k)
    self.ichannels = (16 * k)
    if standard:
        self.init_conv = nn.Sequential(nn.Conv2d(3, self.ichannels, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(self.ichannels), nn.ReLU(True))
        self.layer1 = self._make_layer(BasicBlock, (16 * k), n)
        self.standard = True
    else:
        self.K = in_channels
        self.init_conv = nn.Sequential(nn.BatchNorm2d(in_channels, eps=1e-05, affine=False), nn.Conv2d(in_channels, self.ichannels, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(self.ichannels), nn.ReLU(True))
        self.standard = False
    self.layer2 = self._make_layer(BasicBlock, (32 * k), n)
    self.layer3 = self._make_layer(BasicBlock, (64 * k), n)
    self.avgpool = nn.AdaptiveAvgPool2d(2)
    self.fc = nn.Linear(((64 * k) * 4), num_classes)
