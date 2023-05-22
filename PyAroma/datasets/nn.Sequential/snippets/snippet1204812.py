from __future__ import absolute_import
import torch
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    ''
    Model.check_parameters(params, {'name': 'GoogleNet', 'input_shape': (3, 224, 224), 'num_classes': 1000, 'phase': 'training', 'dtype': 'float32'})
    Model.__init__(self, params)
    self.features = nn.Sequential(ConvModule(self.input_shape[0], 64, kernel_size=7, stride=2, padding=3), nn.MaxPool2d(kernel_size=3, stride=2), nn.LocalResponseNorm(size=5, alpha=0.0001, beta=0.75, k=2), ConvModule(64, 64, kernel_size=1, stride=1), ConvModule(64, 192, kernel_size=3, stride=1, padding=1), nn.LocalResponseNorm(size=5, alpha=0.0001, beta=0.75, k=2), nn.MaxPool2d(kernel_size=3, stride=2), InceptionModule(192, num_1x1=64, num_3x3red=96, num_3x3=128, num_d5x5red=16, num_d5x5=32, proj=32), InceptionModule(256, num_1x1=128, num_3x3red=128, num_3x3=192, num_d5x5red=32, num_d5x5=96, proj=64), nn.MaxPool2d(kernel_size=3, stride=2), InceptionModule(480, num_1x1=192, num_3x3red=96, num_3x3=208, num_d5x5red=16, num_d5x5=48, proj=64), InceptionModule(512, num_1x1=160, num_3x3red=112, num_3x3=224, num_d5x5red=24, num_d5x5=64, proj=64), InceptionModule(512, num_1x1=128, num_3x3red=128, num_3x3=256, num_d5x5red=24, num_d5x5=64, proj=64), InceptionModule(512, num_1x1=112, num_3x3red=144, num_3x3=288, num_d5x5red=32, num_d5x5=64, proj=64), InceptionModule(528, num_1x1=256, num_3x3red=160, num_3x3=320, num_d5x5red=32, num_d5x5=128, proj=128), nn.MaxPool2d(kernel_size=3, stride=2, padding=1), InceptionModule(832, num_1x1=256, num_3x3red=160, num_3x3=320, num_d5x5red=32, num_d5x5=128, proj=128), InceptionModule(832, num_1x1=384, num_3x3red=192, num_3x3=384, num_d5x5red=48, num_d5x5=128, proj=128), nn.AvgPool2d(kernel_size=7, stride=1))
    self.classifier = nn.Sequential(nn.Dropout(), nn.Linear(1024, self.num_classes))
