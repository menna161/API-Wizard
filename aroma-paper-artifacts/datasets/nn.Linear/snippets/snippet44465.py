from torch import nn
from models_lpf import *


def __init__(self, num_classes=1000, width_mult=1.0, filter_size=1):
    super(MobileNetV2, self).__init__()
    block = InvertedResidual
    input_channel = 32
    last_channel = 1280
    inverted_residual_setting = [[1, 16, 1, 1], [6, 24, 2, 2], [6, 32, 3, 2], [6, 64, 4, 2], [6, 96, 3, 1], [6, 160, 3, 2], [6, 320, 1, 1]]
    input_channel = int((input_channel * width_mult))
    self.last_channel = int((last_channel * max(1.0, width_mult)))
    features = [ConvBNReLU(3, input_channel, stride=2)]
    for (t, c, n, s) in inverted_residual_setting:
        output_channel = int((c * width_mult))
        for i in range(n):
            stride = (s if (i == 0) else 1)
            features.append(block(input_channel, output_channel, stride, expand_ratio=t, filter_size=filter_size))
            input_channel = output_channel
    features.append(ConvBNReLU(input_channel, self.last_channel, kernel_size=1))
    self.features = nn.Sequential(*features)
    self.classifier = nn.Sequential(nn.Linear(self.last_channel, num_classes))
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out')
            if (m.bias is not None):
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.ones_(m.weight)
            nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, 0, 0.01)
            nn.init.zeros_(m.bias)
