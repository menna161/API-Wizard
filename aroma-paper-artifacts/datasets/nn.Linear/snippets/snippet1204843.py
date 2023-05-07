from __future__ import absolute_import
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    Model.check_parameters(params, {'name': 'Overfeat', 'input_shape': (3, 231, 231), 'num_classes': 1000, 'phase': 'training', 'dtype': 'float32'})
    Model.__init__(self, params)
    self.features = nn.Sequential(nn.Conv2d(self.input_shape[0], 96, kernel_size=11, stride=4), nn.ReLU(inplace=True), nn.MaxPool2d(kernel_size=2, stride=2), nn.Conv2d(96, 256, kernel_size=5), nn.ReLU(inplace=True), nn.MaxPool2d(kernel_size=2, stride=2), nn.Conv2d(256, 512, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.Conv2d(512, 1024, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.Conv2d(1024, 1024, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(kernel_size=2, stride=2))
    self.classifier = nn.Sequential(nn.Linear(((1024 * 6) * 6), 3072), nn.ReLU(inplace=True), nn.Dropout(), nn.Linear(3072, 4096), nn.ReLU(inplace=True), nn.Dropout(), nn.Linear(4096, self.num_classes))
