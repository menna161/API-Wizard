import os
import random
import torch
import numpy as np
import json
import pickle
import torch.nn as nn
from collections import OrderedDict
from pathlib import Path
import logging


def register_hook(module):

    def hook(module, input, output=None):
        class_name = str(module.__class__).split('.')[(- 1)].split("'")[0]
        module_idx = len(summary)
        m_key = f'{class_name}-{(module_idx + 1)}'
        summary[m_key] = OrderedDict()
        summary[m_key]['input_shape'] = list(input[0].size())
        summary[m_key]['input_shape'][0] = batch_size
        if ((show_input is False) and (output is not None)):
            if isinstance(output, (list, tuple)):
                for out in output:
                    if isinstance(out, torch.Tensor):
                        summary[m_key]['output_shape'] = [([(- 1)] + list(out.size())[1:])][0]
                    else:
                        summary[m_key]['output_shape'] = [([(- 1)] + list(out[0].size())[1:])][0]
            else:
                summary[m_key]['output_shape'] = list(output.size())
                summary[m_key]['output_shape'][0] = batch_size
        params = 0
        if (hasattr(module, 'weight') and hasattr(module.weight, 'size')):
            params += torch.prod(torch.LongTensor(list(module.weight.size())))
            summary[m_key]['trainable'] = module.weight.requires_grad
        if (hasattr(module, 'bias') and hasattr(module.bias, 'size')):
            params += torch.prod(torch.LongTensor(list(module.bias.size())))
        summary[m_key]['nb_params'] = params
    if ((not isinstance(module, nn.Sequential)) and (not isinstance(module, nn.ModuleList)) and (not (module == model))):
        if (show_input is True):
            hooks.append(module.register_forward_pre_hook(hook))
        else:
            hooks.append(module.register_forward_hook(hook))
