import torch
import torch.nn as nn
from .utils import residual, upsample, merge, _decode


def _make_layer_revr(inp_dim, out_dim, modules):
    layers = [residual(inp_dim, inp_dim) for _ in range((modules - 1))]
    layers += [residual(inp_dim, out_dim)]
    return nn.Sequential(*layers)
