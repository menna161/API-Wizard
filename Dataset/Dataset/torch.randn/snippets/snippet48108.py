from collections import OrderedDict
import torch
import torch.nn as nn


def generate(self):
    z = torch.randn(self.batch_size, self.latent_dim).to(self.device)
    x = self.decode(z)
    x = torch.sigmoid(x)
    x = x.view((- 1), self.num_colors, self.patch_size, self.patch_size)
    return x
