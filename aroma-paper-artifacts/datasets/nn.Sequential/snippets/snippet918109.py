from copy import deepcopy
from nnunet.network_architecture.custom_modules.helperModules import Identity
from torch import nn


def __init__(self, input_channels, output_channels, kernel_size, network_props, num_blocks, first_stride=None, block=BasicResidualBlock):
    super().__init__()
    network_props = deepcopy(network_props)
    self.convs = nn.Sequential(block(input_channels, output_channels, kernel_size, network_props, first_stride), *[block(output_channels, output_channels, kernel_size, network_props) for _ in range((num_blocks - 1))])
