import torch
import torch.nn as nn
import numpy as np
from hrl4in.utils.networks import AddBias


def __init__(self, num_inputs, num_outputs_list):
    super().__init__()
    self.linear_layers = nn.ModuleList([nn.Linear(num_inputs, num_outputs) for num_outputs in num_outputs_list])
    for linear_layer in self.linear_layers:
        nn.init.orthogonal_(linear_layer.weight, gain=0.01)
        nn.init.constant_(linear_layer.bias, 0.0)
