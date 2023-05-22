import torch
import torch.nn.functional as F
import math


def sample_params(self, shape, device='cpu'):
    v = (math.log(0.1) + (0.1 * torch.randn(shape))).to(device).exp()
    shape = (torch.Size(shape) + torch.Size([self.dim]))
    mu = (4.0 * torch.randn(shape).to(device))
    W = (0.25 * torch.randn(shape).to(device))
    return torch.cat([mu, v.unsqueeze((- 1)), W], (- 1))
