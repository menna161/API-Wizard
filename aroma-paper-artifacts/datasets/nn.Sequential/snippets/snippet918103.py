from copy import deepcopy
from nnunet.network_architecture.custom_modules.helperModules import Identity
from torch import nn


def __init__(self, input_channels, output_channels, kernel_size, network_props, num_convs, first_stride=None):
    "\n        if network_props['dropout_op'] is None then no dropout\n        if network_props['norm_op'] is None then no norm\n        :param input_channels:\n        :param output_channels:\n        :param kernel_size:\n        :param network_props:\n        "
    super(StackedConvLayers, self).__init__()
    network_props = deepcopy(network_props)
    network_props_first = deepcopy(network_props)
    if (first_stride is not None):
        network_props_first['conv_op_kwargs']['stride'] = first_stride
    self.convs = nn.Sequential(ConvDropoutNormReLU(input_channels, output_channels, kernel_size, network_props_first), *[ConvDropoutNormReLU(output_channels, output_channels, kernel_size, network_props) for _ in range((num_convs - 1))])
