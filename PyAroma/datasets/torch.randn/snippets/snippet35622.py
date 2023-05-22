import torch
import torch.nn as nn
import torch.nn.functional as F
from gae.layers import GraphConvolution


def reparameterize(self, mu, logvar):
    if self.training:
        std = torch.exp(logvar)
        eps = torch.randn_like(std)
        return eps.mul(std).add_(mu)
    else:
        return mu
