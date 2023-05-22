from torch import nn
from torch.nn import functional as F
from networks.layers.quantization import Quantization
from networks.controller.network_controller import NetworkQuantizationController


def __init__(self, network_controller: NetworkQuantizationController, in_channels, out_channels):
    '\n        A fully connected module with HMQ quantization of the weights.\n        :param network_controller: The network quantization controller\n        :param in_channels: The number of input channels\n        :param out_channels: The number of output channels\n        '
    super(FullyConnected, self).__init__()
    self.network_controller = network_controller
    self.fc = nn.Linear(in_channels, out_channels)
    self.q = Quantization(network_controller, is_signed=True, weights_values=self.fc.weight.detach())
