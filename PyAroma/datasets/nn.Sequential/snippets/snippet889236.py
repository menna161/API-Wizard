import numpy as np
import torch


def __init__(self, input_dim, embed_dims, dropout, output_layer=True):
    super().__init__()
    layers = list()
    for embed_dim in embed_dims:
        layers.append(torch.nn.Linear(input_dim, embed_dim))
        layers.append(torch.nn.BatchNorm1d(embed_dim))
        layers.append(torch.nn.ReLU())
        layers.append(torch.nn.Dropout(p=dropout))
        input_dim = embed_dim
    if output_layer:
        layers.append(torch.nn.Linear(input_dim, 1))
    self.mlp = torch.nn.Sequential(*layers)
