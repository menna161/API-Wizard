import os
import math
import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, in_channel, out_channel, tdim, dropout, attn=False):
    super().__init__()
    self.block1 = nn.Sequential(nn.GroupNorm(32, in_channel), Swish(), nn.Conv2d(in_channel, out_channel, 3, stride=1, padding=1))
    self.temb_proj = nn.Sequential(Swish(), nn.Linear(tdim, out_channel))
    self.block2 = nn.Sequential(nn.GroupNorm(32, out_channel), Swish(), nn.Dropout(dropout), nn.Conv2d(out_channel, out_channel, 3, stride=1, padding=1))
    if (in_channel != out_channel):
        self.shortcut = nn.Conv2d(in_channel, out_channel, 1, stride=1, padding=0)
    else:
        self.shortcut = nn.Identity()
    if attn:
        self.attn = AttnBlock(out_channel)
    else:
        self.attn = nn.Identity()
    self.initialize()
