from copy import deepcopy
from nnunet.network_architecture.custom_modules.helperModules import Identity
from torch import nn


def __init__(self, input_channels, output_channels, kernel_size, network_props):
    "\n        if network_props['dropout_op'] is None then no dropout\n        if network_props['norm_op'] is None then no norm\n        :param input_channels:\n        :param output_channels:\n        :param kernel_size:\n        :param network_props:\n        "
    super(ConvDropoutNormReLU, self).__init__()
    network_props = deepcopy(network_props)
    self.conv = network_props['conv_op'](input_channels, output_channels, kernel_size, padding=[((i - 1) // 2) for i in kernel_size], **network_props['conv_op_kwargs'])
    if (network_props['dropout_op'] is not None):
        self.do = network_props['dropout_op'](**network_props['dropout_op_kwargs'])
    else:
        self.do = Identity()
    if (network_props['norm_op'] is not None):
        self.norm = network_props['norm_op'](output_channels, **network_props['norm_op_kwargs'])
    else:
        self.norm = Identity()
    self.nonlin = network_props['nonlin'](**network_props['nonlin_kwargs'])
    self.all = nn.Sequential(self.conv, self.do, self.norm, self.nonlin)
