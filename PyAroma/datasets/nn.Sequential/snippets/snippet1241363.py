import os
import torch
import torch.nn as nn
import torchvision.models
import collections
import math
import torch.nn.functional as F
import imagenet.mobilenet
from collections import OrderedDict
from collections import OrderedDict
from collections import OrderedDict


def __init__(self, decoder, output_size, in_channels=3, pretrained=True):
    super(MobileNet, self).__init__()
    self.output_size = output_size
    mobilenet = imagenet.mobilenet.MobileNet()
    if pretrained:
        pretrained_path = os.path.join('imagenet', 'results', 'imagenet.arch=mobilenet.lr=0.1.bs=256', 'model_best.pth.tar')
        checkpoint = torch.load(pretrained_path)
        state_dict = checkpoint['state_dict']
        from collections import OrderedDict
        new_state_dict = OrderedDict()
        for (k, v) in state_dict.items():
            name = k[7:]
            new_state_dict[name] = v
        mobilenet.load_state_dict(new_state_dict)
    else:
        mobilenet.apply(weights_init)
    if (in_channels == 3):
        self.mobilenet = nn.Sequential(*(mobilenet.model[i] for i in range(14)))
    else:

        def conv_bn(inp, oup, stride):
            return nn.Sequential(nn.Conv2d(inp, oup, 3, stride, 1, bias=False), nn.BatchNorm2d(oup), nn.ReLU6(inplace=True))
        self.mobilenet = nn.Sequential(conv_bn(in_channels, 32, 2), *(mobilenet.model[i] for i in range(1, 14)))
    self.decoder = choose_decoder(decoder)
