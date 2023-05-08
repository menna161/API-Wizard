import os
import math
import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, T, channel, channel_mult, attn, num_res_blocks, dropout):
    '\n        The network of DDPM\n        Inputs:\n            T               : [int] Number of time steps in DDPM\n            channel         : [int] Number of channels in the input image\n            channel_mult    : [list] Number of mult-channels\n            attn            : [list] Number of attention-blocks\n            num_res_block   : [int] Number of residual-blocks\n            dropout         : [float] Dropout\n\n        Attributes:\n            TODO\n        '
    super().__init__()
    assert all([(i < len(channel_mult)) for i in attn]), 'attn index out of bound'
    tdim = (channel * 4)
    self.time_embedding = TimeEmbedding(T, channel, tdim)
    self.head = nn.Conv2d(3, channel, kernel_size=3, stride=1, padding=1)
    self.downblocks = nn.ModuleList()
    channels = [channel]
    now_channel = channel
    for (i, mult) in enumerate(channel_mult):
        out_channel = (channel * mult)
        for _ in range(num_res_blocks):
            self.downblocks.append(ResBlock(in_channel=now_channel, out_channel=out_channel, tdim=tdim, dropout=dropout, attn=(i in attn)))
            now_channel = out_channel
            channels.append(now_channel)
        if (i != (len(channel_mult) - 1)):
            self.downblocks.append(DownSample(now_channel))
            channels.append(now_channel)
    self.middleblocks = nn.ModuleList([ResBlock(now_channel, now_channel, tdim, dropout, attn=True), ResBlock(now_channel, now_channel, tdim, dropout, attn=False)])
    self.upblocks = nn.ModuleList()
    for (i, mult) in reversed(list(enumerate(channel_mult))):
        out_channel = (channel * mult)
        for _ in range((num_res_blocks + 1)):
            self.upblocks.append(ResBlock(in_channel=(channels.pop() + now_channel), out_channel=out_channel, tdim=tdim, dropout=dropout, attn=(i in attn)))
            now_channel = out_channel
        if (i != 0):
            self.upblocks.append(UpSample(now_channel))
    assert (len(channels) == 0)
    self.tail = nn.Sequential(nn.GroupNorm(32, now_channel), Swish(), nn.Conv2d(now_channel, 3, 3, stride=1, padding=1))
    self.initialize()
