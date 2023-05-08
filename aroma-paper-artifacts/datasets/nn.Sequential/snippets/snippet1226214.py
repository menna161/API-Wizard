import torch
import torch.nn as nn
import torch.nn.functional as F
from networks.deeplab.aspp import ASPP
from networks.deeplab.backbone.resnet import SEResNet50
from networks.correlation_package.correlation import Correlation
from networks.ltm_transfer import LTM_transfer


def __init__(self):
    super(ConverterEncoder, self).__init__()
    downsample1 = nn.Sequential(nn.Conv2d(512, 1024, kernel_size=1, stride=2, bias=False), nn.BatchNorm2d(1024))
    self.block1 = SEBottleneck(512, 256, stride=2, downsample=downsample1)
    downsample2 = nn.Sequential(nn.Conv2d(1024, 2048, kernel_size=1, stride=2, bias=False), nn.BatchNorm2d(2048))
    self.block2 = SEBottleneck(1024, 512, stride=2, downsample=downsample2)
    self.conv1x1 = nn.Conv2d((2048 * 2), 2048, kernel_size=1, padding=0)
