from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import OpenAIGPTConfig, OpenAIGPTModel, OpenAIGPTLMHeadModel, OpenAIGPTDoubleHeadsModel


def create_openai_lm_head(self, config, input_ids, token_type_ids, position_ids, mc_labels, lm_labels, mc_token_ids):
    model = OpenAIGPTLMHeadModel(config)
    model.eval()
    loss = model(input_ids, position_ids, token_type_ids, lm_labels)
    lm_logits = model(input_ids, position_ids, token_type_ids)
    outputs = {'loss': loss, 'lm_logits': lm_logits}
    return outputs
