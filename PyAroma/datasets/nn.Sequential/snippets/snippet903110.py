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


def _make_model_wrapper(self, model):
    try:
        import torch.nn as nn
        if (not hasattr(self, '_model_wrapper')):

            class ModelWrapper(nn.Module):
                '\n                    This is a wrapper for the input model.\n                    '

                def __init__(self, model):
                    '\n                        Initialization by storing the input model.\n\n                        :param model: PyTorch model. The forward function of the model must return the logit output.\n                        :type model: is instance of `torch.nn.Module`\n                        '
                    super(ModelWrapper, self).__init__()
                    self._model = model

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
            self._model_wrapper = ModelWrapper
        return self._model_wrapper(model)
    except ImportError:
        raise ImportError('Could not find PyTorch (`torch`) installation.')
