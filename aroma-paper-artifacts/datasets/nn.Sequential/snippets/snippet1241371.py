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


def __init__(self, output_size, pretrained=True):
    super(MobileNetSkipConcat, self).__init__()
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
    for i in range(14):
        setattr(self, 'conv{}'.format(i), mobilenet.model[i])
    kernel_size = 5
    self.decode_conv1 = nn.Sequential(depthwise(1024, kernel_size), pointwise(1024, 512))
    self.decode_conv2 = nn.Sequential(depthwise(512, kernel_size), pointwise(512, 256))
    self.decode_conv3 = nn.Sequential(depthwise(512, kernel_size), pointwise(512, 128))
    self.decode_conv4 = nn.Sequential(depthwise(256, kernel_size), pointwise(256, 64))
    self.decode_conv5 = nn.Sequential(depthwise(128, kernel_size), pointwise(128, 32))
    self.decode_conv6 = pointwise(32, 1)
    weights_init(self.decode_conv1)
    weights_init(self.decode_conv2)
    weights_init(self.decode_conv3)
    weights_init(self.decode_conv4)
    weights_init(self.decode_conv5)
    weights_init(self.decode_conv6)
