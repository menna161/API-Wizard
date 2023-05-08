import torch.nn as nn
import torch
import os


def __init__(self, model_weight=None, num_classes=1000, width_mult=1.0):
    super(MobileNetV2, self).__init__()
    self.cfgs = [[1, 16, 1, 1], [6, 24, 2, 2], [6, 32, 3, 2], [6, 64, 4, 2], [6, 96, 3, 1], [6, 160, 3, 2], [6, 320, 1, 1]]
    input_channel = _make_divisible((32 * width_mult), (4 if (width_mult == 0.1) else 8))
    layers = [conv_3x3_bn(3, input_channel, 2)]
    for (t, c, n, s) in self.cfgs:
        output_channel = _make_divisible((c * width_mult), (4 if (width_mult == 0.1) else 8))
        layers.append(ResidualStage(input_channel, output_channel, s, n, t))
        input_channel = output_channel
    self.features = nn.Sequential(*layers)
    output_channel = (_make_divisible((1280 * width_mult), (4 if (width_mult == 0.1) else 8)) if (width_mult > 1.0) else 1280)
    self.conv = conv_1x1_bn(input_channel, output_channel)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.classifier = nn.Linear(output_channel, num_classes)
    self._initialize_weights(model_weight)