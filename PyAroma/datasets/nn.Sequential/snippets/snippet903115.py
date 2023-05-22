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


@property
def get_layers(self):
    '\n                        Return the hidden layers in the model, if applicable.\n\n                        :return: The hidden layers in the model, input and output layers excluded.\n                        :rtype: `list`\n\n                        .. warning:: `get_layers` tries to infer the internal structure of the model.\n                                     This feature comes with no guarantees on the correctness of the result.\n                                     The intended order of the layers tries to match their order in the model, but this\n                                     is not guaranteed either. In addition, the function can only infer the internal\n                                     layers if the input model is of type `nn.Sequential`, otherwise, it will only\n                                     return the logit layer.\n                        '
    import torch.nn as nn
    result = []
    if isinstance(self._model, nn.Sequential):
        for (name, module_) in self._model._modules.items():
            result.append(((name + '_') + str(module_)))
    elif isinstance(self._model, nn.Module):
        result.append('logit_layer')
    else:
        raise TypeError('The input model must inherit from `nn.Module`.')
    return result
