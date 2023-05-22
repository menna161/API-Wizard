import logging
import math
import pdb
import numpy as np
import torch
import torch.nn as nn
from torch.nn.parameter import Parameter
import torch.nn.functional as F
from torch.nn.utils import weight_norm as wn
from utils import *


def __init__(self, dim_in, dim_out, weight_norm=True):
    super(nin, self).__init__()
    if weight_norm:
        self.lin_a = wn(nn.Linear(dim_in, dim_out))
    else:
        self.lin_a = nn.Linear(dim_in, dim_out)
    self.dim_out = dim_out
