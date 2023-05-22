import torch
import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import torch.distributed as dist


def __init__(self, block, layers, num_classes=1000, deep_stem=False, avg_down=False, bypass_last_bn=False):
    bypass_bn_weight_list = []
    self.inplanes = 64
    super(ResNet, self).__init__()
    self.deep_stem = deep_stem
    self.avg_down = avg_down
    if self.deep_stem:
        self.conv1 = nn.Sequential(nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False), nn.BatchNorm2d(32), nn.ReLU(inplace=True), nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(32), nn.ReLU(inplace=True), nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1, bias=False))
    else:
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = nn.BatchNorm2d(64)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 64, layers[0])
    self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
    self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
    self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
    self.avgpool = nn.AdaptiveAvgPool2d(1)
    self.fc = nn.Linear((512 * block.expansion), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
    if bypass_last_bn:
        for param in bypass_bn_weight_list:
            param.data.zero_()
        print('bypass {} bn.weight in BottleneckBlocks'.format(len(bypass_bn_weight_list)))
