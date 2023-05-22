import torch
import torch.nn as nn
from .wage_initializer import wage_init_
from qtorch.quant import fixed_point_quantize
from qtorch import FixedPoint
import math


def __init__(self, quantizer, wl_activate, wl_error, num_classes=10, depth=16, batch_norm=False, wl_weight=(- 1), writer=None):
    super(VGG, self).__init__()
    quant = (lambda : quantizer(wl_activate, wl_error))
    self.features = nn.Sequential(*[quantizer(wl_activate, (- 1)), nn.Conv2d(3, 128, kernel_size=3, padding=1, bias=False), nn.ReLU(inplace=True), quant(), nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False), nn.MaxPool2d(kernel_size=2, stride=2), nn.ReLU(inplace=True), quant(), nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False), nn.ReLU(inplace=True), quant(), nn.Conv2d(256, 256, kernel_size=3, padding=1, bias=False), nn.MaxPool2d(kernel_size=2, stride=2), nn.ReLU(inplace=True), quant(), nn.Conv2d(256, 512, kernel_size=3, padding=1, bias=False), nn.ReLU(inplace=True), quant(), nn.Conv2d(512, 512, kernel_size=3, padding=1, bias=False), nn.MaxPool2d(kernel_size=2, stride=2), nn.ReLU(inplace=True), quant()])
    self.classifier = nn.Sequential(nn.Linear(8192, 1024, bias=False), nn.ReLU(inplace=True), quant(), nn.Linear(1024, num_classes, bias=False), quantizer((- 1), wl_error))
    self.weight_scale = {}
    self.weight_acc = {}
    for (name, param) in self.named_parameters():
        assert ('weight' in name)
        wage_init_(param, wl_weight, name, self.weight_scale, factor=1.0)
        self.weight_acc[name] = param.data
