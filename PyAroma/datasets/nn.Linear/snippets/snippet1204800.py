from __future__ import absolute_import
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    Model.check_parameters(params, {'name': 'AcousticModel', 'input_shape': 540, 'num_classes': 8192, 'phase': 'training', 'dtype': 'float32'})
    Model.__init__(self, params)
    self.model = nn.Sequential()
    prev_size = self.input_shape[0]
    for idx in range(5):
        self.model.add_module(('linear_%d' % idx), nn.Linear(prev_size, 2048))
        self.model.add_module(('relu_%d' % idx), nn.ReLU(inplace=True))
        prev_size = 2048
    self.model.add_module('classifier', nn.Linear(prev_size, self.num_classes))
