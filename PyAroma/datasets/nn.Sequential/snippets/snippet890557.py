import torch.nn as nn
from octconv import *


def __init__(self, num_classes=1000):
    super(OctMobileNet, self).__init__()
    self.features = nn.Sequential(conv_bn(3, 32, 2), conv_dw(32, 64, 1, 0, 0.5), conv_dw(64, 128, 2), conv_dw(128, 128, 1), conv_dw(128, 256, 2), conv_dw(256, 256, 1), conv_dw(256, 512, 2), conv_dw(512, 512, 1), conv_dw(512, 512, 1), conv_dw(512, 512, 1), conv_dw(512, 512, 1), conv_dw(512, 512, 1, 0.5, 0), conv_dw(512, 1024, 2, 0, 0), conv_dw(1024, 1024, 1, 0, 0))
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(1024, num_classes)
