from __future__ import division
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init


def block(self, name, in_channels, out_channels, pool_stride=2):
    ' Stack n bottleneck modules where n is inferred from the depth of the network.\n\n        Args:\n            name: string name of the current block.\n            in_channels: number of input channels\n            out_channels: number of output channels\n            pool_stride: factor to reduce the spatial dimensionality in the first bottleneck of the block.\n\n        Returns: a Module consisting of n sequential bottlenecks.\n\n        '
    block = nn.Sequential()
    for bottleneck in range(self.block_depth):
        name_ = ('%s_bottleneck_%d' % (name, bottleneck))
        if (bottleneck == 0):
            block.add_module(name_, ResNeXtBottleneck(in_channels, out_channels, pool_stride, self.cardinality, self.base_width, self.widen_factor))
        else:
            block.add_module(name_, ResNeXtBottleneck(out_channels, out_channels, 1, self.cardinality, self.base_width, self.widen_factor))
    return block
