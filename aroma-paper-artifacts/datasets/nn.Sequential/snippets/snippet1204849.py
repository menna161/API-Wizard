from __future__ import absolute_import
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    Model.check_parameters(params, {'name': 'SensorNet', 'input_shape': 784, 'num_classes': 16, 'phase': 'training', 'dtype': 'float32'})
    Model.__init__(self, params)
    self.model = nn.Sequential()
    prev_size = self.input_shape[0]
    for (idx, layer_size) in enumerate([1024, 1024, 1024]):
        self.model.add_module(('linear_%d' % idx), nn.Linear(prev_size, layer_size))
        self.model.add_module(('relu_%d' % idx), nn.ReLU(inplace=True))
        prev_size = layer_size
    self.model.add_module('classifier', nn.Linear(prev_size, self.num_classes))
