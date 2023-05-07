from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import GPT2Config, GPT2Model, GPT2LMHeadModel, GPT2DoubleHeadsModel


def create_gpt2_double_heads(self, config, input_ids, token_type_ids, position_ids, mc_labels, lm_labels, mc_token_ids):
    model = GPT2DoubleHeadsModel(config)
    model.eval()
    loss = model(input_ids, mc_token_ids, lm_labels=lm_labels, mc_labels=mc_labels, token_type_ids=token_type_ids, position_ids=position_ids)
    (lm_logits, mc_logits, presents) = model(input_ids, mc_token_ids, position_ids=position_ids, token_type_ids=token_type_ids)
    outputs = {'loss': loss, 'lm_logits': lm_logits, 'mc_logits': mc_logits, 'presents': presents}
    return outputs
