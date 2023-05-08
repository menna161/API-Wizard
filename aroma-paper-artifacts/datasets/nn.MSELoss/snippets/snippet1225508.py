import unittest
import functools as ft
import itertools as it
from apex import amp
import torch
from torch import nn
import torch.nn.functional as F
from utils import common_init, HALF, FLOAT, ALWAYS_HALF, ALWAYS_FLOAT, MATCH_INPUT


def test_mse_loss_is_float(self):
    shape = (self.b, self.h)
    target = torch.randn(shape)
    mod = nn.MSELoss()
    m = (lambda x: mod(x, target))
    f = ft.partial(F.mse_loss, target=target)
    run_layer_test(self, [m], ALWAYS_FLOAT, shape)
