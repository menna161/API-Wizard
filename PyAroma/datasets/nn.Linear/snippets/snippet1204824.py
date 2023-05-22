from __future__ import absolute_import
import torch
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    Model.check_parameters(params, {'name': 'InceptionV3'})
    BaseInceptionModel.__init__(self, params)
    self.features = nn.Sequential(ConvModule(3, num_filters=32, kernel_size=3, stride=2, padding=0), ConvModule(32, num_filters=32, kernel_size=3, stride=1, padding=0), ConvModule(32, num_filters=64, kernel_size=3, stride=1, padding=1), nn.MaxPool2d(kernel_size=3, stride=2), ConvModule(64, num_filters=80, kernel_size=1, stride=1, padding=0), ConvModule(80, num_filters=192, kernel_size=3, stride=1, padding=0), nn.MaxPool2d(kernel_size=3, stride=2), self.module_a(192, index=0, n=32), self.module_a(256, index=1, n=64), self.module_a(288, index=2, n=64), self.module_b(288, index=0), self.module_c(768, index=0, n=128), self.module_c(768, index=1, n=160), self.module_c(768, index=2, n=160), self.module_c(768, index=3, n=192), self.module_d(768, index=0), self.module_e(1280, index=0, pooltype='avg'), self.module_e(2048, index=1, pooltype='max'), nn.AvgPool2d(kernel_size=8, stride=1))
    self.classifier = nn.Sequential(nn.Dropout(p=0.2), nn.Linear(2048, self.num_classes))
