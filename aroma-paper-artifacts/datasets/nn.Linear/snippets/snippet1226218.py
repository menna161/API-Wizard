import torch
import torch.nn as nn
import torch.nn.functional as F
from networks.deeplab.aspp import ASPP
from networks.deeplab.backbone.resnet import SEResNet50
from networks.correlation_package.correlation import Correlation
from networks.ltm_transfer import LTM_transfer


def __init__(self, channel, reduction=16):
    super(SELayer, self).__init__()
    self.avg_pool = nn.AdaptiveAvgPool2d(1)
    self.fc = nn.Sequential(nn.Linear(channel, (channel // reduction), bias=False), nn.ReLU(inplace=True), nn.Linear((channel // reduction), channel, bias=False), nn.Sigmoid())
