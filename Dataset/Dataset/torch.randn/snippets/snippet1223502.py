import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
import copy
import os


def reparameterize(self, mu, log_var):
    '\n        Gaussian re_parameterization\n        Inputs:\n            mu : [tensor] mean of posterior distribution;\n            log_var : [tensor] log variance of posterior distribution;\n        Outputs:\n            z_sample : [tensor] sample from the distribution\n        '
    std = torch.exp((0.5 * log_var))
    eps = torch.randn_like(std)
    return eps.mul(std).add_(mu)
