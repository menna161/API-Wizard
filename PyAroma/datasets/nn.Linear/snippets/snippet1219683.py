import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.normal import Normal
from lib.utils.vis_logger import logger


def __init__(self, dim_in, dim_latent):
    nn.Module.__init__(self)
    self.mean_layer = nn.Linear(dim_in, dim_latent)
    self.log_var_layer = nn.Linear(dim_in, dim_latent)
