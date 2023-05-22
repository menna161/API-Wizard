import torch
import torch.nn.functional as F
import torch.nn as nn
import math
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
import torch.utils.model_zoo as model_zoo


def __init__(self, output_stride=8, BatchNorm=None, width_mult=1.0, pretrained=True):
    super(MobileNetV2, self).__init__()
    block = InvertedResidual
    input_channel = 32
    current_stride = 1
    rate = 1
    interverted_residual_setting = [[1, 16, 1, 1], [6, 24, 2, 2], [6, 32, 3, 2], [6, 64, 4, 2], [6, 96, 3, 1], [6, 160, 3, 2], [6, 320, 1, 1]]
    input_channel = int((input_channel * width_mult))
    self.features = [conv_bn(3, input_channel, 2, BatchNorm)]
    current_stride *= 2
    for (t, c, n, s) in interverted_residual_setting:
        if (current_stride == output_stride):
            stride = 1
            dilation = rate
            rate *= s
        else:
            stride = s
            dilation = 1
            current_stride *= s
        output_channel = int((c * width_mult))
        for i in range(n):
            if (i == 0):
                self.features.append(block(input_channel, output_channel, stride, dilation, t, BatchNorm))
            else:
                self.features.append(block(input_channel, output_channel, 1, dilation, t, BatchNorm))
            input_channel = output_channel
    self.features = nn.Sequential(*self.features)
    self._initialize_weights()
    if pretrained:
        self._load_pretrained_model()
    self.low_level_features = self.features[0:4]
    self.high_level_features = self.features[4:]
