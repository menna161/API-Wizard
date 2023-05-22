import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
from lib.utils.vis_logger import logger
from math import pi, sqrt, log
from math import pi, sqrt, log


def __init__(self, dim_in, dim_out, n_layers):
    nn.Module.__init__(self)
    self.dim_in = dim_in
    self.dim_out = dim_out
    self.layers = nn.ModuleList([])
    for i in range(n_layers):
        self.layers.append(nn.Linear(dim_in, dim_out))
        dim_in = dim_out
