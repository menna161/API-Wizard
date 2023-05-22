import torch
import torch.nn.functional as F
import math


def sample(self, params):
    mu = params[(..., :self.dim)]
    v = params[(..., self.dim)].unsqueeze((- 1))
    W = params[(..., (self.dim + 1):)]
    eps_v = torch.randn(mu.shape).to(mu.device)
    eps_W = torch.randn(v.shape).to(v.device)
    return ((mu + (eps_v * v.sqrt())) + (eps_W * W))
