import torch
import torch.nn as nn
from lib.sa.modules import Subtraction, Subtraction2, Aggregation


def __init__(self, sa_type, block, layers, kernels, num_classes):
    super(SAN, self).__init__()
    c = 64
    (self.conv_in, self.bn_in) = (conv1x1(3, c), nn.BatchNorm2d(c))
    (self.conv0, self.bn0) = (conv1x1(c, c), nn.BatchNorm2d(c))
    self.layer0 = self._make_layer(sa_type, block, c, layers[0], kernels[0])
    c *= 4
    (self.conv1, self.bn1) = (conv1x1((c // 4), c), nn.BatchNorm2d(c))
    self.layer1 = self._make_layer(sa_type, block, c, layers[1], kernels[1])
    c *= 2
    (self.conv2, self.bn2) = (conv1x1((c // 2), c), nn.BatchNorm2d(c))
    self.layer2 = self._make_layer(sa_type, block, c, layers[2], kernels[2])
    c *= 2
    (self.conv3, self.bn3) = (conv1x1((c // 2), c), nn.BatchNorm2d(c))
    self.layer3 = self._make_layer(sa_type, block, c, layers[3], kernels[3])
    c *= 2
    (self.conv4, self.bn4) = (conv1x1((c // 2), c), nn.BatchNorm2d(c))
    self.layer4 = self._make_layer(sa_type, block, c, layers[4], kernels[4])
    self.relu = nn.ReLU(inplace=True)
    self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(c, num_classes)
