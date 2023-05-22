import math
import torch
from pixelflow.distributions import Distribution
from pixelflow.utils import sum_except_batch
from torch.distributions import Normal


def sample(self, num_samples):
    return torch.randn(((num_samples,) + self.shape), device=self.base_measure.device, dtype=self.base_measure.dtype)
