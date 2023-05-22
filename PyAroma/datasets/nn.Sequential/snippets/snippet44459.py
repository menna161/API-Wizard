import re
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from collections import OrderedDict
from models_lpf import *


def __init__(self, growth_rate=32, block_config=(6, 12, 24, 16), num_init_features=64, bn_size=4, drop_rate=0, num_classes=1000, filter_size=1, pool_only=True):
    super(DenseNet, self).__init__()
    if pool_only:
        self.features = nn.Sequential(OrderedDict([('conv0', nn.Conv2d(3, num_init_features, kernel_size=7, stride=2, padding=3, bias=False)), ('norm0', nn.BatchNorm2d(num_init_features)), ('relu0', nn.ReLU(inplace=True)), ('max0', nn.MaxPool2d(kernel_size=3, stride=1, padding=1)), ('pool0', Downsample(filt_size=filter_size, stride=2, channels=num_init_features))]))
    else:
        self.features = nn.Sequential(OrderedDict([('conv0', nn.Conv2d(3, num_init_features, kernel_size=7, stride=1, padding=3, bias=False)), ('norm0', nn.BatchNorm2d(num_init_features)), ('relu0', nn.ReLU(inplace=True)), ('ds0', Downsample(filt_size=filter_size, stride=2, channels=num_init_features)), ('max0', nn.MaxPool2d(kernel_size=3, stride=1, padding=1)), ('pool0', Downsample(filt_size=filter_size, stride=2, channels=num_init_features))]))
    num_features = num_init_features
    for (i, num_layers) in enumerate(block_config):
        block = _DenseBlock(num_layers=num_layers, num_input_features=num_features, bn_size=bn_size, growth_rate=growth_rate, drop_rate=drop_rate)
        self.features.add_module(('denseblock%d' % (i + 1)), block)
        num_features = (num_features + (num_layers * growth_rate))
        if (i != (len(block_config) - 1)):
            trans = _Transition(num_input_features=num_features, num_output_features=(num_features // 2), filter_size=filter_size)
            self.features.add_module(('transition%d' % (i + 1)), trans)
            num_features = (num_features // 2)
    self.features.add_module('norm5', nn.BatchNorm2d(num_features))
    self.classifier = nn.Linear(num_features, num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            if ((m.in_channels != m.out_channels) or (m.out_channels != m.groups) or (m.bias is not None)):
                nn.init.kaiming_normal_(m.weight)
            else:
                print('Not initializing')
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.Linear):
            nn.init.constant_(m.bias, 0)