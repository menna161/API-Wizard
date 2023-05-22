from __future__ import absolute_import
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    specs = ResNet.specs[params['model']]
    Model.check_parameters(params, {'name': specs['name'], 'input_shape': (3, 224, 224), 'num_classes': 1000, 'phase': 'training', 'dtype': 'float32'})
    Model.__init__(self, params)
    if (specs['num_layers'] >= 50):
        filter_list = [64, 256, 512, 1024, 2048]
        bottle_neck = True
    else:
        filter_list = [64, 64, 128, 256, 512]
        bottle_neck = False
    self.features = nn.Sequential(nn.Conv2d(3, filter_list[0], kernel_size=7, stride=2, padding=3, bias=False), nn.BatchNorm2d(filter_list[0], eps=2e-05, momentum=0.9, affine=True), nn.ReLU(inplace=True), nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
    num_prev_channels = filter_list[0]
    for i in range(len(specs['units'])):
        self.features.add_module(('stage%d_unit%d' % ((i + 1), 1)), ResnetModule(num_prev_channels, filter_list[(i + 1)], (1 if (i == 0) else 2), False, bottle_neck))
        num_prev_channels = filter_list[(i + 1)]
        for j in range((specs['units'][i] - 1)):
            self.features.add_module(('stage%d_unit%d' % ((i + 1), (j + 2))), ResnetModule(num_prev_channels, filter_list[(i + 1)], 1, True, bottle_neck))
    self.features.add_module('pool1', nn.AvgPool2d(kernel_size=7, padding=0))
    self.num_output_channels = filter_list[(- 1)]
    self.classifier = nn.Sequential(nn.Linear(self.num_output_channels, self.num_classes))
