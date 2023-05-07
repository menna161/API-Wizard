import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo


def __init__(self, class_num, pretrained=True, output_stride=8, bn_momentum=0.1, freeze_bn=False):
    super().__init__()
    self.Resnet101 = resnet101(bn_momentum, pretrained, output_stride, multi=False)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear((512 * 4), class_num)
    if freeze_bn:
        self.freeze_bn()
        print('freeze bacth normalization successfully!')
