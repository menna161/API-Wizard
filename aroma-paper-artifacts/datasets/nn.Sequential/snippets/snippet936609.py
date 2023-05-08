import math
import torch.nn as nn
import torchvision.transforms as transforms


def make_layers(cfg, quant, batch_norm=False):
    layers = list()
    in_channels = 3
    n = 1
    for v in cfg:
        if (v == 'M'):
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            use_quant = (v[(- 1)] != 'N')
            filters = (int(v) if use_quant else int(v[:(- 1)]))
            conv2d = nn.Conv2d(in_channels, filters, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(filters), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            if use_quant:
                layers += [quant()]
            n += 1
            in_channels = filters
    return nn.Sequential(*layers)
