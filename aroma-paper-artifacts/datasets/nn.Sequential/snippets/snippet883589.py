import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict
from dataclasses import field
from collections import OrderedDict
from sonosco.serialization import serializable
from sonosco.blocks.modules import SubsampleBlock, TDSBlock, Linear
from sonosco.blocks.attention import DotProductAttention


def __post_init__(self):
    assert ((self.input_dim % self.in_channel) == 0)
    assert (len(self.channels) > 0)
    assert (len(self.channels) == len(self.kernel_sizes))
    super().__init__()
    self.input_freq = (self.input_dim // self.in_channel)
    self.bridge = None
    layers = OrderedDict()
    in_ch = self.in_channel
    in_freq = self.input_freq
    subsample_factor = 1
    for (layer, (channel, kernel_size)) in enumerate(zip(self.channels, self.kernel_sizes)):
        if (in_ch != channel):
            layers[('subsample%d' % layer)] = SubsampleBlock(in_channel=in_ch, out_channel=channel, in_freq=in_freq, dropout=self.dropout)
            subsample_factor *= 2
        layers[('tds%d_block%d' % (channel, layer))] = TDSBlock(channel=channel, kernel_size=kernel_size, in_freq=in_freq, dropout=self.dropout)
        in_ch = channel
    self._output_dim = int((in_ch * in_freq))
    self.hidden_size = self._output_dim
    if (self.bottleneck_dim > 0):
        self.bridge = Linear(self._output_dim, self.bottleneck_dim)
        self._output_dim = self.bottleneck_dim
    self.layers = nn.Sequential(layers)
    self.subsample_factor = subsample_factor
