import unittest
import functools as ft
import itertools as it
from apex import amp
import torch
from torch import nn
import torch.nn.functional as F
from utils import common_init, HALF, FLOAT, ALWAYS_HALF, ALWAYS_FLOAT, MATCH_INPUT


def test_linear_is_half(self):
    m = nn.Linear(self.h, self.h)
    f = ft.partial(F.linear, weight=m.weight, bias=m.bias)
    run_layer_test(self, [m, f], ALWAYS_HALF, (self.b, self.h))
