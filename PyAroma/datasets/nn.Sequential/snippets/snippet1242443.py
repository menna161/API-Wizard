import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim
from torchvision import datasets, transforms
from kymatio.torch import Scattering2D
import kymatio.datasets as scattering_datasets
import argparse


def build(self):
    cfg = [256, 256, 256, 'M', 512, 512, 512, 1024, 1024]
    layers = []
    self.K = self.in_channels
    self.bn = nn.BatchNorm2d(self.K)
    if (self.classifier_type == 'cnn'):
        for v in cfg:
            if (v == 'M'):
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                conv2d = nn.Conv2d(self.in_channels, v, kernel_size=3, padding=1)
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
                self.in_channels = v
        layers += [nn.AdaptiveAvgPool2d(2)]
        self.features = nn.Sequential(*layers)
        self.classifier = nn.Linear((1024 * 4), 10)
    elif (self.classifier_type == 'mlp'):
        self.classifier = nn.Sequential(nn.Linear(((self.K * 8) * 8), 1024), nn.ReLU(), nn.Linear(1024, 1024), nn.ReLU(), nn.Linear(1024, 10))
        self.features = None
    elif (self.classifier_type == 'linear'):
        self.classifier = nn.Linear(((self.K * 8) * 8), 10)
        self.features = None
