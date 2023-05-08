import torch
import torch.nn as nn
from networks import layers


def conv_dw(channels_in, channels_out, stride):
    conv_block = nn.Sequential()
    conv_block.add_module('dw_conv', layers.ConvBN(nc, in_channels=channels_in, out_channels=channels_in, kernel_size=3, stride=stride, padding=1, group=channels_in))
    conv_block.add_module('relu_0', layers.NonLinear(nc, channels_in))
    conv_block.add_module('conv', layers.ConvBN(nc, in_channels=channels_in, out_channels=channels_out, kernel_size=1, stride=1, padding=0))
    conv_block.add_module('relu_1', layers.NonLinear(nc, channels_out))
    return conv_block
