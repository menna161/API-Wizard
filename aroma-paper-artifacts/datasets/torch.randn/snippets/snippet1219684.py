import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.normal import Normal
from lib.utils.vis_logger import logger


def forward(self, x, n_samples):
    '\n        :param x: input from encoder (B, D)\n        :return: (B, N, D), where N is the number of samples\n        '
    self.mean = self.mean_layer(x)
    self.log_var = self.log_var_layer(x)
    log_dev = (0.5 * self.log_var)
    dev = torch.exp(log_dev)
    N = n_samples
    (B, D) = self.mean.size()
    mean = self.mean[(:, None, :)]
    dev = dev[(:, None, :)]
    epsilon = torch.randn(B, N, D).to(self.mean.device)
    return (mean + (dev * epsilon))
