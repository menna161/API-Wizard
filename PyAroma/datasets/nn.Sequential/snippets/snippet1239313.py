import torch
import torch.nn as nn
import torchvision
from . import resnet, resnext
from lib.nn import SynchronizedBatchNorm2d
from torch.nn import BatchNorm2d as SynchronizedBatchNorm2d
from functools import partial


def __init__(self, num_class=150, fc_dim=4096, inference=False, use_softmax=False, pool_scales=(1, 2, 3, 6)):
    super(PPMBilinearDeepsup, self).__init__()
    self.use_softmax = use_softmax
    self.inference = inference
    self.ppm = []
    for scale in pool_scales:
        self.ppm.append(nn.Sequential(nn.AdaptiveAvgPool2d(scale), nn.Conv2d(fc_dim, 512, kernel_size=1, bias=False), SynchronizedBatchNorm2d(512), nn.ReLU(inplace=True)))
    self.ppm = nn.ModuleList(self.ppm)
    self.cbr_deepsup = conv3x3_bn_relu((fc_dim // 2), (fc_dim // 4), 1)
    self.conv_last = nn.Sequential(nn.Conv2d((fc_dim + (len(pool_scales) * 512)), 512, kernel_size=3, padding=1, bias=False), SynchronizedBatchNorm2d(512), nn.ReLU(inplace=True), nn.Dropout2d(0.1), nn.Conv2d(512, num_class, kernel_size=1))
    self.conv_last_deepsup = nn.Conv2d((fc_dim // 4), num_class, 1, 1, 0)
    self.dropout_deepsup = nn.Dropout2d(0.1)
