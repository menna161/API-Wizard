import unittest
import functools as ft
import itertools as it
from apex import amp
import torch
from torch import nn
import torch.nn.functional as F
from utils import common_init, HALF, FLOAT, ALWAYS_HALF, ALWAYS_FLOAT, MATCH_INPUT


def test_matmul_op_is_half(self):
    other = torch.randn(self.h, self.h)
    lhs = (lambda x: (x @ other))
    rhs = (lambda x: (other @ x))
    run_layer_test(self, [lhs, rhs], ALWAYS_HALF, (self.h, self.h))
