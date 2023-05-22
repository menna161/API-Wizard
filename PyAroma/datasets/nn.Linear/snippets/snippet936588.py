import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint as cp
from collections import OrderedDict
from qtorch import BlockQuantizer, FixedQuantizer


def __init__(self, growth_rate=12, block_config=(16, 16, 16), compression=0.5, num_init_features=24, bn_size=4, drop_rate=0, num_classes=10, small_inputs=True, efficient=False, forward_wl=(- 1), forward_fl=(- 1), backward_wl=(- 1), backward_fl=(- 1), forward_layer_type='fixed', backward_layer_type='', forward_round_type='stochastic', backward_round_type=''):
    assert (forward_layer_type in ['block', 'fixed'])
    assert (forward_round_type in ['nearest', 'stochastic'])
    if (backward_layer_type == ''):
        backward_layer_type = forward_layer_type
    if (backward_round_type == ''):
        backward_round_type = forward_round_type
    assert (backward_layer_type in ['block', 'fixed'])
    assert (backward_round_type in ['nearest', 'stochastic'])
    if (forward_layer_type == 'block'):
        quant = (lambda : BlockQuantizer(forward_wl, backward_wl, forward_round_type, backward_round_type))
    elif (forward_layer_type == 'fixed'):
        quant = (lambda : FixedQuantizer(forward_wl, forward_fl, backward_wl, backward_fl, forward_round_type, backward_round_type))
    super(DenseNet, self).__init__()
    assert (0 < compression <= 1), 'compression of densenet should be between 0 and 1'
    self.avgpool_size = (8 if small_inputs else 7)
    if small_inputs:
        self.features = nn.Sequential(OrderedDict([('conv0', nn.Conv2d(3, num_init_features, kernel_size=3, stride=1, padding=1, bias=False))]))
    else:
        self.features = nn.Sequential(OrderedDict([('conv0', nn.Conv2d(3, num_init_features, kernel_size=7, stride=2, padding=3, bias=False))]))
        self.features.add_module('norm0', nn.BatchNorm2d(num_init_features))
        self.features.add_module('relu0', nn.ReLU(inplace=True))
        self.features.add_module('pool0', nn.MaxPool2d(kernel_size=3, stride=2, padding=1, ceil_mode=False))
    num_features = num_init_features
    for (i, num_layers) in enumerate(block_config):
        block = _DenseBlock(num_layers=num_layers, num_input_features=num_features, bn_size=bn_size, growth_rate=growth_rate, drop_rate=drop_rate, quant=quant, efficient=efficient)
        self.features.add_module(('denseblock%d' % (i + 1)), block)
        num_features = (num_features + (num_layers * growth_rate))
        if (i != (len(block_config) - 1)):
            trans = _Transition(num_input_features=num_features, num_output_features=int((num_features * compression)), quant=quant)
            self.features.add_module(('transition%d' % (i + 1)), trans)
            num_features = int((num_features * compression))
    self.features.add_module('norm_final', nn.BatchNorm2d(num_features))
    self.classifier = nn.Linear(num_features, num_classes)
    for (name, param) in self.named_parameters():
        if (('conv' in name) and ('weight' in name)):
            n = ((param.size(0) * param.size(2)) * param.size(3))
            param.data.normal_().mul_(math.sqrt((2.0 / n)))
        elif (('norm' in name) and ('weight' in name)):
            param.data.fill_(1)
        elif (('norm' in name) and ('bias' in name)):
            param.data.fill_(0)
        elif (('classifier' in name) and ('bias' in name)):
            param.data.fill_(0)
