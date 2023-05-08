import os
import math
import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, T, d_model, dim):
    '\n        Get time embedding\n        '
    super().__init__()
    assert ((d_model % 2) == 0)
    emb = ((torch.arange(0, d_model, step=2) / d_model) * math.log(10000))
    emb = torch.exp((- emb))
    pos = torch.arange(T).float()
    emb = (pos[(:, None)] * emb[(None, :)])
    assert (list(emb.shape) == [T, (d_model // 2)])
    emb = torch.stack([torch.sin(emb), torch.cos(emb)], dim=(- 1))
    assert (list(emb.shape) == [T, (d_model // 2), 2])
    emb = emb.view(T, d_model)
    self.timembedding = nn.Sequential(nn.Embedding.from_pretrained(emb), nn.Linear(d_model, dim), Swish(), nn.Linear(dim, dim))
    self.initialize()
