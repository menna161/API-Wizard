import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from .modules import *
import torch.utils.model_zoo as model_zoo
from collections import OrderedDict


def __init__(self, growth_rate=32, block_config=(6, 12, 24, 16), use_spectral_norm=True, num_init_features=64, bn_size=4, drop_rate=0, num_classes=1000):
    super(DenseNet, self).__init__()
    self.features = nn.Sequential(OrderedDict([('conv0', spectral_norm(nn.Conv2d(3, num_init_features, kernel_size=7, stride=2, padding=3, bias=False), use_spectral_norm)), ('norm0', nn.BatchNorm2d(num_init_features)), ('relu0', nn.ReLU()), ('pool0', nn.MaxPool2d(kernel_size=3, stride=2, padding=1))]))
    num_features = num_init_features
    for (i, num_layers) in enumerate(block_config):
        block = _DenseBlock(num_layers=num_layers, num_input_features=num_features, bn_size=bn_size, growth_rate=growth_rate, drop_rate=drop_rate, use_spectral_norm=use_spectral_norm)
        self.features.add_module(('denseblock%d' % (i + 1)), block)
        num_features = (num_features + (num_layers * growth_rate))
        if (i != (len(block_config) - 1)):
            trans = _Transition(num_input_features=num_features, num_output_features=(num_features // 2), use_spectral_norm=use_spectral_norm)
            self.features.add_module(('transition%d' % (i + 1)), trans)
            num_features = (num_features // 2)
    self.features.add_module('norm5', nn.BatchNorm2d(num_features))
    self.conv_last = spectral_norm(nn.Conv2d(num_features, 256, kernel_size=3), use_spectral_norm)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight.data)
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.bias.data.zero_()
