from torch import *
import torch.nn as nn
import torch
from torch.nn import *
import torch.nn.functional as F
import numpy as np


def __init__(self, n_channels_input, n_channels_output):
    '\n        Initialises a DoubleConvolutionLayer object containing one layer that procedes to the operations described\n        above sequentially.\n        :param n_channels_input: number of channels in input\n        :param n_channels_output: number of channels in output\n        '
    super(DoubleConvolutionLayer, self).__init__()
    self.double_layer = nn.Sequential(nn.Conv2d(n_channels_input, n_channels_output, kernel_size=3, padding=1), nn.BatchNorm2d(n_channels_output), nn.ReLU(inplace=True), nn.Conv2d(n_channels_output, n_channels_output, kernel_size=3, padding=1), nn.BatchNorm2d(n_channels_output), nn.ReLU(inplace=True))
