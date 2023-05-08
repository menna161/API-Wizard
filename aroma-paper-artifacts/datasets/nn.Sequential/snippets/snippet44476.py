import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from models_lpf import *


def __init__(self, inplanes, planes, stride=1, downsample=None, groups=1, norm_layer=None, filter_size=1):
    super(BasicBlock, self).__init__()
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    if (groups != 1):
        raise ValueError('BasicBlock only supports groups=1')
    self.conv1 = conv3x3(inplanes, planes)
    self.bn1 = norm_layer(planes)
    self.relu = nn.ReLU(inplace=True)
    if (stride == 1):
        self.conv2 = conv3x3(planes, planes)
    else:
        self.conv2 = nn.Sequential(Downsample(filt_size=filter_size, stride=stride, channels=planes), conv3x3(planes, planes))
    self.bn2 = norm_layer(planes)
    self.downsample = downsample
    self.stride = stride
