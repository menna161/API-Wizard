import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import torch.nn.functional as F
from resnet import channel_scale


def __init__(self, midplanes, inplanes, planes, stride=1, is_downsample=False):
    super(Bottleneck, self).__init__()
    expansion = 4
    norm_layer = nn.BatchNorm2d
    self.conv1 = conv1x1(inplanes, midplanes)
    self.bn1 = norm_layer(midplanes)
    self.conv2 = conv3x3(midplanes, midplanes, stride)
    self.bn2 = norm_layer(midplanes)
    self.conv3 = conv1x1(midplanes, planes)
    self.bn3 = norm_layer(planes)
    self.relu = nn.ReLU(inplace=True)
    self.stride = stride
    self.inplanes = inplanes
    self.planes = planes
    self.midplanes = midplanes
    self.is_downsample = is_downsample
    self.expansion = expansion
    if is_downsample:
        self.downsample = nn.Sequential(conv1x1(inplanes, planes, stride=stride), norm_layer(planes))
