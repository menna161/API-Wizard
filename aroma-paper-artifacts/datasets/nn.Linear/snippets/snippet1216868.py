import torch
from torch import nn
import torch.nn.functional as F
from mogrifier import Mogrifier
import math
from collections import namedtuple
from functools import partial
from inspect import isfunction


def __init__(self, dim, mult=4, dropout=0.0, activation=None, glu=False):
    super().__init__()
    activation = default(activation, GELU)
    self.glu = glu
    self.w1 = nn.Linear(dim, ((dim * mult) * (2 if glu else 1)))
    self.act = activation()
    self.dropout = nn.Dropout(dropout)
    self.w2 = nn.Linear((dim * mult), dim)
