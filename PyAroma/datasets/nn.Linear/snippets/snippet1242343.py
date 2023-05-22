import numpy as np
import torch
import torch.nn.functional as F


def __init__(self, input_dim, cross_layer_sizes, split_half=True):
    super().__init__()
    self.num_layers = len(cross_layer_sizes)
    self.split_half = split_half
    self.conv_layers = torch.nn.ModuleList()
    (prev_dim, fc_input_dim) = (input_dim, 0)
    for i in range(self.num_layers):
        cross_layer_size = cross_layer_sizes[i]
        self.conv_layers.append(torch.nn.Conv1d((input_dim * prev_dim), cross_layer_size, 1, stride=1, dilation=1, bias=True))
        if (self.split_half and (i != (self.num_layers - 1))):
            cross_layer_size //= 2
        prev_dim = cross_layer_size
        fc_input_dim += prev_dim
    self.fc = torch.nn.Linear(fc_input_dim, 1)
