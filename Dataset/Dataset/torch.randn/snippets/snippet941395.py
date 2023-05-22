import math
import torch
import torch.nn as nn
from .prior.priors import *
from .variational_dist import Q_FCDenseNet103_FVI


def _generate_x_c(self, x_t):
    randn = (math.sqrt(self.x_inducing_var) * torch.randn_like(x_t[:self.n_inducing]))
    x_c = (x_t[:self.n_inducing] + randn).clamp_(0.0, 1.0)
    return x_c
