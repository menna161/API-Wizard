import torch
import torch.nn as nn


def __init__(self, block, nblocks, growth_rate=12, reduction=0.5, num_class=100):
    super().__init__()
    self.growth_rate = growth_rate
    inner_channels = (2 * growth_rate)
    self.conv1 = nn.Conv2d(3, inner_channels, kernel_size=3, padding=1, bias=False)
    self.features = nn.Sequential()
    for index in range((len(nblocks) - 1)):
        self.features.add_module('dense_block_layer_{}'.format(index), self._make_dense_layers(block, inner_channels, nblocks[index]))
        inner_channels += (growth_rate * nblocks[index])
        out_channels = int((reduction * inner_channels))
        self.features.add_module('transition_layer_{}'.format(index), Transition(inner_channels, out_channels))
        inner_channels = out_channels
    self.features.add_module('dense_block{}'.format((len(nblocks) - 1)), self._make_dense_layers(block, inner_channels, nblocks[(len(nblocks) - 1)]))
    inner_channels += (growth_rate * nblocks[(len(nblocks) - 1)])
    self.features.add_module('bn', nn.BatchNorm2d(inner_channels))
    self.features.add_module('relu', nn.ReLU(inplace=True))
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.linear = nn.Linear(inner_channels, num_class)
