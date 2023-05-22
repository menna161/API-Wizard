import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from utils.tensor import chunk_two, sum_except_batch as sumeb


def sample(self, num_samples=None, context=None, device='cpu'):
    if (self.use_context and (context is not None)):
        (mu, sigma) = chunk_two(self.context_enc(context))
        sigma = (F.softplus(sigma) + 1e-05)
        eps = torch.randn_like(mu)
        x = (mu + (sigma * eps))
        lp = sumeb((self.unit_log_prob(eps) - sigma.log()))
        return (x, lp)
    else:
        eps = torch.randn(self.infer_shape(num_samples), device=device)
        lp = sumeb(self.unit_log_prob(eps))
        return (eps, lp)
