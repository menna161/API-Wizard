import unittest
import itertools as it
from apex import amp
import torch
from torch import nn
import torch.nn.functional as F
from utils import common_init, HALF, FLOAT, DTYPES


def test_inplace_exp_is_error_for_half(self):
    xs = torch.randn(self.b)
    xs.exp_()
    self.assertEqual(xs.type(), FLOAT)
    xs = torch.randn(self.b, dtype=torch.half)
    with self.assertRaises(NotImplementedError):
        xs.exp_()
