import torch
import torch.nn as nn


def __init__(self, in_features, out_features, bias=True):
    super(ComplexLinear, self).__init__()
    self.real_linear = nn.Linear(in_features=in_features, out_features=out_features, bias=bias)
    self.imag_linear = nn.Linear(in_features=in_features, out_features=out_features, bias=bias)
