import torch
import torch.nn as nn


def weight_xavier_init(*models):
    for model in models:
        for module in model.modules():
            if (isinstance(module, nn.Conv2d) or isinstance(module, nn.Linear)):
                nn.init.orthogonal_(module.weight)
                if (module.bias is not None):
                    module.bias.data.zero_()
            elif isinstance(module, nn.BatchNorm2d):
                module.weight.data.fill_(1)
                module.bias.data.zero_()
