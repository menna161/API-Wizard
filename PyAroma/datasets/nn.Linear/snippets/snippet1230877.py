import torch
from torch import Tensor
from torch import nn
from torch import functional as F
from typing import Union, Tuple, List, Iterable, Dict
import os
import json
from ..util import fullname, import_from_string


def __init__(self, in_features, out_features, bias=True, activation_function=nn.Tanh()):
    super(Dense, self).__init__()
    self.in_features = in_features
    self.out_features = out_features
    self.bias = bias
    self.activation_function = activation_function
    self.linear = nn.Linear(in_features, out_features, bias=bias)
