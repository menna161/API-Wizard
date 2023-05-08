import math
import torch.nn as nn
import torchvision.transforms as transforms
from qtorch import FloatingPoint
from qtorch.quant import Quantizer


def __init__(self, quant=None, num_classes=10, depth=16, batch_norm=False):
    super(VGG, self).__init__()
    self.features = make_layers(cfg[depth], quant, batch_norm)
    IBM_half = FloatingPoint(exp=6, man=9)
    quant_half = (lambda : Quantizer(IBM_half, IBM_half, 'nearest', 'nearest'))
    self.classifier = nn.Sequential(quant_half(), nn.Dropout(), nn.Linear(512, 512), nn.ReLU(True), quant(), nn.Dropout(), nn.Linear(512, 512), nn.ReLU(True), quant(), nn.Linear(512, num_classes), quant_half())
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
            m.bias.data.zero_()
