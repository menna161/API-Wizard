import torch
from torch import nn
from torch.nn import *
from torch.nn import functional as F
import numpy as np
from rlil.environments import State


def perturb(self):
    torch.randn(self.epsilon_weight.size(), out=self.epsilon_weight)
    if (self.bias is not None):
        torch.randn(self.epsilon_bias.size(), out=self.epsilon_bias)
