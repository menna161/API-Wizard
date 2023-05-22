import torch
import torch.nn as nn
import torch.utils.data
from torch.nn import functional as F


def convblock(self, in_ch, out_ch, krn_sz=3):
    block = nn.Sequential(nn.Conv2d(in_ch, out_ch, kernel_size=krn_sz, stride=1, padding=int((krn_sz / 2))), nn.LeakyReLU(0.2, inplace=True))
    return block
