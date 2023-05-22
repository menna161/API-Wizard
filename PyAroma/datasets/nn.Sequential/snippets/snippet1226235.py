import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d


def __init__(self, num_classes, backbone, BatchNorm):
    super(Decoder, self).__init__()
    if ((backbone == 'resnet') or (backbone == 'drn')):
        low_level_inplanes = 256
    elif (backbone == 'xception'):
        low_level_inplanes = 128
    elif (backbone == 'mobilenet'):
        low_level_inplanes = 24
    else:
        raise NotImplementedError
    self.conv1 = nn.Conv2d(low_level_inplanes, 48, 1, bias=False)
    self.bn1 = BatchNorm(48)
    self.relu = nn.ReLU()
    self.last_conv = nn.Sequential(nn.Conv2d(304, 256, kernel_size=3, stride=1, padding=1, bias=False), BatchNorm(256), nn.ReLU(), nn.Dropout(0.5), nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1, bias=False), BatchNorm(256), nn.ReLU(), nn.Dropout(0.1), nn.Conv2d(256, num_classes, kernel_size=1, stride=1))
    self._init_weight()
