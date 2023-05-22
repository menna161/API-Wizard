import functools
import torch.nn as nn
from utils.pyt_utils import load_model


def __init__(self, block, layers, norm_layer=nn.BatchNorm2d, bn_eps=1e-05, bn_momentum=0.1, deep_stem=False, stem_width=32, inplace=True):
    self.inplanes = ((stem_width * 2) if deep_stem else 64)
    super(ResNet, self).__init__()
    if deep_stem:
        self.conv1 = nn.Sequential(nn.Conv2d(3, stem_width, kernel_size=3, stride=2, padding=1, bias=False), norm_layer(stem_width, eps=bn_eps, momentum=bn_momentum), nn.ReLU(inplace=inplace), nn.Conv2d(stem_width, stem_width, kernel_size=3, stride=1, padding=1, bias=False), norm_layer(stem_width, eps=bn_eps, momentum=bn_momentum), nn.ReLU(inplace=inplace), nn.Conv2d(stem_width, (stem_width * 2), kernel_size=3, stride=1, padding=1, bias=False))
    else:
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = norm_layer(((stem_width * 2) if deep_stem else 64), eps=bn_eps, momentum=bn_momentum)
    self.relu = nn.ReLU(inplace=inplace)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, norm_layer, 64, layers[0], inplace, bn_eps=bn_eps, bn_momentum=bn_momentum)
    self.layer2 = self._make_layer(block, norm_layer, 128, layers[1], inplace, stride=2, bn_eps=bn_eps, bn_momentum=bn_momentum)
    self.layer3 = self._make_layer(block, norm_layer, 256, layers[2], inplace, stride=2, bn_eps=bn_eps, bn_momentum=bn_momentum)
    self.layer4 = self._make_layer(block, norm_layer, 512, layers[3], inplace, stride=2, bn_eps=bn_eps, bn_momentum=bn_momentum)
