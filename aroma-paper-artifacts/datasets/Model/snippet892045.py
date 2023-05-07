from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import GPT2Config, GPT2Model, GPT2LMHeadModel, GPT2DoubleHeadsModel


def create_gpt2_model(self, config, input_ids, token_type_ids, position_ids, mc_labels, lm_labels, mc_token_ids):
    model = GPT2Model(config)
    model.eval()
    (hidden_states, presents) = model(input_ids, position_ids, token_type_ids)
    outputs = {'hidden_states': hidden_states, 'presents': presents}
    return outputs
