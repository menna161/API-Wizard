import torch
from torch import nn
import torch.nn.functional as F
from .senet import se_resnext50_32x4d, senet154, se_resnext101_32x4d
from .dpn import dpn92


def __init__(self, channels, reduction=16, concat=False):
    super(SCSEModule, self).__init__()
    self.avg_pool = nn.AdaptiveAvgPool2d(1)
    self.fc1 = nn.Conv2d(channels, (channels // reduction), kernel_size=1, padding=0)
    self.relu = nn.ReLU(inplace=True)
    self.fc2 = nn.Conv2d((channels // reduction), channels, kernel_size=1, padding=0)
    self.sigmoid = nn.Sigmoid()
    self.spatial_se = nn.Sequential(nn.Conv2d(channels, 1, kernel_size=1, stride=1, padding=0, bias=False), nn.Sigmoid())
    self.concat = concat
