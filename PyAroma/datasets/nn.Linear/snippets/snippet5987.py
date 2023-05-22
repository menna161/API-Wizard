import math
import torch.nn as nn
from collections import OrderedDict
import torch.utils.model_zoo as model_zoo
from torchvision.models.resnet import BasicBlock, Bottleneck, model_urls


def __init__(self, block, layers, output_layers, num_classes=1000, inplanes=64):
    self.inplanes = inplanes
    super(ResNet_comb4, self).__init__()
    self.output_layers = output_layers
    self.conv1 = nn.Conv2d(4, inplanes, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = nn.BatchNorm2d(inplanes)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, inplanes, layers[0])
    self.layer2 = self._make_layer(block, (inplanes * 2), layers[1], stride=2)
    self.layer3 = self._make_layer(block, (inplanes * 4), layers[2], stride=2)
    self.layer4 = self._make_layer(block, (inplanes * 8), layers[3], stride=2)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(((inplanes * 8) * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
