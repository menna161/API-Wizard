import torch
import numpy as np
from math import pi
from scipy.special import logsumexp
from utils import calculate_matmul, calculate_matmul_n_times


def _init_params(self):
    if (self.mu_init is not None):
        assert (self.mu_init.size() == (1, self.n_components, self.n_features)), ('Input mu_init does not have required tensor dimensions (1, %i, %i)' % (self.n_components, self.n_features))
        self.mu = torch.nn.Parameter(self.mu_init, requires_grad=False)
    else:
        self.mu = torch.nn.Parameter(torch.randn(1, self.n_components, self.n_features), requires_grad=False)
    if (self.covariance_type == 'diag'):
        if (self.var_init is not None):
            assert (self.var_init.size() == (1, self.n_components, self.n_features)), ('Input var_init does not have required tensor dimensions (1, %i, %i)' % (self.n_components, self.n_features))
            self.var = torch.nn.Parameter(self.var_init, requires_grad=False)
        else:
            self.var = torch.nn.Parameter(torch.ones(1, self.n_components, self.n_features), requires_grad=False)
    elif (self.covariance_type == 'full'):
        if (self.var_init is not None):
            assert (self.var_init.size() == (1, self.n_components, self.n_features, self.n_features)), ('Input var_init does not have required tensor dimensions (1, %i, %i, %i)' % (self.n_components, self.n_features, self.n_features))
            self.var = torch.nn.Parameter(self.var_init, requires_grad=False)
        else:
            self.var = torch.nn.Parameter(torch.eye(self.n_features).reshape(1, 1, self.n_features, self.n_features).repeat(1, self.n_components, 1, 1), requires_grad=False)
    self.pi = torch.nn.Parameter(torch.Tensor(1, self.n_components, 1), requires_grad=False).fill_((1.0 / self.n_components))
    self.params_fitted = False
