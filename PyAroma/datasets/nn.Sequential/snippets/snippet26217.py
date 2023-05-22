import time
import torch
import torch.nn as nn
import torchvision.models._utils as _utils
import torchvision.models as models
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self):
    super(MobileNetV1, self).__init__()
    self.stage1 = nn.Sequential(conv_bn(3, 8, 2, leaky=0.1), conv_dw(8, 16, 1), conv_dw(16, 32, 2), conv_dw(32, 32, 1), conv_dw(32, 64, 2), conv_dw(64, 64, 1))
    self.stage2 = nn.Sequential(conv_dw(64, 128, 2), conv_dw(128, 128, 1), conv_dw(128, 128, 1), conv_dw(128, 128, 1), conv_dw(128, 128, 1), conv_dw(128, 128, 1))
    self.stage3 = nn.Sequential(conv_dw(128, 256, 2), conv_dw(256, 256, 1))
    self.avg = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(256, 1000)
