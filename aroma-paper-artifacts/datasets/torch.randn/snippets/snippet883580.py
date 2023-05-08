import logging
import torch
import torch.nn as nn
import torch.nn.functional as torch_functional
from collections import OrderedDict
from typing import List, Dict
from dataclasses import field
from sonosco.serialization import serializable
from sonosco.blocks.modules import SubsampleBlock, TDSBlock, Linear, BatchRNN, InferenceBatchSoftmax, supported_rnns
from sonosco.blocks.attention import DotAttention
from sonosco.common.global_settings import CUDA_ENABLED, DEVICE
from sonosco.common.utils import labels_to_dict


def _random_sampling(self, y_labels):
    '\n        Randomly sample tokens given a specified probability, in order to bring\n        training closer to inference.\n\n        pseudo:\n        1. sample U random numbers c from uniform distribution (0,1) [B, T, c]\n        2. create vector of 1 and 0 with c > specified probability [B, T, 1 or 0]\n        3. Sample vector Z of tokens (uniform distribution over tokens excl. eos) [B,T,token]\n        4. Calc: Y_hat = R o Z + (1-R) o Y (Y being teacher forced tokens)\n\n        Args:\n            y_labels: (torch tensor) [B, T, V] - tensor of groundtruth tokens\n        Returns\n            tensor of tokens, partially groundtruth partially sampled\n        '
    sampled_tensor = torch.randn(size=y_labels.size())
    sampled_tensor[(sampled_tensor > self.sampling_prob)] = 1
    sampled_tensor[(sampled_tensor < self.sampling_prob)] = 0
    sampled_tensor = sampled_tensor.type(dtype=torch.long)
    sampled_tokens = torch.randint(high=(len(self.labels) - 2), low=0, size=y_labels.size()).type(dtype=torch.long)
    ones = torch.ones(y_labels.shape).type(dtype=torch.long)
    if CUDA_ENABLED:
        sampled_tensor = sampled_tensor.cuda()
        sampled_tokens = sampled_tokens.cuda()
        ones = ones.cuda()
    y_sampled = ((sampled_tensor * sampled_tokens) + ((ones - sampled_tensor) * y_labels))
    return y_sampled
