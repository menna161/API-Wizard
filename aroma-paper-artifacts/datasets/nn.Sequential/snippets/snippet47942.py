from collections import OrderedDict
import torch
import torch.nn as nn


def __init__(self, nb_layers, in_planes, out_planes, block_type, batchnorm=1e-05, stride=1, is_transposed=False):
    super(WRNNetworkBlock, self).__init__()
    if is_transposed:
        self.block = nn.Sequential(OrderedDict([(('convT_block' + str((layer + 1))), block_type((((layer == 0) and in_planes) or out_planes), out_planes, (((layer == 0) and stride) or 1), batchnorm=batchnorm, is_transposed=(layer == 0))) for layer in range(nb_layers)]))
    else:
        self.block = nn.Sequential(OrderedDict([(('conv_block' + str((layer + 1))), block_type((((layer == 0) and in_planes) or out_planes), out_planes, (((layer == 0) and stride) or 1), batchnorm=batchnorm)) for layer in range(nb_layers)]))
