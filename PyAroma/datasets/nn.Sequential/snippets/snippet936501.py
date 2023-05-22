import math
import torch.nn as nn
from torch.nn.init import kaiming_normal_
import torchvision.transforms as transforms


def make_layers(cfg, batch_norm=False):
    layers = list()
    in_channels = 3
    n = 1
    for v in cfg:
        if (v == 'M'):
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            filters = int(v)
            conv2d = nn.Conv2d(in_channels, filters, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(filters), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            n += 1
            in_channels = filters
    return nn.Sequential(*layers)
