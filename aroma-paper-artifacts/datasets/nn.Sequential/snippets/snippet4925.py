from torch import *
import torch.nn as nn
import torch
from torch.nn import *
import torch.nn.functional as F
import numpy as np


def __init__(self, input_channels, middle_channels, output_channels):
    '\n        Initialises a BottleNeck object wich contains one layer applying the different operations sequentially.\n        :param input_channels: number of channels of the input\n        :param middle_channels: number of channels after the double convolution layer\n        :param output_channels: number of channels after the transposed convolution\n        '
    super(Bottleneck, self).__init__()
    self.layer = nn.Sequential(nn.MaxPool2d(2), DoubleConvolutionLayer(input_channels, middle_channels), nn.ConvTranspose2d(in_channels=middle_channels, out_channels=output_channels, kernel_size=3, stride=2, padding=1, output_padding=1))
