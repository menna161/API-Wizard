import numpy as np
import torch.nn as nn
import torch
from torch.autograd import Variable
from torchvision.utils import save_image
from tqdm import tqdm
import os


def __init__(self, img_shape, hid_dims: list=[512, 256]):
    '\n        The basic model for discriminator\n        Inputs:\n            img_shape : [tuple] the size of input\n            latent_dim : [int] discriminator latent dimension;\n        '
    super(Discriminator, self).__init__()
    self.img_shape = img_shape
    self.hid_dims = hid_dims
    self.num_layers = len(self.hid_dims)
    self.Block = nn.ModuleList()
    for layer_index in range(self.num_layers):
        if (layer_index == 0):
            self.Block.append(nn.Linear(int(np.prod(self.img_shape)), self.hid_dims[layer_index]))
        else:
            self.Block.append(nn.Linear(self.hid_dims[(layer_index - 1)], self.hid_dims[layer_index]))
        self.Block.append(nn.LeakyReLU(0.2, inplace=True))
    self.Block.append(nn.Linear(self.hid_dims[(- 1)], 1))
    self.model = nn.Sequential(*self.Block, nn.Sigmoid())
