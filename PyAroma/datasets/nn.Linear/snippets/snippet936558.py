import torch.nn as nn
import math
from qtorch import FloatingPoint
from qtorch.quant import Quantizer


def __init__(self, quant, num_classes=10, depth=110):
    super(PreResNet, self).__init__()
    assert (((depth - 2) % 6) == 0), 'depth should be 6n+2'
    n = ((depth - 2) // 6)
    block = (Bottleneck if (depth >= 44) else BasicBlock)
    self.inplanes = 16
    self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1, bias=False)
    self.layer1 = self._make_layer(block, 16, n, quant)
    self.layer2 = self._make_layer(block, 32, n, quant, stride=2)
    self.layer3 = self._make_layer(block, 64, n, quant, stride=2)
    self.bn = nn.BatchNorm2d((64 * block.expansion))
    self.relu = nn.ReLU(inplace=True)
    self.avgpool = nn.AvgPool2d(8)
    self.fc = nn.Linear((64 * block.expansion), num_classes)
    self.quant = quant()
    IBM_half = FloatingPoint(exp=6, man=9)
    self.quant_half = Quantizer(IBM_half, IBM_half, 'nearest', 'nearest')
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
