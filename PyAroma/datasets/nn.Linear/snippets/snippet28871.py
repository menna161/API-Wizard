import torch, os, numpy as np
import torch.nn as nn
import pretrainedmodels as ptm
import pretrainedmodels.utils as utils
import torchvision.models as models
import googlenet


def initialize_weights(model):
    '\n    Function to initialize network weights.\n    NOTE: NOT USED IN MAIN SCRIPT.\n\n    Args:\n        model: PyTorch Network\n    Returns:\n        Nothing!\n    '
    for (idx, module) in enumerate(model.modules()):
        if isinstance(module, nn.Conv2d):
            nn.init.kaiming_normal_(module.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(module, nn.BatchNorm2d):
            nn.init.constant_(module.weight, 1)
            nn.init.constant_(module.bias, 0)
        elif isinstance(module, nn.Linear):
            module.weight.data.normal_(0, 0.01)
            module.bias.data.zero_()
