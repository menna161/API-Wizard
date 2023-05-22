import unittest
import functools as ft
import itertools as it
from apex import amp
import torch
from torch import nn
import torch.nn.functional as F
from utils import common_init, HALF, FLOAT, ALWAYS_HALF, ALWAYS_FLOAT, MATCH_INPUT


def run_layer_test(test_case, fns, expected, input_shape, test_backward=True):
    for (fn, typ) in it.product(fns, expected.keys()):
        x = torch.randn(input_shape, dtype=typ).requires_grad_()
        y = fn(x)
        test_case.assertEqual(y.type(), expected[typ])
        if test_backward:
            y.float().sum().backward()
            test_case.assertEqual(x.grad.type(), MATCH_INPUT[typ])
