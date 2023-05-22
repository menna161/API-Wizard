import torch
import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo


def __init__(self, last_stride, block, layers, num_classes=1000):
    scale = 64
    self.inplanes = scale
    super(ResNet_IBN, self).__init__()
    self.conv1 = nn.Conv2d(3, scale, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = nn.BatchNorm2d(scale)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, scale, layers[0])
    self.layer2 = self._make_layer(block, (scale * 2), layers[1], stride=2)
    self.layer3 = self._make_layer(block, (scale * 4), layers[2], stride=2)
    self.layer4 = self._make_layer(block, (scale * 8), layers[3], stride=last_stride)
    self.avgpool = nn.AvgPool2d(7)
    self.fc = nn.Linear(((scale * 8) * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.InstanceNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
