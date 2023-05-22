import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
import copy
import os


def sample(self, batch_size):
    '\n        Sample from generator\n        Inputs:\n            batch_size : [int] number of img which you want;\n        Outputs:\n            recon_x : [tensor] reconstruction of x\n        '
    z = torch.randn(batch_size, self.z_dim).to(self.device)
    recon_x = self.vae_decoder(z)
    return recon_x
