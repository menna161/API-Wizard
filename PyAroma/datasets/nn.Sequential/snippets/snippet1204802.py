from __future__ import absolute_import
import torch.nn as nn
from pytorch_benchmarks.models.model import Model


def __init__(self, params):
    Model.check_parameters(params, {'name': 'AlexNet', 'input_shape': (3, 227, 227), 'num_classes': 1000, 'phase': 'training', 'dtype': 'float32'})
    Model.__init__(self, params)
    self.features = nn.Sequential(nn.Conv2d(3, 96, kernel_size=11, stride=4), nn.ReLU(inplace=True), nn.LocalResponseNorm(size=5, alpha=0.0001, beta=0.75, k=2), nn.MaxPool2d(kernel_size=3, stride=2), nn.Conv2d(96, 256, kernel_size=5, padding=2), nn.ReLU(inplace=True), nn.LocalResponseNorm(size=5, alpha=0.0001, beta=0.75, k=2), nn.MaxPool2d(kernel_size=3, stride=2), nn.Conv2d(256, 384, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.Conv2d(384, 384, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.Conv2d(384, 256, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(kernel_size=3, stride=2))
    self.classifier = nn.Sequential(nn.Linear(((256 * 6) * 6), 4096), nn.ReLU(inplace=True), nn.Dropout(), nn.Linear(4096, 4096), nn.ReLU(inplace=True), nn.Dropout(), nn.Linear(4096, self.num_classes))
