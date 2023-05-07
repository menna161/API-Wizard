from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import json
import random
import torch
from pytorch_pretrained_bert import BertConfig, BertModel, BertForMaskedLM, BertForNextSentencePrediction, BertForPreTraining, BertForQuestionAnswering, BertForSequenceClassification, BertForTokenClassification


def create_bert_model(self, config, input_ids, token_type_ids, input_mask, sequence_labels, token_labels):
    model = BertModel(config=config)
    model.eval()
    (all_encoder_layers, pooled_output) = model(input_ids, token_type_ids, input_mask)
    outputs = {'sequence_output': all_encoder_layers[(- 1)], 'pooled_output': pooled_output, 'all_encoder_layers': all_encoder_layers}
    return outputs
