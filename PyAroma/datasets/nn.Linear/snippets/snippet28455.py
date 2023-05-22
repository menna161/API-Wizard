import math
import torch.nn as nn
import torch.nn.functional as F
from layers.ModulatedAttLayer import ModulatedAttLayer


def __init__(self, block, layers, use_modulatedatt=False, use_fc=False, dropout=None):
    self.inplanes = 64
    super(ResNet, self).__init__()
    self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = nn.BatchNorm2d(64)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 64, layers[0])
    self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
    self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
    self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
    self.avgpool = nn.AvgPool2d(7, stride=1)
    self.use_fc = use_fc
    self.use_dropout = (True if dropout else False)
    if self.use_fc:
        print('Using fc.')
        self.fc_add = nn.Linear((512 * block.expansion), 512)
    if self.use_dropout:
        print('Using dropout.')
        self.dropout = nn.Dropout(p=dropout)
    self.use_modulatedatt = use_modulatedatt
    if self.use_modulatedatt:
        print('Using self attention.')
        self.modulatedatt = ModulatedAttLayer(in_channels=(512 * block.expansion))
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
