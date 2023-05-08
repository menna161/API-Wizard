import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d


def __init__(self, backbone, output_stride, BatchNorm, pretrained):
    super(ASPP, self).__init__()
    if (backbone == 'drn'):
        inplanes = 512
    elif (backbone == 'mobilenet'):
        inplanes = 320
    else:
        inplanes = 2048
    if (output_stride == 16):
        dilations = [1, 6, 12, 18]
    elif (output_stride == 8):
        dilations = [1, 12, 24, 36]
    else:
        raise NotImplementedError
    self.aspp1 = _ASPPModule(inplanes, 256, 1, padding=0, dilation=dilations[0], BatchNorm=BatchNorm, pretrained=pretrained)
    self.aspp2 = _ASPPModule(inplanes, 256, 3, padding=dilations[1], dilation=dilations[1], BatchNorm=BatchNorm, pretrained=pretrained)
    self.aspp3 = _ASPPModule(inplanes, 256, 3, padding=dilations[2], dilation=dilations[2], BatchNorm=BatchNorm, pretrained=pretrained)
    self.aspp4 = _ASPPModule(inplanes, 256, 3, padding=dilations[3], dilation=dilations[3], BatchNorm=BatchNorm, pretrained=pretrained)
    self.global_avg_pool = nn.Sequential(nn.AdaptiveAvgPool2d((1, 1)), nn.Conv2d(inplanes, 256, 1, stride=1, bias=False), BatchNorm(256), nn.ReLU())
    self.conv1 = nn.Conv2d(1280, 256, 1, bias=False)
    self.bn1 = BatchNorm(256)
    self.relu = nn.ReLU()
    self.dropout = nn.Dropout(0.5)
    self._init_weight(pretrained)
