import numpy as np
import torch.nn as nn
import torch
from torch.autograd import Variable
from torchvision.utils import save_image
from tqdm import tqdm
import os


def block(in_feat, out_feat, normalize=True):
    layers = [nn.Linear(in_feat, out_feat)]
    if normalize:
        layers.append(nn.BatchNorm1d(out_feat, 0.8))
    layers.append(nn.LeakyReLU(0.2, inplace=True))
    return layers
