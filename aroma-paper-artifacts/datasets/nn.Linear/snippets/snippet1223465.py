import numpy as np
import torch.nn as nn
import torch
from torch.autograd import Variable
from torchvision.utils import save_image
from tqdm import tqdm
import os


def __init__(self, img_shape, z_dim: int=100, hid_dims: list=[100, 200, 400, 800]):
    '\n        The basic model for generator\n        Inputs:\n            img_shape : [tuple] the size of input\n            latent_dim : [int] generator latent dimension;\n            z_dim : [int] the noise dimension\n        '
    super(Generator, self).__init__()
    self.img_shape = img_shape
    self.z_dim = z_dim
    self.hid_dims = hid_dims
    self.num_layers = len(self.hid_dims)

    def block(in_feat, out_feat, normalize=True):
        layers = [nn.Linear(in_feat, out_feat)]
        if normalize:
            layers.append(nn.BatchNorm1d(out_feat, 0.8))
        layers.append(nn.LeakyReLU(0.2, inplace=True))
        return layers
    self.Block = nn.ModuleList()
    for layer_index in range(self.num_layers):
        if (layer_index == 0):
            latent_layers = block(self.z_dim, self.hid_dims[layer_index], normalize=False)
        else:
            latent_layers = block(self.hid_dims[(layer_index - 1)], self.hid_dims[layer_index])
        for i in range(len(latent_layers)):
            self.Block.append(latent_layers[i])
    self.model = nn.Sequential(*self.Block, nn.Linear(self.hid_dims[(- 1)], int(np.prod(self.img_shape))), nn.Tanh())
