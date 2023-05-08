import torch
import torch.nn as nn
import numpy as np


def __init__(self, model_weight, block, layers, num_classes=1000, zero_init_residual=False, groups=1, width_per_group=64, replace_stride_with_dilation=None, norm_layer=None):
    super(ResNet, self).__init__()
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    self._norm_layer = norm_layer
    self.inplanes = 64
    self.dilation = 1
    index_list = list(np.load('../1_evaluate_filter_importance/index.npy'))
    channel_number = []
    for i in range(len(index_list)):
        tmp = index_list[i]
        channel_number.append(int(tmp.sum()))
    print(channel_number)
    self.channel_index = channel_number
    self.input_channel = self.inplanes
    if (replace_stride_with_dilation is None):
        replace_stride_with_dilation = [False, False, False]
    if (len(replace_stride_with_dilation) != 3):
        raise ValueError('replace_stride_with_dilation should be None or a 3-element tuple, got {}'.format(replace_stride_with_dilation))
    self.groups = groups
    self.base_width = width_per_group
    self.conv1 = nn.Conv2d(3, self.inplanes, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1 = norm_layer(self.inplanes)
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.layer1 = self._make_layer(block, 64, layers[0])
    self.layer2 = self._make_layer(block, 128, layers[1], stride=2, dilate=replace_stride_with_dilation[0])
    self.layer3 = self._make_layer(block, 256, layers[2], stride=2, dilate=replace_stride_with_dilation[1])
    self.layer4 = self._make_layer(block, 512, layers[3], stride=2, dilate=replace_stride_with_dilation[2])
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(self.input_channel, num_classes)
    self._initialize_weights(model_weight, index_list)
