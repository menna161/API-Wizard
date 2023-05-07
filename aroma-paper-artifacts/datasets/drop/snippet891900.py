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


def forward(self, h, attn_mask=None, mems=None):
    if (mems is not None):
        c = torch.cat([mems, h], 0)
    else:
        c = h
    if self.pre_lnorm:
        c = self.layer_norm(c)
    head_q = self.q_net(h)
    (head_k, head_v) = torch.chunk(self.kv_net(c), 2, (- 1))
    head_q = head_q.view(h.size(0), h.size(1), self.n_head, self.d_head)
    head_k = head_k.view(c.size(0), c.size(1), self.n_head, self.d_head)
    head_v = head_v.view(c.size(0), c.size(1), self.n_head, self.d_head)
    attn_score = torch.einsum('ibnd,jbnd->ijbn', (head_q, head_k))
    attn_score.mul_(self.scale)
    if ((attn_mask is not None) and attn_mask.any().item()):
        if (attn_mask.dim() == 2):
            attn_score.masked_fill_(attn_mask[(None, :, :, None)], (- float('inf')))
        elif (attn_mask.dim() == 3):
            attn_score.masked_fill_(attn_mask[(:, :, :, None)], (- float('inf')))
    attn_prob = F.softmax(attn_score, dim=1)
    attn_prob = self.dropatt(attn_prob)
    attn_vec = torch.einsum('ijbn,jbnd->ibnd', (attn_prob, head_v))
    attn_vec = attn_vec.contiguous().view(attn_vec.size(0), attn_vec.size(1), (self.n_head * self.d_head))
    attn_out = self.o_net(attn_vec)
    attn_out = self.drop(attn_out)
    if self.pre_lnorm:
        output = (h + attn_out)
    else:
        output = self.layer_norm((h + attn_out))
    return output
