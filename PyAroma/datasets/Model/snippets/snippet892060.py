from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import OpenAIGPTConfig, OpenAIGPTModel, OpenAIGPTLMHeadModel, OpenAIGPTDoubleHeadsModel


def create_openai_model(self, config, input_ids, token_type_ids, position_ids, mc_labels, lm_labels, mc_token_ids):
    model = OpenAIGPTModel(config)
    model.eval()
    hidden_states = model(input_ids, position_ids, token_type_ids)
    outputs = {'hidden_states': hidden_states}
    return outputs
