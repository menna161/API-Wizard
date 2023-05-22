import torch
import torch.nn as nn


def __init__(self, model_weight, block, layers, num_classes=1000, zero_init_residual=False, groups=1, width_per_group=64, replace_stride_with_dilation=None, norm_layer=None):
    super(ResNet, self).__init__()
    if (norm_layer is None):
        norm_layer = nn.BatchNorm2d
    self._norm_layer = norm_layer
    self.inplanes = 64
    self.dilation = 1
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
    self.layer1 = ResidualStage(self.inplanes, block, 64, layers[0])
    self.inplanes = (64 * block.expansion)
    self.layer2 = ResidualStage(self.inplanes, block, 128, layers[1], stride=2, dilate=replace_stride_with_dilation[0])
    self.inplanes = (128 * block.expansion)
    self.layer3 = ResidualStage(self.inplanes, block, 256, layers[2], stride=2, dilate=replace_stride_with_dilation[1])
    self.inplanes = (256 * block.expansion)
    self.layer4 = ResidualStage(self.inplanes, block, 512, layers[3], stride=2, dilate=replace_stride_with_dilation[2])
    self.inplanes = (512 * block.expansion)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear((512 * block.expansion), num_classes)
    self._initialize_old_weights(model_weight)
