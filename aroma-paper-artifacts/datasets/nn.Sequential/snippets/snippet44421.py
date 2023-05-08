import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from models_fconv_lpf import *


def __init__(self, inplanes, planes, stride=1, downsample=None, groups=1, norm_layer=None, filter_size=1):
    super(Bottleneck, self).__init__()
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    self.conv1 = conv1x1(inplanes, planes)
    self.bn1 = norm_layer(planes)
    self.conv2 = conv3x3(planes, planes, groups)
    self.bn2 = norm_layer(planes)
    if (stride == 1):
        self.conv3 = conv1x1(planes, (planes * self.expansion))
    else:
        self.conv3 = nn.Sequential(Downsample(filt_size=filter_size, stride=stride, channels=planes), conv1x1(planes, (planes * self.expansion)))
    self.bn3 = norm_layer((planes * self.expansion))
    self.relu = nn.ReLU(inplace=True)
    self.downsample = downsample
    self.stride = stride
    self.down_pad = nn.ZeroPad2d(1)
    self.normal_pad = nn.ZeroPad2d(1)
