from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import OpenAIGPTConfig, OpenAIGPTModel, OpenAIGPTLMHeadModel, OpenAIGPTDoubleHeadsModel


@classmethod
def ids_tensor(cls, shape, vocab_size, rng=None, name=None):
    'Creates a random int32 tensor of the shape within the vocab size.'
    if (rng is None):
        rng = random.Random()
    total_dims = 1
    for dim in shape:
        total_dims *= dim
    values = []
    for _ in range(total_dims):
        values.append(rng.randint(0, (vocab_size - 1)))
    return torch.tensor(data=values, dtype=torch.long).view(shape).contiguous()
