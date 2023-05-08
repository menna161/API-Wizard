import torch.nn as nn
from base.base_net import BaseNet
from networks.cbam import CBAM
from torch.nn import init


def __init__(self, rep_dim=256):
    self.inplanes = 64
    super().__init__()
    self.rep_dim = rep_dim
    att_type = 'CBAM'
    layers = [2, 2, 2, 2]
    self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.avgpool = nn.AvgPool2d(7)
    self.bn1 = nn.BatchNorm2d(64)
    self.relu = nn.ReLU(inplace=True)
    (self.bam1, self.bam2, self.bam3) = (None, None, None)
    self.layer1 = self._make_layer(BasicBlock, 64, layers[0], att_type=att_type)
    self.layer2 = self._make_layer(BasicBlock, 128, layers[1], stride=2, att_type=att_type)
    self.layer3 = self._make_layer(BasicBlock, 256, layers[2], stride=2, att_type=att_type)
    self.layer4 = self._make_layer(BasicBlock, 512, layers[3], stride=2, att_type=att_type)
    self.fc = nn.Linear((512 * BasicBlock.expansion), self.rep_dim)
    init.kaiming_normal_(self.fc.weight)
    for key in self.state_dict():
        if (key.split('.')[(- 1)] == 'weight'):
            if ('conv' in key):
                init.kaiming_normal_(self.state_dict()[key], mode='fan_out')
            if ('bn' in key):
                if ('SpatialGate' in key):
                    self.state_dict()[key][...] = 0
                else:
                    self.state_dict()[key][...] = 1
        elif (key.split('.')[(- 1)] == 'bias'):
            self.state_dict()[key][...] = 0
