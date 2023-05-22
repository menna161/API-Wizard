import torch
from torch import nn
import torch.nn.functional as F
from .senet import se_resnext50_32x4d, senet154, se_resnext101_32x4d
from .dpn import dpn92


def __init__(self, in_channels, out_channels, kernel_size=3):
    super(ConvRelu, self).__init__()
    self.layer = nn.Sequential(nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, padding=1), nn.ReLU(inplace=True))
