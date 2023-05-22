import torch
from torch import nn
from torch.nn import *
from torch.nn import functional as F
import numpy as np
from rlil.environments import State


def perturb(self):
    torch.randn(self.epsilon_input.size(), out=self.epsilon_input)
    torch.randn(self.epsilon_output.size(), out=self.epsilon_output)
