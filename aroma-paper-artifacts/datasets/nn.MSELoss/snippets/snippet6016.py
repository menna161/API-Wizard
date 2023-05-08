import torch.nn as nn
import torch
from torch.nn import functional as F
import math


def __init__(self, error_metric=nn.MSELoss(), threshold=None, clip=None):
    super().__init__()
    self.error_metric = error_metric
    self.threshold = (threshold if (threshold is not None) else (- 100))
    self.clip = clip
