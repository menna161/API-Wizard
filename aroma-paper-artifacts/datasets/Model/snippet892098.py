from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import TransfoXLConfig, TransfoXLModel, TransfoXLLMHeadModel


def create_transfo_xl_model(self, config, input_ids_1, input_ids_2, lm_labels):
    model = TransfoXLModel(config)
    model.eval()
    (hidden_states_1, mems_1) = model(input_ids_1)
    (hidden_states_2, mems_2) = model(input_ids_2, mems_1)
    outputs = {'hidden_states_1': hidden_states_1, 'mems_1': mems_1, 'hidden_states_2': hidden_states_2, 'mems_2': mems_2}
    return outputs
