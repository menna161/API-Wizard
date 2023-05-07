import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import kaiming_init


def __init__(self, in_dim, spatial_range=(- 1), num_heads=9, position_embedding_dim=(- 1), position_magnitude=1, kv_stride=2, q_stride=1, attention_type='1111'):
    super(GeneralizedAttention, self).__init__()
    self.position_embedding_dim = (position_embedding_dim if (position_embedding_dim > 0) else in_dim)
    self.position_magnitude = position_magnitude
    self.num_heads = num_heads
    self.channel_in = in_dim
    self.spatial_range = spatial_range
    self.kv_stride = kv_stride
    self.q_stride = q_stride
    self.attention_type = [bool(int(_)) for _ in attention_type]
    self.qk_embed_dim = (in_dim // num_heads)
    out_c = (self.qk_embed_dim * num_heads)
    if (self.attention_type[0] or self.attention_type[1]):
        self.query_conv = nn.Conv2d(in_channels=in_dim, out_channels=out_c, kernel_size=1, bias=False)
        self.query_conv.kaiming_init = True
    if (self.attention_type[0] or self.attention_type[2]):
        self.key_conv = nn.Conv2d(in_channels=in_dim, out_channels=out_c, kernel_size=1, bias=False)
        self.key_conv.kaiming_init = True
    self.v_dim = (in_dim // num_heads)
    self.value_conv = nn.Conv2d(in_channels=in_dim, out_channels=(self.v_dim * num_heads), kernel_size=1, bias=False)
    self.value_conv.kaiming_init = True
    if (self.attention_type[1] or self.attention_type[3]):
        self.appr_geom_fc_x = nn.Linear((self.position_embedding_dim // 2), out_c, bias=False)
        self.appr_geom_fc_x.kaiming_init = True
        self.appr_geom_fc_y = nn.Linear((self.position_embedding_dim // 2), out_c, bias=False)
        self.appr_geom_fc_y.kaiming_init = True
    if self.attention_type[2]:
        stdv = (1.0 / math.sqrt((self.qk_embed_dim * 2)))
        appr_bias_value = ((((- 2) * stdv) * torch.rand(out_c)) + stdv)
        self.appr_bias = nn.Parameter(appr_bias_value)
    if self.attention_type[3]:
        stdv = (1.0 / math.sqrt((self.qk_embed_dim * 2)))
        geom_bias_value = ((((- 2) * stdv) * torch.rand(out_c)) + stdv)
        self.geom_bias = nn.Parameter(geom_bias_value)
    self.proj_conv = nn.Conv2d(in_channels=(self.v_dim * num_heads), out_channels=in_dim, kernel_size=1, bias=True)
    self.proj_conv.kaiming_init = True
    self.gamma = nn.Parameter(torch.zeros(1))
    if (self.spatial_range >= 0):
        if (in_dim == 256):
            max_len = 84
        elif (in_dim == 512):
            max_len = 42
        max_len_kv = int((((max_len - 1.0) / self.kv_stride) + 1))
        local_constraint_map = np.ones((max_len, max_len, max_len_kv, max_len_kv), dtype=np.int)
        for iy in range(max_len):
            for ix in range(max_len):
                local_constraint_map[(iy, ix, max(((iy - self.spatial_range) // self.kv_stride), 0):min(((((iy + self.spatial_range) + 1) // self.kv_stride) + 1), max_len), max(((ix - self.spatial_range) // self.kv_stride), 0):min(((((ix + self.spatial_range) + 1) // self.kv_stride) + 1), max_len))] = 0
        self.local_constraint_map = nn.Parameter(torch.from_numpy(local_constraint_map).byte(), requires_grad=False)
    if (self.q_stride > 1):
        self.q_downsample = nn.AvgPool2d(kernel_size=1, stride=self.q_stride)
    else:
        self.q_downsample = None
    if (self.kv_stride > 1):
        self.kv_downsample = nn.AvgPool2d(kernel_size=1, stride=self.kv_stride)
    else:
        self.kv_downsample = None
    self.init_weights()
