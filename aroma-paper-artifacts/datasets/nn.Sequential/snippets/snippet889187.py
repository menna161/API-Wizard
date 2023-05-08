import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, input_dim, embed_dims, dropout, output_layer=True):
    super().__init__()
    layers = list()
    for embed_dim in embed_dims:
        layers.append(Meta_Linear(input_dim, embed_dim))
        layers.append(torch.nn.ReLU())
        input_dim = embed_dim
    if output_layer:
        layers.append(Meta_Linear(input_dim, 1))
    self.mlp = torch.nn.Sequential(*layers)
