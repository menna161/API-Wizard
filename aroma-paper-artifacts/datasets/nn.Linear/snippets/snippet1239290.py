import os, torch, numpy
from torch.utils.data import TensorDataset


def z_sample_for_model(model, size=100, seed=1):
    if hasattr(model, 'input_shape'):
        sample = standard_z_sample(size, model.input_shape[1], seed=seed).view(((size,) + model.input_shape[1:]))
        return sample
    first_layer = [c for c in model.modules() if isinstance(c, (torch.nn.Conv2d, torch.nn.ConvTranspose2d, torch.nn.Linear))][0]
    if isinstance(first_layer, (torch.nn.Conv2d, torch.nn.ConvTranspose2d)):
        sample = standard_z_sample(size, first_layer.in_channels, seed=seed)[(:, :, None, None)]
    else:
        sample = standard_z_sample(size, first_layer.in_features, seed=seed)
    return sample
