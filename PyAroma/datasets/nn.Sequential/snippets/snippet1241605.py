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


def summary(model, *inputs, batch_size=(- 1), show_input=True):
    '\n    打印模型结构信息\n    :param model:\n    :param inputs:\n    :param batch_size:\n    :param show_input:\n    :return:\n    Example:\n        >>> print("model summary info: ")\n        >>> for step,batch in enumerate(train_data):\n        >>>     summary(self.model,*batch,show_input=True)\n        >>>     break\n    '

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
    summary = OrderedDict()
    hooks = []
    model.apply(register_hook)
    model(*inputs)
    for h in hooks:
        h.remove()
    print('-----------------------------------------------------------------------')
    if (show_input is True):
        line_new = f"{'Layer (type)':>25}  {'Input Shape':>25} {'Param #':>15}"
    else:
        line_new = f"{'Layer (type)':>25}  {'Output Shape':>25} {'Param #':>15}"
    print(line_new)
    print('=======================================================================')
    total_params = 0
    total_output = 0
    trainable_params = 0
    for layer in summary:
        if (show_input is True):
            line_new = '{:>25}  {:>25} {:>15}'.format(layer, str(summary[layer]['input_shape']), '{0:,}'.format(summary[layer]['nb_params']))
        else:
            line_new = '{:>25}  {:>25} {:>15}'.format(layer, str(summary[layer]['output_shape']), '{0:,}'.format(summary[layer]['nb_params']))
        total_params += summary[layer]['nb_params']
        if (show_input is True):
            total_output += np.prod(summary[layer]['input_shape'])
        else:
            total_output += np.prod(summary[layer]['output_shape'])
        if ('trainable' in summary[layer]):
            if (summary[layer]['trainable'] == True):
                trainable_params += summary[layer]['nb_params']
        print(line_new)
    print('=======================================================================')
    print(f'Total params: {total_params:0,}')
    print(f'Trainable params: {trainable_params:0,}')
    print(f'Non-trainable params: {(total_params - trainable_params):0,}')
    print('-----------------------------------------------------------------------')
