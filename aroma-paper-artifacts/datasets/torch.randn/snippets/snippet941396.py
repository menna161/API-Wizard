import math
import torch
import torch.nn as nn
from .prior.priors import *
from .variational_dist import Q_FCDenseNet103_FVI


def _sample_functions(self, q_mean, q_cov):
    (N, P, _) = q_cov.size()
    q_cov_diag = torch.diagonal(q_cov, dim1=0, dim2=2).t()
    Z = torch.randn(self.S, N, P).to(q_mean.device)
    f = torch.einsum('ij,lij->lij', q_cov_diag.sqrt(), Z)
    f_values = (q_mean.unsqueeze(0).expand(self.S, (- 1), (- 1)) + f)
    return f_values
