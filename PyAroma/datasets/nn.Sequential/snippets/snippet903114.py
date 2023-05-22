from __future__ import absolute_import, division, print_function, unicode_literals
import abc
import sys
import numpy as np
import logging as logger
import torch
import torch
import torch
import torch
import torch
import os
import torch
import time
import copy
import os
import torch
import torch.nn as nn
import torch.nn as nn
import torch.nn as nn


def forward(self, x):
    '\n                        This is where we get outputs from the input model.\n\n                        :param x: Input data.\n                        :type x: `torch.Tensor`\n                        :return: a list of output layers, where the last 2 layers are logit and final outputs.\n                        :rtype: `list`\n                        '
    import torch.nn as nn
    result = []
    if isinstance(self._model, nn.Sequential):
        for (_, module_) in self._model._modules.items():
            x = module_(x)
            result.append(x)
    elif isinstance(self._model, nn.Module):
        x = self._model(x)
        result.append(x)
    else:
        raise TypeError('The input model must inherit from `nn.Module`.')
    output_layer = nn.functional.softmax(x, dim=1)
    result.append(output_layer)
    return result
