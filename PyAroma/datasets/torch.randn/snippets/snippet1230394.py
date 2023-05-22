import torch
import torch.nn.functional as F
import math


def sample(self, params):
    mu = params[(..., :self.dim)]
    sigma = params[(..., self.dim:)]
    eps = torch.randn(mu.shape).to(mu.device)
    return (mu + (eps * sigma))
