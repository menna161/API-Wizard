import numpy as np
import torch
from torch import nn
from torch.distributions import Independent, Normal
from torch.nn import Parameter, functional as F


def _create_fcnn(input_size, hidden_size, output_size, activation_function, dropout=0, final_gain=1.0):
    assert (activation_function in ACTIVATION_FUNCTIONS.keys())
    (network_dims, layers) = ((input_size, hidden_size, hidden_size), [])
    for l in range((len(network_dims) - 1)):
        layer = nn.Linear(network_dims[l], network_dims[(l + 1)])
        nn.init.orthogonal_(layer.weight, gain=nn.init.calculate_gain(activation_function))
        nn.init.constant_(layer.bias, 0)
        layers.append(layer)
        if (dropout > 0):
            layers.append(nn.Dropout(p=dropout))
        layers.append(ACTIVATION_FUNCTIONS[activation_function]())
    final_layer = nn.Linear(network_dims[(- 1)], output_size)
    nn.init.orthogonal_(final_layer.weight, gain=final_gain)
    nn.init.constant_(final_layer.bias, 0)
    layers.append(final_layer)
    return nn.Sequential(*layers)
