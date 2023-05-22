import torch
import torch.nn as nn
import torch.nn.functional as F
from networks.deeplab.aspp import ASPP
from networks.deeplab.backbone.resnet import SEResNet50
from networks.correlation_package.correlation import Correlation
from networks.ltm_transfer import LTM_transfer


def _initialize_weights(self, pretrained):
    for m in self.modules():
        if pretrained:
            break
        elif isinstance(m, nn.Conv2d):
            m.weight.data.normal_(0, 0.001)
            if (m.bias is not None):
                m.bias.data.zero_()
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.weight.data.normal_(0, 0.01)
            m.bias.data.zero_()
