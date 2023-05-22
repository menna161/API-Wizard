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


def _forward(self, dec_inp, mems=None):
    (qlen, bsz) = dec_inp.size()
    word_emb = self.word_emb(dec_inp)
    mlen = (mems[0].size(0) if (mems is not None) else 0)
    klen = (mlen + qlen)
    if self.same_length:
        all_ones = word_emb.new_ones(qlen, klen)
        mask_len = (klen - self.mem_len)
        if (mask_len > 0):
            mask_shift_len = (qlen - mask_len)
        else:
            mask_shift_len = qlen
        dec_attn_mask = (torch.triu(all_ones, (1 + mlen)) + torch.tril(all_ones, (- mask_shift_len))).byte()[(:, :, None)]
    else:
        dec_attn_mask = torch.triu(word_emb.new_ones(qlen, klen), diagonal=(1 + mlen)).byte()[(:, :, None)]
    hids = []
    if (self.attn_type == 0):
        pos_seq = torch.arange((klen - 1), (- 1), (- 1.0), device=word_emb.device, dtype=word_emb.dtype)
        if (self.clamp_len > 0):
            pos_seq.clamp_(max=self.clamp_len)
        pos_emb = self.pos_emb(pos_seq)
        core_out = self.drop(word_emb)
        pos_emb = self.drop(pos_emb)
        for (i, layer) in enumerate(self.layers):
            hids.append(core_out)
            mems_i = (None if (mems is None) else mems[i])
            core_out = layer(core_out, pos_emb, dec_attn_mask=dec_attn_mask, mems=mems_i)
    elif (self.attn_type == 1):
        core_out = self.drop(word_emb)
        for (i, layer) in enumerate(self.layers):
            hids.append(core_out)
            if (self.clamp_len > 0):
                r_emb = self.r_emb[i][(- self.clamp_len):]
                r_bias = self.r_bias[i][(- self.clamp_len):]
            else:
                (r_emb, r_bias) = (self.r_emb[i], self.r_bias[i])
            mems_i = (None if (mems is None) else mems[i])
            core_out = layer(core_out, r_emb, self.r_w_bias[i], r_bias, dec_attn_mask=dec_attn_mask, mems=mems_i)
    elif (self.attn_type == 2):
        pos_seq = torch.arange((klen - 1), (- 1), (- 1.0), device=word_emb.device, dtype=word_emb.dtype)
        if (self.clamp_len > 0):
            pos_seq.clamp_(max=self.clamp_len)
        pos_emb = self.pos_emb(pos_seq)
        core_out = self.drop((word_emb + pos_emb[(- qlen):]))
        for (i, layer) in enumerate(self.layers):
            hids.append(core_out)
            mems_i = (None if (mems is None) else mems[i])
            if ((mems_i is not None) and (i == 0)):
                mems_i += pos_emb[:mlen]
            core_out = layer(core_out, dec_attn_mask=dec_attn_mask, mems=mems_i)
    elif (self.attn_type == 3):
        core_out = self.drop(word_emb)
        for (i, layer) in enumerate(self.layers):
            hids.append(core_out)
            mems_i = (None if (mems is None) else mems[i])
            if ((mems_i is not None) and (mlen > 0)):
                cur_emb = self.r_emb[i][:(- qlen)]
                cur_size = cur_emb.size(0)
                if (cur_size < mlen):
                    cur_emb_pad = cur_emb[0:1].expand((mlen - cur_size), (- 1), (- 1))
                    cur_emb = torch.cat([cur_emb_pad, cur_emb], 0)
                else:
                    cur_emb = cur_emb[(- mlen):]
                mems_i += cur_emb.view(mlen, 1, (- 1))
            core_out += self.r_emb[i][(- qlen):].view(qlen, 1, (- 1))
            core_out = layer(core_out, dec_attn_mask=dec_attn_mask, mems=mems_i)
    core_out = self.drop(core_out)
    new_mems = self._update_mems(hids, mems, mlen, qlen)
    return (core_out, new_mems)
