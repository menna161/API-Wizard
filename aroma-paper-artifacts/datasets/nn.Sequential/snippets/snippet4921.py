from torch import *
import torch.nn as nn
import torch
from torch.nn import *
import torch.nn.functional as F
import numpy as np


def __init__(self, input_channels, output_channels):
    '\n        Initialise a Downscaling_layer that takes input_channels as number of input channels and produces an output\n        with the desired output_channels.\n        We only define one layer which applies the maxPool and the DoubleConvolutionLayer sequentially.\n        :param input_channels: number of input channels\n        :param output_channels: number of output channels\n        '
    super(Downscaling_layer, self).__init__()
    self.layer = nn.Sequential(nn.MaxPool2d(2), DoubleConvolutionLayer(input_channels, output_channels))
