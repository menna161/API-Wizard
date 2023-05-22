import torch
import torch.nn as nn
from lib.ssn.ssn import ssn_iter, sparse_ssn_iter


def __init__(self, feature_dim, nspix, n_iter=10):
    super().__init__()
    self.nspix = nspix
    self.n_iter = n_iter
    self.scale1 = nn.Sequential(conv_bn_relu(5, 64), conv_bn_relu(64, 64))
    self.scale2 = nn.Sequential(nn.MaxPool2d(3, 2, padding=1), conv_bn_relu(64, 64), conv_bn_relu(64, 64))
    self.scale3 = nn.Sequential(nn.MaxPool2d(3, 2, padding=1), conv_bn_relu(64, 64), conv_bn_relu(64, 64))
    self.output_conv = nn.Sequential(nn.Conv2d(((64 * 3) + 5), (feature_dim - 5), 3, padding=1), nn.ReLU(True))
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.normal_(m.weight, 0, 0.001)
            if (m.bias is not None):
                nn.init.constant_(m.bias, 0)
