import torch
from networks import load_config
from torch import nn


def reparam(self, mean, std):
    epsilon = torch.randn_like(std)
    return (mean + torch.mul(epsilon, std))
