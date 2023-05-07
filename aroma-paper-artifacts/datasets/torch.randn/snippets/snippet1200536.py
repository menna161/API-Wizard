import torch
import numpy as np
from math import pi
from scipy.special import logsumexp
from utils import calculate_matmul, calculate_matmul_n_times


def sample(self, n):
    '\n        Samples from the model.\n        args:\n            n:          int\n        returns:\n            x:          torch.Tensor (n, d)\n            y:          torch.Tensor (n)\n        '
    counts = torch.distributions.multinomial.Multinomial(total_count=n, probs=self.pi.squeeze()).sample()
    x = torch.empty(0, device=counts.device)
    y = torch.cat([torch.full([int(sample)], j, device=counts.device) for (j, sample) in enumerate(counts)])
    for k in np.arange(self.n_components)[(counts > 0)]:
        if (self.covariance_type == 'diag'):
            x_k = (self.mu[(0, k)] + (torch.randn(int(counts[k]), self.n_features, device=x.device) * torch.sqrt(self.var[(0, k)])))
        elif (self.covariance_type == 'full'):
            d_k = torch.distributions.multivariate_normal.MultivariateNormal(self.mu[(0, k)], self.var[(0, k)])
            x_k = torch.stack([d_k.sample() for _ in range(int(counts[k]))])
        x = torch.cat((x, x_k), dim=0)
    return (x, y)
