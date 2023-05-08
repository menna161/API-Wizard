import torch
from torch import nn
from qtorch.quant import *
from collections import OrderedDict
import copy


def _get_return_sequential_lower_func(quant, layer_types=[]):

    def _insert_LP_layer(module):
        'Insert quant layer for all layers so long as in layer_types\n        '
        if (type(module) in SEQUENTIAL_LAYERS):
            for (i, sub_module) in enumerate(module.children()):
                module[i] = _insert_LP_layer(module[i])
            return module
        elif (type(module) in DICT_LAYERS):
            for (key, sub_module) in module.items():
                module[key] = _insert_LP_layer(module[key])
            return module
        elif (len(list(module.children())) != 0):
            for attribute_name in module.__dir__():
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, nn.Module):
                    setattr(module, attribute_name, _insert_LP_layer(attribute))
            return module
        else:
            lp_layer_types = []
            for layer_type in layer_types:
                assert (layer_type in LAYERS_TYPES.keys())
                lp_layer_types += LAYERS_TYPES[layer_type]
            if (type(module) in lp_layer_types):
                module = nn.Sequential(module, quant)
            return module
    return _insert_LP_layer
