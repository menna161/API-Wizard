import numpy as np
import torch
import torch.nn.functional as F


def __init__(self, input_dim, num_layers):
    super().__init__()
    self.num_layers = num_layers
    self.w = torch.nn.ModuleList([torch.nn.Linear(input_dim, 1, bias=False) for _ in range(num_layers)])
    self.b = torch.nn.ParameterList([torch.nn.Parameter(torch.zeros((input_dim,))) for _ in range(num_layers)])
