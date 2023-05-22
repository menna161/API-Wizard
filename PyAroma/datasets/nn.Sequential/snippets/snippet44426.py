import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from models_fconv_lpf import *


def make_layers(cfg, batch_norm=False, filter_size=1):
    layers = []
    in_channels = 3
    for v in cfg:
        if (v == 'M'):
            layers += [nn.MaxPool2d(kernel_size=2, stride=1), Downsample(filt_size=filter_size, stride=2, channels=in_channels)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=2)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)
