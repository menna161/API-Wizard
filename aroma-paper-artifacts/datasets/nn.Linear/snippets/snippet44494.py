import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from models_lpf import *


def _initialize_weights(self):
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            if ((m.in_channels != m.out_channels) or (m.out_channels != m.groups) or (m.bias is not None)):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if (m.bias is not None):
                    nn.init.constant_(m.bias, 0)
            else:
                print('Not initializing')
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, 0, 0.01)
            nn.init.constant_(m.bias, 0)
