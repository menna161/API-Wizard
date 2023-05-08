import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import torch.nn.functional as F
from resnet import channel_scale


def __init__(self, ids, num_classes=1000):
    super(resnet50, self).__init__()
    (overall_channel, mid_channel) = adapt_channel(ids)
    layer_num = 0
    self.conv1 = nn.Conv2d(3, overall_channel[layer_num], kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = nn.BatchNorm2d(overall_channel[layer_num])
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layers = nn.ModuleList()
    layer_num += 1
    for i in range(len(stage_repeat)):
        if (i == 0):
            self.layers.append(Bottleneck(mid_channel[(layer_num - 1)], overall_channel[(layer_num - 1)], overall_channel[layer_num], stride=1, is_downsample=True))
            layer_num += 1
        else:
            self.layers.append(Bottleneck(mid_channel[(layer_num - 1)], overall_channel[(layer_num - 1)], overall_channel[layer_num], stride=2, is_downsample=True))
            layer_num += 1
        for j in range(1, stage_repeat[i]):
            self.layers.append(Bottleneck(mid_channel[(layer_num - 1)], overall_channel[(layer_num - 1)], overall_channel[layer_num]))
            layer_num += 1
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(2048, num_classes)
