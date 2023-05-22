import torch.nn as nn
import torch
import torch.nn.functional as F
import math
import utils.logger as logger


def __init__(self, n_channels, n_classes, vec_len, normalize=False):
    super().__init__()
    if normalize:
        target_scale = 0.06
        self.embedding_scale = target_scale
        self.normalize_scale = target_scale
    else:
        self.embedding_scale = 0.001
        self.normalize_scale = None
    self.embedding0 = nn.Parameter((torch.randn(n_channels, n_classes, vec_len, requires_grad=True) * self.embedding_scale))
    self.offset = (torch.arange(n_channels).cuda() * n_classes)
    self.n_classes = n_classes
    self.after_update()
