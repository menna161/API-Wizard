from __future__ import absolute_import
import torch
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    Model.check_parameters(params, {'name': 'InceptionV4'})
    BaseInceptionModel.__init__(self, params)
    self.features = nn.Sequential(ConvModule(3, num_filters=32, kernel_size=3, stride=2, padding=0), ConvModule(32, num_filters=32, kernel_size=3, stride=1, padding=0), ConvModule(32, num_filters=64, kernel_size=3, stride=1, padding=1), self.inception_v4_sa(64, index=0), self.inception_v4_sb(160, index=0), self.inception_v4_sc(192, index=0), self.inception_v4_a(384, index=0), self.inception_v4_a(384, index=1), self.inception_v4_a(384, index=2), self.inception_v4_a(384, index=3), self.inception_v4_ra(384, 0, 192, 224, 256, 384), self.inception_v4_b(1024, index=0), self.inception_v4_b(1024, index=1), self.inception_v4_b(1024, index=2), self.inception_v4_b(1024, index=3), self.inception_v4_b(1024, index=4), self.inception_v4_b(1024, index=5), self.inception_v4_b(1024, index=6), self.inception_v4_rb(1024, index=0), self.inception_v4_c(1536, index=0), self.inception_v4_c(1536, index=1), self.inception_v4_c(1536, index=2), nn.AvgPool2d(kernel_size=8, stride=1))
    self.classifier = nn.Sequential(nn.Dropout(p=0.2), nn.Linear(1536, self.num_classes))
