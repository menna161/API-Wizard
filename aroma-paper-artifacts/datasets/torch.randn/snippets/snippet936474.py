import torch
import unittest
from qtorch.quant import *
from qtorch import FixedPoint, BlockFloatingPoint, FloatingPoint


def test_fixed_random(self):
    S = (lambda bits: (2 ** bits))
    Q = (lambda x, bits: (torch.round((x * S(bits))) / S(bits)))
    wl = 8
    quant = (lambda x: fixed_point_quantize(x, wl=wl, fl=wl, clamp=False, rounding='nearest'))
    N = int(100000000.0)
    for device in ['cpu', 'cuda']:
        x = torch.randn(N, device='cpu')
        oracle = Q(x, wl)
        target = quant(x)
        matched = torch.eq(oracle, target).all().item()
        self.assertTrue(matched)
