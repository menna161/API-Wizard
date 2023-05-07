from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import GPT2Config, GPT2Model, GPT2LMHeadModel, GPT2DoubleHeadsModel


def create_gpt2_lm_head(self, config, input_ids, token_type_ids, position_ids, mc_labels, lm_labels, mc_token_ids):
    model = GPT2LMHeadModel(config)
    model.eval()
    loss = model(input_ids, position_ids, token_type_ids, lm_labels)
    (lm_logits, presents) = model(input_ids, position_ids, token_type_ids)
    outputs = {'loss': loss, 'lm_logits': lm_logits, 'presents': presents}
    return outputs
