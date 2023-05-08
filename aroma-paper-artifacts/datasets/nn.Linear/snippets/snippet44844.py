import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict
import math


def __init__(self, sample_size, sample_duration, growth_rate=32, block_config=(6, 12, 24, 16), num_init_features=64, bn_size=4, drop_rate=0, num_classes=1000):
    super(DenseNet, self).__init__()
    self.sample_size = sample_size
    self.sample_duration = sample_duration
    self.features = nn.Sequential(OrderedDict([('conv0', nn.Conv3d(3, num_init_features, kernel_size=7, stride=(1, 2, 2), padding=(3, 3, 3), bias=False)), ('norm0', nn.BatchNorm3d(num_init_features)), ('relu0', nn.ReLU(inplace=True)), ('pool0', nn.MaxPool3d(kernel_size=3, stride=2, padding=1))]))
    num_features = num_init_features
    for (i, num_layers) in enumerate(block_config):
        block = _DenseBlock(num_layers=num_layers, num_input_features=num_features, bn_size=bn_size, growth_rate=growth_rate, drop_rate=drop_rate)
        self.features.add_module(('denseblock%d' % (i + 1)), block)
        num_features = (num_features + (num_layers * growth_rate))
        if (i != (len(block_config) - 1)):
            trans = _Transition(num_input_features=num_features, num_output_features=(num_features // 2))
            self.features.add_module(('transition%d' % (i + 1)), trans)
            num_features = (num_features // 2)
    self.features.add_module('norm5', nn.BatchNorm2d(num_features))
    for m in self.modules():
        if isinstance(m, nn.Conv3d):
            m.weight = nn.init.kaiming_normal(m.weight, mode='fan_out')
        elif (isinstance(m, nn.BatchNorm3d) or isinstance(m, nn.BatchNorm2d)):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
    self.classifier = nn.Linear(num_features, num_classes)
