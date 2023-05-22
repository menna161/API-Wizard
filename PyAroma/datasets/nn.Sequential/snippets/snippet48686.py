import torch
import torch.nn as nn
from .utils import residual, upsample, merge, _decode


def _make_layer(inp_dim, out_dim, modules):
    layers = [residual(inp_dim, out_dim)]
    layers += [residual(out_dim, out_dim) for _ in range(1, modules)]
    return nn.Sequential(*layers)
