from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import TransfoXLConfig, TransfoXLModel, TransfoXLLMHeadModel


def create_transfo_xl_lm_head(self, config, input_ids_1, input_ids_2, lm_labels):
    model = TransfoXLLMHeadModel(config)
    model.eval()
    (loss_1, mems_1a) = model(input_ids_1, target=lm_labels)
    (lm_logits_1, mems_1b) = model(input_ids_1)
    (loss_2, mems_2a) = model(input_ids_2, target=lm_labels, mems=mems_1a)
    (lm_logits_2, mems_2b) = model(input_ids_2, mems=mems_1b)
    outputs = {'loss_1': loss_1, 'mems_1a': mems_1a, 'lm_logits_1': lm_logits_1, 'mems_1b': mems_1b, 'loss_2': loss_2, 'mems_2a': mems_2a, 'lm_logits_2': lm_logits_2, 'mems_2b': mems_2b}
    return outputs
