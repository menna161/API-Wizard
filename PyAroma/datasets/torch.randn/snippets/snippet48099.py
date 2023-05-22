from collections import OrderedDict
import torch
import torch.nn as nn


def get_feat_size(block, spatial_size, ncolors=3):
    "\n    Function to infer spatial dimensionality in intermediate stages of a model after execution of the specified block.\n\n    Parameters:\n        block (torch.nn.Module): Some part of the model, e.g. the encoder to determine dimensionality before flattening.\n        spatial_size (int): Quadratic input's spatial dimensionality.\n        ncolors (int): Number of dataset input channels/colors.\n    "
    x = torch.randn(2, ncolors, spatial_size, spatial_size)
    out = block(x)
    num_feat = out.size(1)
    spatial_dim_x = out.size(2)
    spatial_dim_y = out.size(3)
    return (num_feat, spatial_dim_x, spatial_dim_y)
