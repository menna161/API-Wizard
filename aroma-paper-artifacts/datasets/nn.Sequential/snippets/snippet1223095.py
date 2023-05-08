import torch
import torch.nn as nn
from networks import layers


def conv_bn(channels_in, channels_out, stride):
    conv_block = nn.Sequential()
    conv_block.add_module('conv2d', layers.ConvBN(nc, in_channels=channels_in, out_channels=channels_out, kernel_size=3, stride=stride, padding=1))
    conv_block.add_module('relu', layers.NonLinear(nc, channels_out))
    return conv_block
