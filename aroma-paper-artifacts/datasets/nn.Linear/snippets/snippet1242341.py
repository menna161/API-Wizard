import numpy as np
import torch
import torch.nn.functional as F


def __init__(self, embed_dim, attn_size, dropouts):
    super().__init__()
    self.attention = torch.nn.Linear(embed_dim, attn_size)
    self.projection = torch.nn.Linear(attn_size, 1)
    self.fc = torch.nn.Linear(embed_dim, 1)
    self.dropouts = dropouts
