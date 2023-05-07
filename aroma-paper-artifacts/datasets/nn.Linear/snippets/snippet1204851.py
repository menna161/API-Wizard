from __future__ import absolute_import
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    specs = VGG.specs[params['model']]
    Model.check_parameters(params, {'name': specs['name'], 'input_shape': (3, 224, 224), 'num_classes': 1000, 'phase': 'training', 'dtype': 'float32'})
    Model.__init__(self, params)
    self.features = nn.Sequential()
    (layers, filters) = specs['specs']
    prev_filters = self.input_shape[0]
    for (i, num) in enumerate(layers):
        for j in range(num):
            self.features.add_module(('conv%d_%d' % ((i + 1), (j + 1))), nn.Conv2d(prev_filters, filters[i], kernel_size=3, padding=1))
            self.features.add_module(('relu%d_%d' % ((i + 1), (j + 1))), nn.ReLU(inplace=True))
            prev_filters = filters[i]
        self.features.add_module(('pool%d' % (i + 1)), nn.MaxPool2d(kernel_size=2, stride=2))
    self.classifier = nn.Sequential(nn.Linear(((512 * 7) * 7), 4096), nn.ReLU(inplace=True), nn.Dropout(p=0.5), nn.Linear(4096, 4096), nn.ReLU(inplace=True), nn.Dropout(p=0.5), nn.Linear(4096, self.num_classes))
