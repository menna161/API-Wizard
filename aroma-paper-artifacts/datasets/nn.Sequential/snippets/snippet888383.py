import torch
import torch.nn as nn


def _make_dense_layers(self, block, in_channels, nblocks):
    dense_block = nn.Sequential()
    for index in range(nblocks):
        dense_block.add_module('bottle_neck_layer_{}'.format(index), block(in_channels, self.growth_rate))
        in_channels += self.growth_rate
    return dense_block
