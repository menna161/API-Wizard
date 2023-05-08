import math
import torch.nn as nn
import torchvision.transforms as transforms


def __init__(self, num_classes=10, depth=16, batch_norm=False):
    super(VGG, self).__init__()
    self.features = make_layers(cfg[depth], batch_norm)
    self.classifier = nn.Sequential(nn.Dropout(), nn.Linear(512, 512), nn.ReLU(True), nn.Dropout(), nn.Linear(512, 512), nn.ReLU(True), nn.Linear(512, num_classes))
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
            m.bias.data.zero_()
