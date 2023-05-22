import math
import torch.nn as nn
from torch.nn.init import kaiming_normal_
import torchvision.transforms as transforms


def __init__(self, num_classes=10, depth=16, batch_norm=False):
    super(VGG, self).__init__()
    self.features = make_layers(cfg[depth], batch_norm)
    self.classifier = nn.Sequential(nn.Dropout(), nn.Linear(512, 512), nn.ReLU(True), nn.Dropout(), nn.Linear(512, 512), nn.ReLU(True), nn.Linear(512, num_classes))
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            kaiming_normal_(m.weight)
            m.bias.data.zero_()
