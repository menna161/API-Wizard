from torch import *
import torch.nn as nn
import torch
from torch.nn import *
import torch.nn.functional as F
import numpy as np


def __init__(self, input_channels, middle_channels, output_channels):
    '\n        Inititalises a FinalLayer object containing one layer applying the operations described above sequentially.\n        :param input_channels: number of channels of the input.\n        :param middle_channels: number of channels after the DoubleConvolution\n        :param output_channels: number of channels after the conv2d (here 2 because we have 2 classes)\n        '
    super(FinalLayer, self).__init__()
    self.conv = nn.Sequential(DoubleConvolutionLayer(input_channels, middle_channels), nn.Conv2d(middle_channels, output_channels, kernel_size=3, padding=1), nn.BatchNorm2d(output_channels), nn.Sigmoid())
