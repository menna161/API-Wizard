import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from functools import partial
from collections import OrderedDict
from config import config
from resnet import get_resnet50


def __init__(self, class_num, norm_layer, resnet_out=2048, feature=512, ThreeDinit=True, bn_momentum=0.1, pretrained_model=None, eval=False, freeze_bn=False):
    super(STAGE1, self).__init__()
    self.business_layer = []
    self.oper1 = nn.Sequential(nn.Conv3d(1, 3, kernel_size=3, padding=1, bias=False), norm_layer(3, momentum=bn_momentum), nn.ReLU(), nn.Conv3d(3, 64, kernel_size=3, padding=1, bias=False), norm_layer(64, momentum=bn_momentum), nn.ReLU(), nn.Conv3d(64, feature, kernel_size=3, padding=1, bias=False), norm_layer(feature, momentum=bn_momentum), nn.ReLU(inplace=False))
    self.business_layer.append(self.oper1)
    self.completion_layer1 = nn.Sequential(Bottleneck3D(feature, (feature // 4), bn_momentum=bn_momentum, expansion=4, stride=2, downsample=nn.Sequential(nn.AvgPool3d(kernel_size=2, stride=2), nn.Conv3d(feature, feature, kernel_size=1, stride=1, bias=False), norm_layer(feature, momentum=bn_momentum)), norm_layer=norm_layer), Bottleneck3D(feature, (feature // 4), bn_momentum=bn_momentum, norm_layer=norm_layer, dilation=[1, 1, 1]), Bottleneck3D(feature, (feature // 4), bn_momentum=bn_momentum, norm_layer=norm_layer, dilation=[2, 2, 2]), Bottleneck3D(feature, (feature // 4), bn_momentum=bn_momentum, norm_layer=norm_layer, dilation=[3, 3, 3]))
    self.business_layer.append(self.completion_layer1)
    self.completion_layer2 = nn.Sequential(Bottleneck3D(feature, (feature // 4), bn_momentum=bn_momentum, expansion=8, stride=2, downsample=nn.Sequential(nn.AvgPool3d(kernel_size=2, stride=2), nn.Conv3d(feature, (feature * 2), kernel_size=1, stride=1, bias=False), norm_layer((feature * 2), momentum=bn_momentum)), norm_layer=norm_layer), Bottleneck3D((feature * 2), (feature // 2), bn_momentum=bn_momentum, norm_layer=norm_layer, dilation=[1, 1, 1]), Bottleneck3D((feature * 2), (feature // 2), bn_momentum=bn_momentum, norm_layer=norm_layer, dilation=[2, 2, 2]), Bottleneck3D((feature * 2), (feature // 2), bn_momentum=bn_momentum, norm_layer=norm_layer, dilation=[3, 3, 3]))
    self.business_layer.append(self.completion_layer2)
    self.cvae = CVAE(norm_layer=norm_layer, bn_momentum=bn_momentum, latent_size=config.lantent_size)
    self.business_layer.append(self.cvae)
    self.classify_sketch = nn.ModuleList([nn.Sequential(nn.ConvTranspose3d((feature * 2), feature, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1), norm_layer(feature, momentum=bn_momentum), nn.ReLU(inplace=False)), nn.Sequential(nn.ConvTranspose3d(feature, feature, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1), norm_layer(feature, momentum=bn_momentum), nn.ReLU(inplace=False)), nn.Sequential(nn.Dropout3d(0.1), nn.Conv3d(feature, 2, kernel_size=1, bias=True))])
    self.business_layer.append(self.classify_sketch)
