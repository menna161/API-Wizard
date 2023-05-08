import os
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.nn.modules.conv import _ConvNd
from torch.nn.modules.batchnorm import _BatchNorm
import torch.nn.init as initer
import torch.nn.functional as F
import socket


def init_weights(model, conv='kaiming', batchnorm='normal', linear='kaiming', lstm='kaiming'):
    "\n    :param model: Pytorch Model which is nn.Module\n    :param conv:  'kaiming' or 'xavier'\n    :param batchnorm: 'normal' or 'constant'\n    :param linear: 'kaiming' or 'xavier'\n    :param lstm: 'kaiming' or 'xavier'\n    "
    for m in model.modules():
        if isinstance(m, _ConvNd):
            if (conv == 'kaiming'):
                initer.kaiming_normal_(m.weight)
            elif (conv == 'xavier'):
                initer.xavier_normal_(m.weight)
            else:
                raise ValueError('init type of conv error.\n')
            if (m.bias is not None):
                initer.constant_(m.bias, 0)
        elif isinstance(m, _BatchNorm):
            if (batchnorm == 'normal'):
                initer.normal_(m.weight, 1.0, 0.02)
            elif (batchnorm == 'constant'):
                initer.constant_(m.weight, 1.0)
            else:
                raise ValueError('init type of batchnorm error.\n')
            initer.constant_(m.bias, 0.0)
        elif isinstance(m, nn.Linear):
            if (linear == 'kaiming'):
                initer.kaiming_normal_(m.weight)
            elif (linear == 'xavier'):
                initer.xavier_normal_(m.weight)
            else:
                raise ValueError('init type of linear error.\n')
            if (m.bias is not None):
                initer.constant_(m.bias, 0)
        elif isinstance(m, nn.LSTM):
            for (name, param) in m.named_parameters():
                if ('weight' in name):
                    if (lstm == 'kaiming'):
                        initer.kaiming_normal_(param)
                    elif (lstm == 'xavier'):
                        initer.xavier_normal_(param)
                    else:
                        raise ValueError('init type of lstm error.\n')
                elif ('bias' in name):
                    initer.constant_(param, 0)
