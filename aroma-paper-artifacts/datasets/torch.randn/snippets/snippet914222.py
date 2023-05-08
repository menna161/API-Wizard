from __future__ import division
import math
import torch
from torch import nn
from torch.nn import functional as F


def _scale_noise(self, size):
    x = torch.randn(size)
    return x.sign().mul_(x.abs().sqrt_())
