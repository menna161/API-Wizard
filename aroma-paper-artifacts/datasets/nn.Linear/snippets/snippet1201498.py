import torch
from torch import nn
import torch.nn.functional as F
from .senet import se_resnext50_32x4d, senet154, se_resnext101_32x4d
from .dpn import dpn92


def _initialize_weights(self):
    for m in self.modules():
        if (isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d) or isinstance(m, nn.Linear)):
            m.weight.data = nn.init.kaiming_normal_(m.weight.data)
            if (m.bias is not None):
                m.bias.data.zero_()
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
