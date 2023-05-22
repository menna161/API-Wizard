import unittest
import functools as ft
import itertools as it
from apex import amp
import torch
from torch import nn
import torch.nn.functional as F
from utils import common_init, HALF, FLOAT, ALWAYS_HALF, ALWAYS_FLOAT, MATCH_INPUT


def test_disabled_linear(self):
    m = nn.Linear(self.h, self.h)
    f = ft.partial(F.linear, weight=m.weight, bias=m.bias)
    input_shape = (self.b, self.h)
    for fn in [m, f]:
        x = torch.randn(input_shape, dtype=torch.float).requires_grad_()
        y = fn(x)
        self.assertEqual(y.type(), FLOAT)
        y.sum().backward()
        self.assertEqual(x.grad.type(), FLOAT)
        x = torch.randn(input_shape, dtype=torch.half).requires_grad_()
        self.assertRaises(RuntimeError, fn, x)
