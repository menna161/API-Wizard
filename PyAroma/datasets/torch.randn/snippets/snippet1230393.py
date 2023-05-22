import torch
import torch.nn.functional as F
import math


def sample_params(self, shape, device='cpu'):
    shape = (torch.Size(shape) + torch.Size([self.dim]))
    mu = (3.0 * torch.randn(shape).to(device))
    sigma = (math.log(0.25) + (0.1 * torch.randn(shape))).exp().to(device)
    return torch.cat([mu, sigma], (- 1))
