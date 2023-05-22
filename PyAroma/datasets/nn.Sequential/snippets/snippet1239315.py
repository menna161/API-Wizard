import torch
import torch.nn as nn
import torchvision
from . import resnet, resnext
from lib.nn import SynchronizedBatchNorm2d
from torch.nn import BatchNorm2d as SynchronizedBatchNorm2d
from functools import partial


def __init__(self, num_class=150, fc_dim=4096, inference=False, use_softmax=False, pool_scales=(1, 2, 3, 6), fpn_inplanes=(256, 512, 1024, 2048), fpn_dim=256):
    super(UPerNet, self).__init__()
    self.use_softmax = use_softmax
    self.inference = inference
    self.ppm_pooling = []
    self.ppm_conv = []
    for scale in pool_scales:
        self.ppm_pooling.append(nn.AdaptiveAvgPool2d(scale))
        self.ppm_conv.append(nn.Sequential(nn.Conv2d(fc_dim, 512, kernel_size=1, bias=False), SynchronizedBatchNorm2d(512), nn.ReLU(inplace=True)))
    self.ppm_pooling = nn.ModuleList(self.ppm_pooling)
    self.ppm_conv = nn.ModuleList(self.ppm_conv)
    self.ppm_last_conv = conv3x3_bn_relu((fc_dim + (len(pool_scales) * 512)), fpn_dim, 1)
    self.fpn_in = []
    for fpn_inplane in fpn_inplanes[:(- 1)]:
        self.fpn_in.append(nn.Sequential(nn.Conv2d(fpn_inplane, fpn_dim, kernel_size=1, bias=False), SynchronizedBatchNorm2d(fpn_dim), nn.ReLU(inplace=True)))
    self.fpn_in = nn.ModuleList(self.fpn_in)
    self.fpn_out = []
    for i in range((len(fpn_inplanes) - 1)):
        self.fpn_out.append(nn.Sequential(conv3x3_bn_relu(fpn_dim, fpn_dim, 1)))
    self.fpn_out = nn.ModuleList(self.fpn_out)
    self.conv_last = nn.Sequential(conv3x3_bn_relu((len(fpn_inplanes) * fpn_dim), fpn_dim, 1), nn.Conv2d(fpn_dim, num_class, kernel_size=1))
