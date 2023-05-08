import torch.nn as nn
import math
import functools
from condconv import CondConv2d, route_func


def __init__(self, num_classes=1000, width_mult=1.0, num_experts=8):
    super(CondMobileNetV2, self).__init__()
    self.cfgs = [[1, 16, 1, 1], [6, 24, 2, 2], [6, 32, 3, 2], [6, 64, 4, 2], [6, 96, 3, 1], [6, 160, 3, 2], [6, 320, 1, 1]]
    input_channel = _make_divisible((32 * width_mult), 8)
    layers = [conv_3x3_bn(3, input_channel, 2)]
    block = InvertedResidual
    self.num_experts = None
    for (j, (t, c, n, s)) in enumerate(self.cfgs):
        output_channel = _make_divisible((c * width_mult), 8)
        for i in range(n):
            layers.append(block(input_channel, output_channel, (s if (i == 0) else 1), t, self.num_experts))
            input_channel = output_channel
            if ((j == 4) and (i == 0)):
                self.num_experts = num_experts
    self.features = nn.Sequential(*layers)
    output_channel = (_make_divisible((1280 * width_mult), 8) if (width_mult > 1.0) else 1280)
    self.conv = conv_1x1_bn(input_channel, output_channel)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.classifier_route = route_func(output_channel, num_experts)
    self.classifier = CondConv2d(output_channel, num_classes, kernel_size=1, bias=False, num_experts=num_experts)
    self._initialize_weights()
