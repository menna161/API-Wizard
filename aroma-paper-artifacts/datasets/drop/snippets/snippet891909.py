import os
import copy
import json
import math
import logging
import tarfile
import tempfile
import shutil
import collections
import sys
from io import open
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
from torch.nn.parameter import Parameter
from .modeling import BertLayerNorm as LayerNorm
from .modeling_transfo_xl_utilities import ProjectedAdaptiveLogSoftmax, sample_logits
from .file_utils import cached_path
import numpy as np
import tensorflow as tf


def forward(self, w, r_emb, r_w_bias, r_bias, attn_mask=None, mems=None):
    (qlen, bsz) = (w.size(0), w.size(1))
    if (mems is not None):
        cat = torch.cat([mems, w], 0)
        if self.pre_lnorm:
            w_heads = self.qkv_net(self.layer_norm(cat))
        else:
            w_heads = self.qkv_net(cat)
        (w_head_q, w_head_k, w_head_v) = torch.chunk(w_heads, 3, dim=(- 1))
        w_head_q = w_head_q[(- qlen):]
    else:
        if self.pre_lnorm:
            w_heads = self.qkv_net(self.layer_norm(w))
        else:
            w_heads = self.qkv_net(w)
        (w_head_q, w_head_k, w_head_v) = torch.chunk(w_heads, 3, dim=(- 1))
    klen = w_head_k.size(0)
    w_head_q = w_head_q.view(qlen, bsz, self.n_head, self.d_head)
    w_head_k = w_head_k.view(klen, bsz, self.n_head, self.d_head)
    w_head_v = w_head_v.view(klen, bsz, self.n_head, self.d_head)
    if (klen > r_emb.size(0)):
        r_emb_pad = r_emb[0:1].expand((klen - r_emb.size(0)), (- 1), (- 1))
        r_emb = torch.cat([r_emb_pad, r_emb], 0)
        r_bias_pad = r_bias[0:1].expand((klen - r_bias.size(0)), (- 1))
        r_bias = torch.cat([r_bias_pad, r_bias], 0)
    else:
        r_emb = r_emb[(- klen):]
        r_bias = r_bias[(- klen):]
    rw_head_q = (w_head_q + r_w_bias[None])
    AC = torch.einsum('ibnd,jbnd->ijbn', (rw_head_q, w_head_k))
    B_ = torch.einsum('ibnd,jnd->ijbn', (w_head_q, r_emb))
    D_ = r_bias[(None, :, None)]
    BD = self._rel_shift((B_ + D_))
    attn_score = (AC + BD)
    attn_score.mul_(self.scale)
    if ((attn_mask is not None) and attn_mask.any().item()):
        if (attn_mask.dim() == 2):
            attn_score.masked_fill_(attn_mask[(None, :, :, None)], (- float('inf')))
        elif (attn_mask.dim() == 3):
            attn_score.masked_fill_(attn_mask[(:, :, :, None)], (- float('inf')))
    attn_prob = F.softmax(attn_score, dim=1)
    attn_prob = self.dropatt(attn_prob)
    attn_vec = torch.einsum('ijbn,jbnd->ibnd', (attn_prob, w_head_v))
    attn_vec = attn_vec.contiguous().view(attn_vec.size(0), attn_vec.size(1), (self.n_head * self.d_head))
    attn_out = self.o_net(attn_vec)
    attn_out = self.drop(attn_out)
    if self.pre_lnorm:
        output = (w + attn_out)
    else:
        output = self.layer_norm((w + attn_out))
    return output
