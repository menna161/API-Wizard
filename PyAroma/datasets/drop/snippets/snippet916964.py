import torch
import torch.nn as nn
import torch.nn.functional as F
from pixelflow.layers import LambdaLayer, ElementwiseParams2d
from pixelflow.layers.autoregressive import MaskedConv2d


def forward(self, x):
    identity = x
    x = self.conv1(F.relu(x))
    x = self.conv2(F.relu(x))
    x = self.conv3(F.relu(x))
    return (self.drop(x) + identity)
